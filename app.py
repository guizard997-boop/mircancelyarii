# -*- coding: utf-8 -*-
"""Мир канцелярии — магазин предзаказов.

Переменные окружения (Railway → Variables):
  ADMIN_PASSWORD         пароль админки (обязательно задайте свой)
  SECRET_KEY             любая длинная случайная строка
  DATA_DIR               папка для базы и загруженных фото (на Railway: путь Volume, например /data)
  SITE_URL               адрес сайта, https://...
  TELEGRAM_BOT_TOKEN     токен бота (необязательно)
  TELEGRAM_ADMIN_IDS     id админов через запятую (бот подскажет ваш id)
  TELEGRAM_WEBHOOK_SECRET  секрет вебхука (необязательно)
  GEMINI_API_KEY / HF_TOKEN  распознавание товара по фото в боте (необязательно)
"""
import hmac
import html as htmllib
import os
import re
import secrets
import time
import uuid
from datetime import datetime, timedelta
from functools import wraps

import requests
from flask import (Flask, Response, abort, flash, jsonify, redirect, render_template,
                   request, send_from_directory, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from jinja2 import DictLoader
from sqlalchemy import event, func, text
from sqlalchemy.engine import Engine

from templates_data import T

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get('DATA_DIR') or BASE_DIR
UPLOAD_DIR = os.path.join(DATA_DIR, 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _secret_key():
    key = os.environ.get('SECRET_KEY')
    if key:
        return key
    path = os.path.join(DATA_DIR, '.secret_key')
    try:
        if os.path.exists(path):
            return open(path).read().strip()
        key = secrets.token_hex(32)
        open(path, 'w').write(key)
        return key
    except OSError:
        return secrets.token_hex(32)


app = Flask(__name__)
app.config.update(
    SECRET_KEY=_secret_key(),
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(DATA_DIR, 'shop.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,
    PERMANENT_SESSION_LIFETIME=timedelta(days=30),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
app.jinja_env.loader = DictLoader(T)
db = SQLAlchemy(app)

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
STATUSES = ['Новый', 'В обработке', 'Ждёт оплаты', 'Оплачен', 'Готов', 'Выдан', 'Отменён']
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
DEFAULT_PW = not os.environ.get('ADMIN_PASSWORD')
PER_PAGE = 24


@event.listens_for(Engine, 'connect')
def _sqlite_unicode_lower(dbapi_conn, _):
    """SQLite по умолчанию не понимает регистр кириллицы: учим lower() работать с Unicode (поиск «ручка» = «Ручка»)."""
    try:
        dbapi_conn.create_function('lower', 1, lambda v: v.lower() if isinstance(v, str) else v)
    except Exception:  # noqa
        pass


# ============================ МОДЕЛИ ============================
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False, default=0)
    image_url = db.Column(db.String(500), default='/placeholder.svg')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=False)
    comment = db.Column(db.Text)
    token = db.Column(db.String(40))
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Новый')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product')


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, default='')


class PaymentMethod(db.Model):
    """Реквизиты для оплаты, которые владелец добавляет в админке."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    details = db.Column(db.Text, default='')
    qr_url = db.Column(db.String(500), default='')
    active = db.Column(db.Boolean, default=True)
    position = db.Column(db.Integer, default=0)


class BotState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(50), unique=True, nullable=False)
    step = db.Column(db.String(30), default='idle')
    draft_name = db.Column(db.String(300), default='')
    draft_image = db.Column(db.String(500), default='')
    draft_category_id = db.Column(db.Integer)


# ============================ ХЕЛПЕРЫ ============================
def get_setting(key, default=''):
    s = Setting.query.filter_by(key=key).first()
    return s.value if s and s.value is not None else default


def set_setting(key, value):
    s = Setting.query.filter_by(key=key).first()
    if s:
        s.value = value
    else:
        db.session.add(Setting(key=key, value=value))
    db.session.commit()


def get_cart():
    return session.get('cart', {})


def cart_count():
    return sum(get_cart().values())


def cart_items():
    items, total = [], 0.0
    for pid, qty in get_cart().items():
        p = db.session.get(Product, int(pid))
        if p:
            sub = (p.price or 0) * qty
            total += sub
            items.append((p, qty, sub))
    return items, total


def public_methods():
    return PaymentMethod.query.filter_by(active=True).order_by(PaymentMethod.position, PaymentMethod.id).all()


def allowed_file(name):
    return '.' in name and name.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def save_upload(fs):
    if not fs or not fs.filename or not allowed_file(fs.filename):
        return None
    name = f"{uuid.uuid4().hex}.{fs.filename.rsplit('.', 1)[1].lower()}"
    fs.save(os.path.join(UPLOAD_DIR, name))
    return f'/uploads/{name}'


def csrf_token():
    if 'csrf' not in session:
        session['csrf'] = secrets.token_hex(16)
    return session['csrf']


@app.before_request
def csrf_guard():
    if request.method == 'POST' and request.path.startswith('/admin') and request.path != '/admin':
        sent = request.form.get('_csrf', '').encode()
        if not hmac.compare_digest(sent, session.get('csrf', 'x').encode()):
            abort(400)


def admin_required(f):
    @wraps(f)
    def wrap(*a, **kw):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*a, **kw)
    return wrap


@app.template_filter('money')
def money(v):
    try:
        return f'{float(v):,.0f}'.replace(',', '\u00a0')
    except (TypeError, ValueError):
        return '0'


@app.template_filter('img')
def img(p):
    url = (p.image_url or '') if p else ''
    return '/placeholder.svg' if (not url or 'via.placeholder.com' in url) else url


@app.template_filter('tel')
def tel(s):
    return re.sub(r'[^\d+]', '', s or '')


@app.context_processor
def inject():
    raw = get_setting('phones')
    return dict(cart_count=cart_count(), csrf_token=csrf_token, statuses=STATUSES,
                categories=Category.query.order_by(Category.name).all(),
                phones=[l.strip() for l in raw.splitlines() if l.strip()],
                whatsapp=get_setting('whatsapp'))


# ============================ ФАЙЛЫ ============================
@app.route('/uploads/<path:fname>')
def uploaded_file(fname):
    resp = send_from_directory(UPLOAD_DIR, fname)
    resp.headers['Cache-Control'] = 'public, max-age=604800'
    return resp


@app.route('/placeholder.svg')
def placeholder():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><rect width="400" height="400" fill="#141414"/>'
           '<g fill="none" stroke="#555" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">'
           '<rect x="140" y="140" width="120" height="120" rx="16"/><circle cx="180" cy="182" r="10"/><path d="m150 250 40-40 30 28 20-18 20 30"/></g></svg>')
    return Response(svg, mimetype='image/svg+xml', headers={'Cache-Control': 'public, max-age=86400'})


# ============================ ВИТРИНА ============================
@app.route('/')
def index():
    products = Product.query.order_by(Product.created_at.desc(), Product.id.desc()).limit(8).all()
    return render_template('home.html', title='Главная', products=products, feature=products[:3])


@app.route('/catalog')
def catalog():
    q = request.args.get('q', '').strip()
    cur = request.args.get('category', type=int)
    sort = request.args.get('sort', 'new')
    page = request.args.get('page', 1, type=int)
    query = Product.query
    if q:
        like = f'%{q.lower()}%'
        query = query.filter(func.lower(Product.name).like(like) | func.lower(func.coalesce(Product.description, '')).like(like))
    if cur:
        query = query.filter(Product.category_id == cur)
    order = {'asc': Product.price.asc(), 'desc': Product.price.desc()}.get(sort, Product.created_at.desc())
    query = query.order_by(order, Product.id.desc())
    total = query.count()
    pages = max(1, -(-total // PER_PAGE))
    page = min(max(page, 1), pages)
    products = query.offset((page - 1) * PER_PAGE).limit(PER_PAGE).all()
    return render_template('catalog.html', title='Каталог', products=products, q=q, cur=cur,
                           sort=sort, page=page, pages=pages, total=total)


@app.route('/product/<int:pid>')
def product_detail(pid):
    p = db.get_or_404(Product, pid)
    related = []
    if p.category_id:
        related = Product.query.filter(Product.category_id == p.category_id, Product.id != p.id).limit(4).all()
    return render_template('product.html', title=p.name, p=p, related=related)


@app.route('/cart')
def cart():
    items, total = cart_items()
    return render_template('cart.html', title='Корзина', items=items, total=total, count=cart_count())


@app.route('/cart/add/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    p = db.get_or_404(Product, pid)
    qty = min(99, max(1, request.form.get('quantity', 1, type=int) or 1))
    c = get_cart()
    c[str(pid)] = min(99, c.get(str(pid), 0) + qty)
    session['cart'] = c
    session.permanent = True
    if request.headers.get('X-Requested-With') == 'fetch':
        return jsonify(ok=True, name=p.name, count=sum(c.values()))
    flash(f'Добавлено: {p.name}', 'success')
    return redirect(request.referrer or url_for('catalog'))


@app.route('/cart/update/<int:pid>', methods=['POST'])
def update_cart(pid):
    c = get_cart()
    if str(pid) in c:
        c[str(pid)] += request.form.get('delta', 0, type=int)
        if c[str(pid)] <= 0:
            c.pop(str(pid))
        c[str(pid)] = min(99, c[str(pid)]) if str(pid) in c else 0
        if not c[str(pid)]:
            c.pop(str(pid))
    session['cart'] = c
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    items, total = cart_items()
    if not items:
        flash('Корзина пуста', 'warning')
        return redirect(url_for('catalog'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()[:100]
        phone = request.form.get('phone', '').strip()[:30]
        if not name or len(tel(phone)) < 7:
            flash('Укажите имя и корректный телефон', 'danger')
            return redirect(url_for('checkout'))
        o = Order(customer_name=name, customer_phone=phone, total_price=total,
                  comment=request.form.get('comment', '').strip()[:1000], token=secrets.token_urlsafe(16))
        db.session.add(o)
        db.session.flush()
        for p, qty, _ in items:
            db.session.add(OrderItem(order_id=o.id, product_id=p.id, quantity=qty, price=p.price or 0))
        db.session.commit()
        session['cart'] = {}
        lines = '\n'.join(f'• {htmllib.escape(p.name)} × {q}' for p, q, _ in items)
        notify_admins(f'<b>Новый предзаказ №{o.id}</b>\n{htmllib.escape(name)} · {htmllib.escape(phone)}\n{lines}\n<b>Итого: {money(total)} сом</b>')
        return redirect(url_for('order_done', oid=o.id, token=o.token))
    return render_template('checkout.html', title='Оформление', items=items, total=total, methods=public_methods())


@app.route('/order/<int:oid>/<token>')
def order_done(oid, token):
    o = db.get_or_404(Order, oid)
    if not o.token or not hmac.compare_digest(o.token, token):
        abort(404)
    return render_template('order_done.html', title=f'Предзаказ №{o.id}', o=o, methods=public_methods())


# ============================ АДМИНКА ============================
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        pw = request.form.get('password', '')
        if hmac.compare_digest(pw.encode(), ADMIN_PASSWORD.encode()):
            session['admin'] = True
            csrf_token()
            return redirect(url_for('admin_dashboard'))
        time.sleep(0.8)
        flash('Неверный пароль', 'danger')
    return render_template('admin_login.html', title='Вход')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/')


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    orders = Order.query.order_by(Order.created_at.desc()).limit(8).all()
    revenue = db.session.query(db.func.coalesce(db.func.sum(Order.total_price), 0)).filter(Order.status != 'Отменён').scalar()
    return render_template('admin_dashboard.html', title='Админка', active='dashboard', orders=orders,
                           pc=Product.query.count(), oc=Order.query.count(),
                           nc=Order.query.filter_by(status='Новый').count(), revenue=revenue,
                           default_pw=DEFAULT_PW, methods=PaymentMethod.query.all())


# --- товары
@app.route('/admin/products')
@admin_required
def admin_products():
    q = request.args.get('q', '').strip()
    query = Product.query
    if q:
        query = query.filter(func.lower(Product.name).like(f'%{q.lower()}%'))
    return render_template('admin_products.html', title='Товары', active='products', q=q,
                           products=query.order_by(Product.created_at.desc(), Product.id.desc()).all())


@app.route('/admin/products/new', methods=['GET', 'POST'])
@app.route('/admin/products/<int:pid>', methods=['GET', 'POST'])
@admin_required
def admin_product_form(pid=None):
    p = db.get_or_404(Product, pid) if pid else None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()[:200]
        try:
            price = max(0.0, float(request.form.get('price') or 0))
        except ValueError:
            price = 0.0
        if not name:
            flash('Укажите название', 'danger')
            return redirect(request.url)
        if not p:
            p = Product()
            db.session.add(p)
        p.name, p.price = name, price
        p.description = request.form.get('description', '').strip()
        p.category_id = request.form.get('category_id', type=int) or None
        up = save_upload(request.files.get('photo'))
        if up:
            p.image_url = up
        elif not p.image_url:
            p.image_url = '/placeholder.svg'
        db.session.commit()
        flash('Сохранено', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin_product_form.html', title='Товар', active='products', p=p)


@app.route('/admin/products/<int:pid>/delete', methods=['POST'])
@admin_required
def admin_delete_product(pid):
    db.session.delete(db.get_or_404(Product, pid))
    db.session.commit()
    flash('Товар удалён', 'success')
    return redirect(url_for('admin_products'))


# --- заказы
@app.route('/admin/orders')
@admin_required
def admin_orders():
    st = request.args.get('status')
    query = Order.query.order_by(Order.created_at.desc())
    if st in STATUSES:
        query = query.filter_by(status=st)
    return render_template('admin_orders.html', title='Заказы', active='orders', orders=query.all(), st=st)


@app.route('/admin/orders/<int:oid>')
@admin_required
def admin_order(oid):
    return render_template('admin_order.html', title=f'Заказ №{oid}', active='orders', o=db.get_or_404(Order, oid))


@app.route('/admin/orders/<int:oid>/status', methods=['POST'])
@admin_required
def admin_order_status(oid):
    o = db.get_or_404(Order, oid)
    if request.form.get('status') in STATUSES:
        o.status = request.form['status']
        db.session.commit()
        flash('Статус обновлён', 'success')
    return redirect(url_for('admin_order', oid=oid))


@app.route('/admin/orders/<int:oid>/delete', methods=['POST'])
@admin_required
def admin_order_delete(oid):
    db.session.delete(db.get_or_404(Order, oid))
    db.session.commit()
    flash('Заказ удалён', 'success')
    return redirect(url_for('admin_orders'))


# --- категории
@app.route('/admin/categories', methods=['GET', 'POST'])
@admin_required
def admin_categories():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()[:100]
        if name and not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
            db.session.commit()
            flash('Категория добавлена', 'success')
        return redirect(url_for('admin_categories'))
    return render_template('admin_categories.html', title='Категории', active='categories',
                           cats=Category.query.order_by(Category.name).all())


@app.route('/admin/categories/<int:cid>/delete', methods=['POST'])
@admin_required
def admin_delete_category(cid):
    c = db.get_or_404(Category, cid)
    Product.query.filter_by(category_id=cid).update({'category_id': None})
    db.session.delete(c)
    db.session.commit()
    flash('Категория удалена', 'success')
    return redirect(url_for('admin_categories'))


# --- реквизиты для оплаты (свои способы оплаты)
@app.route('/admin/payments')
@admin_required
def admin_payments():
    edit = db.session.get(PaymentMethod, request.args.get('edit', type=int)) if request.args.get('edit') else None
    methods = PaymentMethod.query.order_by(PaymentMethod.position, PaymentMethod.id).all()
    return render_template('admin_payments.html', title='Оплата', active='payments', methods=methods, edit=edit)


@app.route('/admin/payments/save', methods=['POST'])
@admin_required
def admin_payment_save():
    title = request.form.get('title', '').strip()[:80]
    if not title:
        flash('Укажите название', 'danger')
        return redirect(url_for('admin_payments'))
    pid = request.form.get('id', type=int)
    m = db.session.get(PaymentMethod, pid) if pid else None
    if not m:
        m = PaymentMethod(position=PaymentMethod.query.count())
        db.session.add(m)
    m.title = title
    m.details = request.form.get('details', '').strip()[:2000]
    m.active = bool(request.form.get('active'))
    if request.form.get('remove_qr'):
        m.qr_url = ''
    up = save_upload(request.files.get('qr'))
    if up:
        m.qr_url = up
    db.session.commit()
    flash('Реквизиты сохранены', 'success')
    return redirect(url_for('admin_payments'))


@app.route('/admin/payments/<int:pid>/toggle', methods=['POST'])
@admin_required
def admin_payment_toggle(pid):
    m = db.get_or_404(PaymentMethod, pid)
    m.active = not m.active
    db.session.commit()
    return redirect(url_for('admin_payments'))


@app.route('/admin/payments/<int:pid>/delete', methods=['POST'])
@admin_required
def admin_payment_delete(pid):
    db.session.delete(db.get_or_404(PaymentMethod, pid))
    db.session.commit()
    flash('Реквизиты удалены', 'success')
    return redirect(url_for('admin_payments'))


# --- контакты
@app.route('/admin/contacts', methods=['GET', 'POST'])
@admin_required
def admin_contacts():
    if request.method == 'POST':
        set_setting('phones', request.form.get('phones', '').strip())
        set_setting('whatsapp', request.form.get('whatsapp', '').strip())
        flash('Контакты сохранены', 'success')
        return redirect(url_for('admin_contacts'))
    return render_template('admin_contacts.html', title='Контакты', active='contacts',
                           phones_raw=get_setting('phones'), bot_on=bool(TG_TOKEN))


# ============================ TELEGRAM-БОТ ============================
TG_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '').strip()
ADMIN_IDS = {x.strip() for x in os.environ.get('TELEGRAM_ADMIN_IDS', '').split(',') if x.strip()}


def site_url():
    return (os.environ.get('SITE_URL') or request.url_root).rstrip('/')


def tg(method, **data):
    if not TG_TOKEN:
        return None
    try:
        return requests.post(f'https://api.telegram.org/bot{TG_TOKEN}/{method}', json=data, timeout=30).json()
    except Exception as e:  # noqa
        print('TG error:', e)
        return None


def tg_send(chat_id, msg):
    return tg('sendMessage', chat_id=chat_id, text=msg, parse_mode='HTML')


def notify_admins(msg):
    for uid in ADMIN_IDS:
        tg_send(uid, msg)


def download_tg_photo(file_id):
    info = tg('getFile', file_id=file_id)
    if not info or not info.get('ok'):
        return None
    fp = info['result']['file_path']
    try:
        r = requests.get(f'https://api.telegram.org/file/bot{TG_TOKEN}/{fp}', timeout=60)
        ext = fp.rsplit('.', 1)[-1].lower() if '.' in fp else 'jpg'
        name = f"{uuid.uuid4().hex}.{ext if ext in ALLOWED_EXT else 'jpg'}"
        path = os.path.join(UPLOAD_DIR, name)
        with open(path, 'wb') as f:
            f.write(r.content)
        return f'/uploads/{name}', path
    except Exception as e:  # noqa
        print('photo error:', e)
        return None


CAT_RULES = [(['карандаш', 'ручк', 'маркер', 'фломастер', 'pen', 'pencil'], ['письм']),
             (['тетрад', 'блокнот', 'альбом', 'notebook'], ['тетрад', 'бумаг', 'блокнот']),
             (['краск', 'кист', 'гуаш', 'акварел', 'пластилин'], ['творч', 'рисов']),
             (['ранец', 'пенал', 'линейк', 'ластик', 'точилк'], ['школ']),
             (['степлер', 'скрепк', 'папк', 'файл', 'корректор'], ['офис'])]


def match_category(name):
    n = (name or '').lower()
    cats = Category.query.all()
    for keys, parts in CAT_RULES:
        if any(k in n for k in keys):
            for c in cats:
                if any(p in c.name.lower() for p in parts):
                    return c.id
    for c in cats:
        if c.name.lower() in n:
            return c.id
    return None


def ai_describe(path):
    """Название товара по фото: Gemini (по-русски) или Hugging Face. Без ключей вернёт None."""
    gem = os.environ.get('GEMINI_API_KEY', '').strip()
    if gem:
        try:
            import base64
            ext = path.rsplit('.', 1)[-1].lower()
            mime = {'png': 'image/png', 'webp': 'image/webp', 'gif': 'image/gif'}.get(ext, 'image/jpeg')
            b64 = base64.b64encode(open(path, 'rb').read()).decode()
            prompt = 'Это товар магазина канцелярии. Ответь одной строкой: название товара по-русски, 2-6 слов, без кавычек.'
            r = requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gem}',
                              json={'contents': [{'parts': [{'text': prompt}, {'inline_data': {'mime_type': mime, 'data': b64}}]}]}, timeout=45).json()
            name = r['candidates'][0]['content']['parts'][0]['text'].strip().splitlines()[0].strip('"\' ')[:200]
            if name:
                return name, match_category(name)
        except Exception as e:  # noqa
            print('Gemini error:', e)
    hf = (os.environ.get('HF_TOKEN') or '').strip()
    if hf:
        try:
            r = requests.post('https://router.huggingface.co/hf-inference/models/Salesforce/blip-image-captioning-base',
                              headers={'Authorization': f'Bearer {hf}'}, data=open(path, 'rb').read(), timeout=60)
            cap = (r.json() or [{}])[0].get('generated_text', '')
            if cap:
                return cap.strip().capitalize()[:200], match_category(cap)
        except Exception as e:  # noqa
            print('HF error:', e)
    return None, None


def bot_state(chat_id):
    st = BotState.query.filter_by(chat_id=str(chat_id)).first()
    if not st:
        st = BotState(chat_id=str(chat_id))
        db.session.add(st)
        db.session.commit()
    return st


@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    if not TG_TOKEN:
        return 'off', 200
    secret = os.environ.get('TELEGRAM_WEBHOOK_SECRET')
    if secret and request.headers.get('X-Telegram-Bot-Api-Secret-Token') != secret:
        abort(403)
    msg = (request.get_json(silent=True) or {}).get('message')
    if not msg:
        return 'ok'
    chat_id = msg['chat']['id']
    uid = str(msg.get('from', {}).get('id', ''))
    if uid not in ADMIN_IDS:
        tg_send(chat_id, f'Нет доступа.\nВаш id: <code>{uid}</code>\nДобавьте его в переменную TELEGRAM_ADMIN_IDS на сервере.')
        return 'ok'
    txt = (msg.get('text') or '').strip()
    st = bot_state(chat_id)

    def reset():
        st.step, st.draft_name, st.draft_image, st.draft_category_id = 'idle', '', '', None
        db.session.commit()

    if txt.startswith('/start') or txt.startswith('/help'):
        reset()
        tg_send(chat_id, 'Пришлите <b>фото товара</b>. Я определю название, спрошу цену и добавлю товар на сайт.\n/cancel — отменить')
        return 'ok'
    if txt.startswith('/cancel'):
        reset()
        tg_send(chat_id, 'Отменено. Пришлите новое фото.')
        return 'ok'
    if msg.get('photo'):
        tg_send(chat_id, 'Смотрю на фото…')
        res = download_tg_photo(msg['photo'][-1]['file_id'])
        if not res:
            tg_send(chat_id, 'Не удалось скачать фото. Попробуйте ещё раз.')
            return 'ok'
        url, path = res
        name, cat_id = ai_describe(path)
        st.draft_image, st.draft_name, st.draft_category_id = url, name or '', cat_id
        st.step = 'wait_price' if name else 'wait_name'
        db.session.commit()
        if name:
            tg_send(chat_id, f'Похоже, это: <b>{htmllib.escape(name)}</b>\nПришлите <b>цену</b> числом или другое название.')
        else:
            tg_send(chat_id, 'Фото получено. Напишите <b>название</b> товара:')
        return 'ok'
    if st.step == 'wait_name' and txt:
        st.draft_name, st.step = txt[:200], 'wait_price'
        db.session.commit()
        tg_send(chat_id, f'Название: <b>{htmllib.escape(st.draft_name)}</b>\nТеперь пришлите <b>цену в сомах</b>:')
        return 'ok'
    if st.step == 'wait_price' and txt:
        digits = re.sub(r'[^\d.,]', '', txt).replace(',', '.')
        try:
            price = float(digits)
            if price <= 0:
                raise ValueError
        except ValueError:
            st.draft_name = txt[:200]
            db.session.commit()
            tg_send(chat_id, f'Название обновлено: <b>{htmllib.escape(st.draft_name)}</b>\nПришлите <b>цену</b> числом:')
            return 'ok'
        p = Product(name=st.draft_name or 'Товар', price=price, description='',
                    image_url=st.draft_image or '/placeholder.svg', category_id=st.draft_category_id)
        db.session.add(p)
        db.session.commit()
        reset()
        tg_send(chat_id, f'Добавлено: <b>{htmllib.escape(p.name)}</b> — {money(price)} сом\n{site_url()}/product/{p.id}\n\nПришлите следующее фото.')
        return 'ok'
    tg_send(chat_id, 'Пришлите фото товара. /help — подсказка.')
    return 'ok'


@app.route('/admin/bot/webhook', methods=['POST'])
@admin_required
def admin_set_webhook():
    r = tg('setWebhook', url=f'{site_url()}/telegram-webhook', secret_token=os.environ.get('TELEGRAM_WEBHOOK_SECRET') or None)
    ok = bool(r and r.get('ok'))
    flash('Бот подключён' if ok else f'Не удалось подключить: {r}', 'success' if ok else 'danger')
    return redirect(url_for('admin_contacts'))


# ============================ ЗАПУСК ============================
def ensure_columns():
    with db.engine.begin() as c:
        cols = {r[1] for r in c.execute(text('PRAGMA table_info("order")'))}
        if cols and 'token' not in cols:
            c.execute(text('ALTER TABLE "order" ADD COLUMN token VARCHAR(40)'))
        if cols and 'comment' not in cols:
            c.execute(text('ALTER TABLE "order" ADD COLUMN comment TEXT'))


def migrate_old_requisites():
    """Переносит реквизиты из старой версии (раздел «Реквизиты») в новые способы оплаты."""
    if PaymentMethod.query.count() == 0:
        txt, qr = get_setting('rekvizity'), get_setting('rekvizity_image')
        if txt or qr:
            db.session.add(PaymentMethod(title='Основные реквизиты', details=txt, qr_url=qr or '', active=True))
            db.session.commit()


def init_db():
    from catalog_seed import seed
    with app.app_context():
        db.create_all()
        ensure_columns()
        migrate_old_requisites()
        try:
            seed(app, db, Product, Category)
        except Exception as e:  # noqa
            print('catalog seed error:', e)


init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
