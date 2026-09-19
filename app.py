# -*- coding: utf-8 -*-
"""Мир канцелярии — улучшенный магазин с предзаказом."""
import os
import uuid
from datetime import datetime
from functools import wraps

import requests
from flask import (
    Flask, request, redirect, url_for, session, flash,
    render_template_string, send_from_directory, abort, jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

_BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", _BASE)
try:
    os.makedirs(DATA_DIR, exist_ok=True)
except Exception:
    DATA_DIR = _BASE

UPLOAD = os.path.join(DATA_DIR, "uploads")
os.makedirs(UPLOAD, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mir-kanc-v2-secret-2026")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///" + os.path.join(DATA_DIR, "shop.db")
)
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"].replace(
        "postgres://", "postgresql://", 1
    )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

db = SQLAlchemy(app)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ADMIN_IDS = [
    x.strip()
    for x in os.environ.get("TELEGRAM_ADMIN_IDS", "").split(",")
    if x.strip()
]
SITE_NAME = os.environ.get("SITE_NAME", "Мир канцелярии")
SITE_PHONE = os.environ.get("SITE_PHONE", "")
SITE_TAGLINE = os.environ.get("SITE_TAGLINE", "Всё для учёбы и офиса · Предзаказ по Кыргызстану")

ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}


# ─── Models ───────────────────────────────────────────────
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    products = db.relationship("Product", backref="category", lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Float, default=0)
    image_url = db.Column(db.String(500), default="")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    in_stock = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, default="")
    total_price = db.Column(db.Float, default=0)
    status = db.Column(db.String(30), default="new")  # new / done / cancel
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=True)
    product_name = db.Column(db.String(200), default="")
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, default=0)


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    value = db.Column(db.Text, default="")


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50), default="")
    note = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    debts = db.relationship("Debt", backref="organization", lazy=True, cascade="all, delete-orphan")


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=True)
    product_name = db.Column(db.String(200), default="")
    quantity = db.Column(db.Integer, default=1)
    amount = db.Column(db.Float, default=0)
    description = db.Column(db.Text, default="")
    status = db.Column(db.String(20), default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)


DEFAULT_CATEGORIES = [
    "Письменные принадлежности",
    "Ручки и маркеры",
    "Карандаши и грифели",
    "Тетради и блокноты",
    "Бумага и альбомы",
    "Творчество и рисование",
    "Краски и кисти",
    "Школьные товары",
    "Пеналы и сумки",
    "Ранцы и рюкзаки",
    "Офисные принадлежности",
    "Файлы и папки",
    "Клей и скотч",
    "Стикеры и закладки",
    "Линейки и чертежные",
    "Калькуляторы",
    "Подарки и сувениры",
    "Для дошкольников",
]


# ─── Helpers ──────────────────────────────────────────────
def cart():
    return session.get("cart", {})


def cart_count():
    return sum(int(v) for v in cart().values())


def cart_total():
    total = 0.0
    for pid, qty in cart().items():
        p = db.session.get(Product, int(pid))
        if p:
            total += p.price * int(qty)
    return total


def cart_items():
    items = []
    for pid, qty in cart().items():
        p = db.session.get(Product, int(pid))
        if p:
            items.append({"product": p, "qty": int(qty), "sum": p.price * int(qty)})
    return items


def save_upload(f):
    if not f or not f.filename:
        return ""
    ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else ""
    if ext not in ALLOWED_EXT:
        return ""
    name = f"{uuid.uuid4().hex}.{ext}"
    f.save(os.path.join(UPLOAD, name))
    return "/uploads/" + name


def admin_required(f):
    @wraps(f)
    def w(*a, **k):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*a, **k)

    return w


def tg_notify_order(order):
    if not TELEGRAM_TOKEN or not ADMIN_IDS:
        return
    lines = [
        f"🛒 <b>Новая заявка #{order.id}</b>",
        f"👤 {order.customer_name}",
        f"📞 {order.customer_phone}",
    ]
    if order.comment:
        lines.append(f"💬 {order.comment}")
    lines.append("")
    lines.append("<b>Товары:</b>")
    for it in order.items:
        lines.append(f"• {it.product_name} × {it.quantity} — {it.price * it.quantity:,.0f} сом")
    lines.append("")
    lines.append(f"💰 <b>Итого: {order.total_price:,.0f} сом</b>")
    text = "\n".join(lines)
    for aid in ADMIN_IDS:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={"chat_id": aid, "text": text, "parse_mode": "HTML"},
                timeout=15,
            )
        except Exception as e:
            print("tg notify", e)


def money(v):
    try:
        return f"{float(v):,.0f}".replace(",", " ")
    except Exception:
        return "0"


# ─── Layout ───────────────────────────────────────────────
LAYOUT = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{{ title }} — {{ site_name }}</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = { theme: { extend: {
  colors: { brand: '#0D9488', brandd: '#0F766E', soft: '#F0FDFA', ink: '#134E4A', accent: '#F59E0B' },
  fontFamily: { sans: ['Nunito','system-ui','sans-serif'] }
}}}
</script>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
body{font-family:Nunito,system-ui,sans-serif}
.btn{background:linear-gradient(135deg,#0D9488,#0F766E);color:#fff;font-weight:700;border-radius:9999px;padding:.7rem 1.25rem;display:inline-block;transition:.15s}
.btn:hover{filter:brightness(1.06);transform:translateY(-1px)}
.btn-o{background:linear-gradient(135deg,#F59E0B,#D97706);color:#fff;font-weight:700;border-radius:9999px;padding:.7rem 1.25rem;display:inline-block}
.card{background:#fff;border:1px solid #ccfbf1;border-radius:1.25rem;overflow:hidden;transition:.2s}
.card:hover{box-shadow:0 12px 40px rgba(13,148,136,.12);transform:translateY(-2px)}
.chip{border-radius:9999px;padding:.35rem .9rem;font-size:.8rem;border:1px solid #99f6e4;background:#fff;color:#0F766E;display:inline-block}
.chip.active{background:#0D9488;color:#fff;border-color:#0D9488}
input,select,textarea{border:1px solid #99f6e4;border-radius:.9rem;padding:.65rem 1rem;width:100%}
input:focus,select:focus,textarea:focus{outline:2px solid #5eead4;outline-offset:1px}
.badge{position:absolute;top:-6px;right:-8px;background:#F59E0B;color:#fff;font-size:11px;font-weight:800;min-width:18px;height:18px;border-radius:999px;display:flex;align-items:center;justify-content:center;padding:0 5px}
</style>
</head>
<body class="bg-soft text-ink min-h-screen flex flex-col">
<header class="bg-white/90 backdrop-blur border-b border-teal-100 sticky top-0 z-50">
  <div class="max-w-6xl mx-auto px-4 h-16 flex items-center gap-3">
    <a href="/" class="font-extrabold text-brandd text-lg tracking-tight">{{ site_name }}</a>
    <form action="/catalog" method="get" class="hidden sm:flex flex-1 max-w-md mx-4">
      <input name="q" value="{{ request.args.get('q','') }}" placeholder="Поиск товаров..." class="text-sm">
    </form>
    <nav class="flex items-center gap-1 sm:gap-2 ml-auto text-sm font-semibold">
      <a href="/catalog" class="px-3 py-1.5 rounded-full hover:bg-teal-50">Каталог</a>
      <a href="/cart" class="relative px-3 py-1.5 rounded-full hover:bg-teal-50">
        Корзина{% if cart_count %}<span class="badge">{{ cart_count }}</span>{% endif %}
      </a>
      {% if session.get('admin') %}
      <a href="/admin/dashboard" class="px-3 py-1.5 rounded-full bg-teal-50 text-brandd">Админ</a>
      {% endif %}
    </nav>
  </div>
</header>

{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
<div class="max-w-6xl mx-auto px-4 pt-3 space-y-2">
{% for cat, msg in messages %}
<div class="text-sm px-4 py-2.5 rounded-xl {% if cat=='success' %}bg-emerald-50 text-emerald-800 border border-emerald-100{% else %}bg-red-50 text-red-700 border border-red-100{% endif %}">{{ msg }}</div>
{% endfor %}
</div>
{% endif %}
{% endwith %}

<main class="flex-1">{{ content|safe }}</main>

<footer class="mt-12 border-t border-teal-100 bg-white">
  <div class="max-w-6xl mx-auto px-4 py-8 grid sm:grid-cols-3 gap-6 text-sm">
    <div>
      <div class="font-extrabold text-brandd mb-2">{{ site_name }}</div>
      <p class="text-teal-800/70">{{ tagline }}</p>
    </div>
    <div>
      <div class="font-bold mb-2">Покупателям</div>
      <a href="/catalog" class="block text-teal-800/70 hover:text-brandd">Каталог</a>
      <a href="/cart" class="block text-teal-800/70 hover:text-brandd">Корзина</a>
    </div>
    <div>
      <div class="font-bold mb-2">Связь</div>
      {% if phone %}<a href="tel:{{ phone }}" class="block text-teal-800/70">{{ phone }}</a>{% endif %}
      <p class="text-teal-800/60 text-xs mt-2">Только предзаказ · Без доставки</p>
    </div>
  </div>
</footer>
</body></html>
"""


def render(title, content):
    from flask import get_flashed_messages

    return render_template_string(
        LAYOUT,
        title=title,
        content=content,
        site_name=SITE_NAME,
        tagline=SITE_TAGLINE,
        phone=SITE_PHONE,
        cart_count=cart_count(),
        session=session,
        request=request,
        get_flashed_messages=get_flashed_messages,
    )


def product_card(p):
    img = p.image_url or "https://placehold.co/400x400/f0fdfa/0d9488?text=+"
    stock = "" if p.in_stock else '<span class="text-xs text-red-500 font-bold">Нет в наличии</span>'
    return f"""
<a href="/product/{p.id}" class="card block group">
  <div class="aspect-square bg-teal-50 overflow-hidden">
    <img src="{img}" alt="" class="w-full h-full object-cover group-hover:scale-105 transition duration-300" loading="lazy"
      onerror="this.src='https://placehold.co/400x400/f0fdfa/0d9488?text=+'">
  </div>
  <div class="p-3">
    <div class="font-bold text-sm leading-snug line-clamp-2 min-h-[2.5rem]">{p.name}</div>
    <div class="mt-2 flex items-center justify-between gap-2">
      <span class="font-extrabold text-brandd">{money(p.price)} сом</span>
      {stock}
    </div>
  </div>
</a>"""


# ─── Public routes ────────────────────────────────────────
@app.route("/uploads/<path:filename>")
def uploaded(filename):
    return send_from_directory(UPLOAD, filename)


@app.route("/")
def index():
    products = Product.query.filter_by(in_stock=True).order_by(Product.created_at.desc()).limit(8).all()
    cats = Category.query.order_by(Category.name).all()
    chips = "".join(
        f'<a class="chip" href="/catalog?category={c.id}">{c.name}</a>' for c in cats[:12]
    )
    cards = "".join(product_card(p) for p in products) or (
        '<p class="col-span-full text-center text-teal-800/50 py-16">Каталог пока пуст — загляните позже</p>'
    )
    content = f"""
<section class="relative overflow-hidden">
  <div class="max-w-6xl mx-auto px-4 py-12 sm:py-16">
    <div class="max-w-xl">
      <p class="text-brand font-bold text-sm mb-2">Предзаказ по Кыргызстану</p>
      <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3">{SITE_NAME}</h1>
      <p class="text-teal-900/70 mb-6">{SITE_TAGLINE}</p>
      <a href="/catalog" class="btn-o">Смотреть каталог →</a>
    </div>
  </div>
</section>
<section class="max-w-6xl mx-auto px-4 pb-6">
  <div class="flex flex-wrap gap-2 mb-8">{chips}</div>
  <div class="flex items-end justify-between mb-4">
    <h2 class="text-xl font-extrabold">Новинки</h2>
    <a href="/catalog" class="text-sm font-bold text-brandd">Весь каталог</a>
  </div>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">{cards}</div>
</section>"""
    return render("Главная", content)


@app.route("/catalog")
def catalog():
    q = request.args.get("q", "").strip()
    cat_id = request.args.get("category", type=int)
    query = Product.query
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))
    if cat_id:
        query = query.filter_by(category_id=cat_id)
    products = query.order_by(Product.created_at.desc()).all()
    cats = Category.query.order_by(Category.name).all()

    chip_all = "chip active" if not cat_id else "chip"
    chips = [f'<a class="{chip_all}" href="/catalog">Все</a>']
    for c in cats:
        cls = "chip active" if cat_id == c.id else "chip"
        href = f"/catalog?category={c.id}" + (f"&q={q}" if q else "")
        chips.append(f'<a class="{cls}" href="{href}">{c.name}</a>')

    cards = "".join(product_card(p) for p in products) or (
        '<p class="col-span-full text-center text-teal-800/50 py-16">Ничего не найдено</p>'
    )
    content = f"""
<div class="max-w-6xl mx-auto px-4 py-8">
  <h1 class="text-2xl font-extrabold mb-4">Каталог</h1>
  <form method="get" class="flex gap-2 mb-4 max-w-lg">
    <input type="hidden" name="category" value="{cat_id or ''}">
    <input name="q" value="{q.replace('"', '&quot;')}" placeholder="Поиск..." class="text-sm flex-1">
    <button class="btn text-sm !rounded-xl !py-2">Найти</button>
  </form>
  <div class="flex flex-wrap gap-2 mb-6">{''.join(chips)}</div>
  <p class="text-sm text-teal-800/60 mb-3">{len(products)} товар(ов)</p>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">{cards}</div>
</div>"""
    return render("Каталог", content)


@app.route("/product/<int:pid>")
def product_detail(pid):
    p = db.session.get(Product, pid)
    if not p:
        abort(404)
    img = p.image_url or "https://placehold.co/600x600/f0fdfa/0d9488?text=+"
    cat = p.category.name if p.category else ""
    desc = (p.description or "Описание появится позже.").replace("\n", "<br>")
    cat_html = f'<span class="chip mb-3">{cat}</span>' if cat else ""
    content = f"""
<div class="max-w-6xl mx-auto px-4 py-8 grid md:grid-cols-2 gap-8">
  <div class="card aspect-square bg-teal-50">
    <img src="{img}" class="w-full h-full object-cover" alt=""
      onerror="this.src='https://placehold.co/600x600/f0fdfa/0d9488?text=+'">
  </div>
  <div>
    {cat_html}
    <h1 class="text-2xl sm:text-3xl font-extrabold mb-2 mt-2">{p.name}</h1>
    <div class="text-3xl font-extrabold text-brandd mb-4">{money(p.price)} сом</div>
    <div class="text-teal-900/70 text-sm leading-relaxed mb-6">{desc}</div>
    <form action="/cart/add/{p.id}" method="post" class="flex flex-wrap gap-3 items-center">
      <input type="number" name="qty" value="1" min="1" max="99" class="!w-20 text-center">
      <button class="btn-o" type="submit">В предзаказ</button>
      <a href="/catalog" class="text-sm font-bold text-brandd">← В каталог</a>
    </form>
    <p class="text-xs text-teal-800/50 mt-4">Только предзаказ · Без доставки · Мы свяжемся с вами</p>
  </div>
</div>"""
    return render(p.name, content)


@app.route("/cart")
def cart_page():
    items = cart_items()
    if not items:
        content = """
<div class="max-w-lg mx-auto px-4 py-20 text-center">
  <div class="text-5xl mb-4">🛒</div>
  <h1 class="text-xl font-extrabold mb-2">Предзаказ пуст</h1>
  <p class="text-teal-800/60 mb-6">Добавьте товары из каталога</p>
  <a href="/catalog" class="btn">В каталог</a>
</div>"""
        return render("Корзина", content)

    rows = ""
    for it in items:
        p = it["product"]
        rows += f"""
<div class="flex gap-3 items-center border-b border-teal-50 py-3">
  <img src="{p.image_url or ''}" class="w-16 h-16 rounded-xl object-cover bg-teal-50" onerror="this.style.background='#f0fdfa'">
  <div class="flex-1 min-w-0">
    <a href="/product/{p.id}" class="font-bold text-sm line-clamp-1">{p.name}</a>
    <div class="text-xs text-teal-800/60">{money(p.price)} сом</div>
  </div>
  <form action="/cart/update/{p.id}" method="post" class="flex items-center gap-1">
    <input type="number" name="qty" value="{it['qty']}" min="0" max="99" class="!w-14 text-center text-sm">
  </form>
  <div class="font-extrabold text-sm w-20 text-right">{money(it['sum'])}</div>
  <a href="/cart/remove/{p.id}" class="text-red-400 text-xs font-bold">✕</a>
</div>"""

    content = f"""
<div class="max-w-2xl mx-auto px-4 py-8">
  <h1 class="text-2xl font-extrabold mb-4">Ваш предзаказ</h1>
  <div class="card p-4 mb-4">{rows}</div>
  <div class="flex items-center justify-between mb-6">
    <span class="text-teal-800/70">Итого</span>
    <span class="text-2xl font-extrabold text-brandd">{money(cart_total())} сом</span>
  </div>
  <a href="/checkout" class="btn-o w-full text-center block">Оформить предзаказ</a>
  <a href="/catalog" class="block text-center text-sm font-bold text-brandd mt-3">← Продолжить выбор</a>
</div>"""
    return render("Корзина", content)


@app.route("/cart/add/<int:pid>", methods=["POST"])
def cart_add(pid):
    p = db.session.get(Product, pid)
    if not p:
        abort(404)
    try:
        qty = max(1, int(request.form.get("qty", 1)))
    except ValueError:
        qty = 1
    c = cart()
    c[str(pid)] = int(c.get(str(pid), 0)) + qty
    session["cart"] = c
    flash(f"{p.name} добавлен в предзаказ", "success")
    return redirect(request.referrer or url_for("catalog"))


@app.route("/cart/update/<int:pid>", methods=["POST"])
def cart_update(pid):
    try:
        qty = int(request.form.get("qty", 1))
    except ValueError:
        qty = 1
    c = cart()
    if qty <= 0:
        c.pop(str(pid), None)
    else:
        c[str(pid)] = qty
    session["cart"] = c
    return redirect(url_for("cart_page"))


@app.route("/cart/remove/<int:pid>")
def cart_remove(pid):
    c = cart()
    c.pop(str(pid), None)
    session["cart"] = c
    return redirect(url_for("cart_page"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not cart():
        flash("Предзаказ пуст", "danger")
        return redirect(url_for("catalog"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        comment = request.form.get("comment", "").strip()
        if not name or not phone:
            flash("Укажите имя и телефон", "danger")
            return redirect(url_for("checkout"))
        order = Order(
            customer_name=name,
            customer_phone=phone,
            comment=comment,
            total_price=cart_total(),
            status="new",
        )
        db.session.add(order)
        db.session.flush()
        for pid, qty in cart().items():
            p = db.session.get(Product, int(pid))
            if p:
                db.session.add(
                    OrderItem(
                        order_id=order.id,
                        product_id=p.id,
                        product_name=p.name,
                        quantity=int(qty),
                        price=p.price,
                    )
                )
        db.session.commit()
        try:
            tg_notify_order(order)
        except Exception as e:
            print("notify", e)
        session["cart"] = {}
        content = f"""
<div class="max-w-md mx-auto px-4 py-16 text-center">
  <div class="text-5xl mb-4">✅</div>
  <h1 class="text-2xl font-extrabold mb-2">Заявка #{order.id} принята</h1>
  <p class="text-teal-800/70 mb-6">Мы свяжемся с вами по телефону <b>{phone}</b></p>
  <a href="/catalog" class="btn">В каталог</a>
</div>"""
        return render("Спасибо", content)

    content = f"""
<div class="max-w-md mx-auto px-4 py-8">
  <h1 class="text-2xl font-extrabold mb-2">Оформление</h1>
  <p class="text-sm text-teal-800/60 mb-6">Итого: <b class="text-brandd">{money(cart_total())} сом</b> · Без доставки</p>
  <form method="post" class="card p-5 space-y-3">
    <div><label class="text-xs font-bold text-teal-800/60">Имя</label>
    <input name="name" required placeholder="Как к вам обращаться"></div>
    <div><label class="text-xs font-bold text-teal-800/60">Телефон</label>
    <input name="phone" required placeholder="+996 ..." inputmode="tel"></div>
    <div><label class="text-xs font-bold text-teal-800/60">Комментарий</label>
    <textarea name="comment" rows="2" placeholder="Необязательно"></textarea></div>
    <button class="btn-o w-full text-center" type="submit">Отправить заявку</button>
  </form>
</div>"""
    return render("Оформление", content)


# ─── Admin ────────────────────────────────────────────────
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if session.get("admin"):
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Неверный пароль", "danger")
    content = """
<div class="min-h-[60vh] flex items-center justify-center px-4">
  <form method="post" class="card p-6 w-full max-w-xs text-center space-y-3">
    <h1 class="font-extrabold text-lg">Админ-панель</h1>
    <input type="password" name="password" required placeholder="Пароль" class="text-center">
    <button class="btn w-full" type="submit">Войти</button>
  </form>
</div>"""
    return render("Вход", content)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/")


def admin_nav(active=""):
    links = [
        ("dashboard", "/admin/dashboard", "Дашборд"),
        ("products", "/admin/products", "Товары"),
        ("orders", "/admin/orders", "Заявки"),
        ("orgs", "/admin/orgs", "Организации"),
        ("debts", "/admin/debts", "Долги"),
        ("categories", "/admin/categories", "Категории"),
    ]
    html = '<div class="flex flex-wrap gap-2 text-sm mb-6">'
    for key, href, label in links:
        cls = "chip active" if active == key else "chip"
        html += f'<a class="{cls}" href="{href}">{label}</a>'
    html += '<a class="chip !text-red-500 !border-red-200" href="/admin/logout">Выйти</a></div>'
    return html


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    pc = Product.query.count()
    oc = Order.query.filter_by(status="new").count()
    total_orders = Order.query.count()
    debt_open = db.session.query(db.func.coalesce(db.func.sum(Debt.amount), 0)).filter_by(status="open").scalar() or 0
    content = f"""
<div class="max-w-3xl mx-auto px-4 py-8">
{admin_nav('dashboard')}
<h1 class="text-xl font-extrabold mb-4">Дашборд</h1>
<div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
  <div class="card p-4"><div class="text-xs text-teal-800/50">Товары</div><div class="text-2xl font-extrabold">{pc}</div></div>
  <div class="card p-4"><div class="text-xs text-teal-800/50">Новые заявки</div><div class="text-2xl font-extrabold text-amber-600">{oc}</div></div>
  <div class="card p-4"><div class="text-xs text-teal-800/50">Всего заявок</div><div class="text-2xl font-extrabold">{total_orders}</div></div>
  <div class="card p-4"><div class="text-xs text-teal-800/50">Открытые долги</div><div class="text-2xl font-extrabold text-red-500">{money(debt_open)}</div></div>
</div>
<div class="flex flex-wrap gap-2">
<a href="/admin/products/add" class="btn text-sm">+ Товар</a>
<a href="/admin/debts/add" class="btn text-sm" style="background:linear-gradient(135deg,#F59E0B,#D97706)">+ Долг</a>
</div>
</div>"""
    return render("Админ", content)


@app.route("/admin/products")
@admin_required
def admin_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    rows = ""
    for p in products:
        rows += f"""
<tr class="border-t border-teal-50">
  <td class="py-2 pr-2"><img src="{p.image_url or ''}" class="w-10 h-10 rounded-lg object-cover bg-teal-50"></td>
  <td class="py-2 font-semibold text-sm">{p.name}</td>
  <td class="py-2 text-sm">{money(p.price)}</td>
  <td class="py-2 text-sm">
    <a href="/admin/products/edit/{p.id}" class="text-brandd font-bold">Изм.</a>
    <form action="/admin/products/delete/{p.id}" method="post" class="inline" onsubmit="return confirm('Удалить?')">
      <button class="text-red-400 font-bold ml-2">Удал.</button>
    </form>
  </td>
</tr>"""
    content = f"""
<div class="max-w-3xl mx-auto px-4 py-8">
{admin_nav('products')}
<div class="flex justify-between items-center mb-4">
  <h1 class="text-xl font-extrabold">Товары</h1>
  <a href="/admin/products/add" class="btn text-sm !py-1.5">+ Добавить</a>
</div>
<div class="card p-4 overflow-x-auto">
<table class="w-full text-sm"><thead><tr class="text-left text-teal-800/50">
<th class="pb-2"></th><th class="pb-2">Название</th><th class="pb-2">Цена</th><th></th>
</tr></thead><tbody>{rows or '<tr><td colspan="4" class="py-8 text-center text-teal-800/40">Пусто</td></tr>'}</tbody></table>
</div></div>"""
    return render("Товары", content)


@app.route("/admin/products/add", methods=["GET", "POST"])
@app.route("/admin/products/edit/<int:pid>", methods=["GET", "POST"])
@admin_required
def admin_product_form(pid=None):
    p = db.session.get(Product, pid) if pid else None
    cats = Category.query.order_by(Category.name).all()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Укажите название", "danger")
            return redirect(request.url)
        try:
            price = float(str(request.form.get("price", "0")).replace(",", "."))
        except ValueError:
            price = 0
        cat_id = request.form.get("category_id") or None
        if cat_id:
            cat_id = int(cat_id)
        img = save_upload(request.files.get("image"))
        if p:
            p.name = name
            p.price = price
            p.description = request.form.get("description", "").strip()
            p.category_id = cat_id
            p.in_stock = bool(request.form.get("in_stock"))
            if img:
                p.image_url = img
        else:
            p = Product(
                name=name,
                price=price,
                description=request.form.get("description", "").strip(),
                category_id=cat_id,
                image_url=img or "",
                in_stock=bool(request.form.get("in_stock")),
            )
            db.session.add(p)
        db.session.commit()
        flash("Сохранено", "success")
        return redirect(url_for("admin_products"))

    opts = '<option value="">— без категории —</option>'
    for c in cats:
        sel = "selected" if p and p.category_id == c.id else ""
        opts += f'<option value="{c.id}" {sel}>{c.name}</option>'
    content = f"""
<div class="max-w-md mx-auto px-4 py-8">
{admin_nav('products')}
<h1 class="text-xl font-extrabold mb-4">{'Изменить' if p else 'Новый'} товар</h1>
<form method="post" enctype="multipart/form-data" class="card p-5 space-y-3">
  <input name="name" required value="{p.name if p else ''}" placeholder="Название">
  <input name="price" type="number" step="0.01" value="{p.price if p else ''}" placeholder="Цена (сом)">
  <select name="category_id">{opts}</select>
  <textarea name="description" rows="3" placeholder="Описание">{p.description if p else ''}</textarea>
  <div><label class="text-xs font-bold text-teal-800/60">Фото</label>
  <input type="file" name="image" accept="image/*"></div>
  <label class="flex items-center gap-2 text-sm"><input type="checkbox" name="in_stock" value="1" {"checked" if not p or p.in_stock else ""}> В наличии</label>
  <button class="btn w-full" type="submit">Сохранить</button>
</form></div>"""
    return render("Товар", content)


@app.route("/admin/products/delete/<int:pid>", methods=["POST"])
@admin_required
def admin_product_delete(pid):
    p = db.session.get(Product, pid)
    if p:
        db.session.delete(p)
        db.session.commit()
        flash("Удалено", "success")
    return redirect(url_for("admin_products"))


@app.route("/admin/orders")
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.created_at.desc()).limit(100).all()
    blocks = ""
    for o in orders:
        items = "".join(
            f'<div class="text-xs text-teal-800/70">• {it.product_name} × {it.quantity} — {money(it.price * it.quantity)} сом</div>'
            for it in o.items
        )
        st_color = {"new": "text-amber-600", "done": "text-emerald-600", "cancel": "text-red-400"}.get(o.status, "")
        st_label = {"new": "Новая", "done": "Готово", "cancel": "Отмена"}.get(o.status, o.status)
        actions = ""
        if o.status == "new":
            actions = f"""
<form action="/admin/orders/{o.id}/status" method="post" class="inline">
  <input type="hidden" name="status" value="done">
  <button class="text-emerald-600 font-bold text-xs">Готово</button>
</form>
<form action="/admin/orders/{o.id}/status" method="post" class="inline ml-2">
  <input type="hidden" name="status" value="cancel">
  <button class="text-red-400 font-bold text-xs">Отмена</button>
</form>"""
        blocks += f"""
<div class="card p-4 mb-3">
  <div class="flex justify-between gap-2 mb-1">
    <div class="font-extrabold">#{o.id} · {o.customer_name}</div>
    <div class="text-xs font-bold {st_color}">{st_label}</div>
  </div>
  <div class="text-sm">{o.customer_phone}</div>
  {f'<div class="text-xs text-teal-800/50 mt-1">{o.comment}</div>' if o.comment else ''}
  <div class="mt-2 space-y-0.5">{items}</div>
  <div class="mt-2 flex justify-between items-center">
    <span class="font-extrabold text-brandd">{money(o.total_price)} сом</span>
    <div>{actions}</div>
  </div>
</div>"""
    content = f"""
<div class="max-w-2xl mx-auto px-4 py-8">
{admin_nav('orders')}
<h1 class="text-xl font-extrabold mb-4">Заявки</h1>
{blocks or '<p class="text-teal-800/40 text-center py-12">Заявок пока нет</p>'}
</div>"""
    return render("Заявки", content)


@app.route("/admin/orders/<int:oid>/status", methods=["POST"])
@admin_required
def admin_order_status(oid):
    o = db.session.get(Order, oid)
    if o:
        st = request.form.get("status", "")
        if st in ("new", "done", "cancel"):
            o.status = st
            db.session.commit()
    return redirect(url_for("admin_orders"))


@app.route("/admin/categories", methods=["GET", "POST"])
@admin_required
def admin_categories():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name and not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
            db.session.commit()
            flash("Категория добавлена", "success")
        return redirect(url_for("admin_categories"))
    cats = Category.query.order_by(Category.name).all()
    rows = "".join(
        f'<div class="flex justify-between py-2 border-b border-teal-50 text-sm"><span>{c.name}</span>'
        f'<form method="post" action="/admin/categories/delete/{c.id}" onsubmit="return confirm(\'Удалить?\')">'
        f'<button class="text-red-400 font-bold">Удал.</button></form></div>'
        for c in cats
    )
    content = f"""
<div class="max-w-md mx-auto px-4 py-8">
{admin_nav('categories')}
<h1 class="text-xl font-extrabold mb-4">Категории</h1>
<form method="post" class="flex gap-2 mb-4">
  <input name="name" required placeholder="Новая категория" class="flex-1">
  <button class="btn text-sm !rounded-xl">+</button>
</form>
<div class="card p-4">{rows or '<p class="text-teal-800/40 text-center">Пусто</p>'}</div>
</div>"""
    return render("Категории", content)


@app.route("/admin/categories/delete/<int:cid>", methods=["POST"])
@admin_required
def admin_cat_delete(cid):
    c = db.session.get(Category, cid)
    if c:
        Product.query.filter_by(category_id=cid).update({"category_id": None})
        db.session.delete(c)
        db.session.commit()
    return redirect(url_for("admin_categories"))


@app.route("/admin/orgs")
@admin_required
def admin_orgs():
    orgs = Organization.query.order_by(Organization.name).all()
    rows = ""
    for o in orgs:
        s = sum(d.amount or 0 for d in o.debts if d.status == "open")
        red = "text-red-500" if s else "text-teal-800/30"
        rows += (
            f'<tr class="border-t border-teal-50">'
            f'<td class="py-2 font-semibold text-sm">{o.name}</td>'
            f'<td class="py-2 text-sm text-teal-800/60">{o.phone or "—"}</td>'
            f'<td class="py-2 text-sm font-bold {red}">{money(s)}</td>'
            f'<td class="py-2 text-sm">'
            f'<a href="/admin/debts?org={o.id}" class="text-brandd font-bold">Долги</a> '
            f'<a href="/admin/orgs/edit/{o.id}" class="text-brandd font-bold">Изм.</a> '
            f'<form action="/admin/orgs/delete/{o.id}" method="post" class="inline" '
            f'onsubmit="return confirm(\'Удалить?\')">'
            f'<button class="text-red-400 font-bold">Удал.</button></form></td></tr>'
        )
    content = f"""
<div class="max-w-3xl mx-auto px-4 py-8">
{admin_nav('orgs')}
<div class="flex justify-between items-center mb-4">
  <h1 class="text-xl font-extrabold">Организации</h1>
  <a href="/admin/orgs/add" class="btn text-sm !py-1.5">+ Добавить</a>
</div>
<div class="card p-4 overflow-x-auto">
<table class="w-full text-sm"><thead><tr class="text-left text-teal-800/50">
<th class="pb-2">Название</th><th class="pb-2">Телефон</th><th class="pb-2">Долг</th><th></th>
</tr></thead><tbody>{rows or '<tr><td colspan="4" class="py-8 text-center text-teal-800/40">Пусто</td></tr>'}</tbody></table>
</div></div>"""
    return render("Организации", content)


@app.route("/admin/orgs/add", methods=["GET", "POST"])
@app.route("/admin/orgs/edit/<int:oid>", methods=["GET", "POST"])
@admin_required
def admin_org_form(oid=None):
    o = db.session.get(Organization, oid) if oid else None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Укажите название", "danger")
            return redirect(request.url)
        if o:
            o.name = name
            o.phone = request.form.get("phone", "").strip()
            o.note = request.form.get("note", "").strip()
        else:
            db.session.add(Organization(
                name=name,
                phone=request.form.get("phone", "").strip(),
                note=request.form.get("note", "").strip(),
            ))
        db.session.commit()
        flash("Сохранено", "success")
        return redirect(url_for("admin_orgs"))
    content = f"""
<div class="max-w-md mx-auto px-4 py-8">
{admin_nav('orgs')}
<h1 class="text-xl font-extrabold mb-4">{'Изменить' if o else 'Новая'} организация</h1>
<form method="post" class="card p-5 space-y-3">
  <input name="name" required value="{o.name if o else ''}" placeholder="Название организации">
  <input name="phone" value="{o.phone if o else ''}" placeholder="Телефон">
  <textarea name="note" rows="2" placeholder="Заметка">{o.note if o else ''}</textarea>
  <button class="btn w-full" type="submit">Сохранить</button>
</form></div>"""
    return render("Организация", content)


@app.route("/admin/orgs/delete/<int:oid>", methods=["POST"])
@admin_required
def admin_org_delete(oid):
    o = db.session.get(Organization, oid)
    if o:
        db.session.delete(o)
        db.session.commit()
        flash("Удалено", "success")
    return redirect(url_for("admin_orgs"))


@app.route("/admin/debts")
@admin_required
def admin_debts():
    org_id = request.args.get("org", type=int)
    status = request.args.get("status", "open")
    q = Debt.query
    if org_id:
        q = q.filter_by(organization_id=org_id)
    if status in ("open", "paid"):
        q = q.filter_by(status=status)
    debts = q.order_by(Debt.created_at.desc()).limit(200).all()
    orgs = {x.id: x.name for x in Organization.query.all()}
    rows = ""
    for d in debts:
        name = orgs.get(d.organization_id, "—")
        st = "Открыт" if d.status == "open" else "Погашен"
        stc = "text-red-500" if d.status == "open" else "text-emerald-600"
        prod = d.product_name or "—"
        act = ""
        if d.status == "open":
            act += (
                f'<form action="/admin/debts/pay/{d.id}" method="post" class="inline">'
                f'<button class="text-emerald-600 font-bold text-xs">Погасить</button></form> '
            )
        act += (
            f'<form action="/admin/debts/delete/{d.id}" method="post" class="inline" '
            f'onsubmit="return confirm(\'Удалить?\')">'
            f'<button class="text-red-400 font-bold text-xs">Удал.</button></form>'
        )
        rows += (
            f'<tr class="border-t border-teal-50">'
            f'<td class="py-2 text-sm">{name}</td>'
            f'<td class="py-2 text-sm">{prod} × {d.quantity}</td>'
            f'<td class="py-2 text-sm font-bold">{money(d.amount)}</td>'
            f'<td class="py-2 text-xs {stc}">{st}</td>'
            f'<td class="py-2">{act}</td></tr>'
        )
    total = db.session.query(db.func.coalesce(db.func.sum(Debt.amount), 0)).filter_by(status="open").scalar() or 0
    a_open = "active" if status == "open" else ""
    a_paid = "active" if status == "paid" else ""
    a_all = "active" if status == "all" else ""
    content = f"""
<div class="max-w-4xl mx-auto px-4 py-8">
{admin_nav('debts')}
<div class="flex justify-between items-center mb-2">
  <h1 class="text-xl font-extrabold">Долги</h1>
  <a href="/admin/debts/add" class="btn text-sm !py-1.5">+ Долг по товару</a>
</div>
<p class="text-sm text-teal-800/60 mb-3">Открытых: <b class="text-red-500">{money(total)} сом</b></p>
<p class="text-sm mb-4 space-x-1">
  <a href="/admin/debts?status=open" class="chip {a_open}">Открытые</a>
  <a href="/admin/debts?status=paid" class="chip {a_paid}">Погашенные</a>
  <a href="/admin/debts?status=all" class="chip {a_all}">Все</a>
</p>
<div class="card p-4 overflow-x-auto">
<table class="w-full text-sm"><thead><tr class="text-left text-teal-800/50">
<th class="pb-2">Организация</th><th class="pb-2">Товар</th><th class="pb-2">Сумма</th><th class="pb-2">Статус</th><th></th>
</tr></thead><tbody>{rows or '<tr><td colspan="5" class="py-8 text-center text-teal-800/40">Нет записей</td></tr>'}</tbody></table>
</div></div>"""
    return render("Долги", content)


@app.route("/admin/debts/add", methods=["GET", "POST"])
@admin_required
def admin_debt_add():
    orgs = Organization.query.order_by(Organization.name).all()
    products = Product.query.order_by(Product.name).all()
    if request.method == "POST":
        try:
            oid = int(request.form.get("organization_id") or 0)
            qty = max(1, int(request.form.get("quantity") or 1))
        except ValueError:
            flash("Проверьте данные", "danger")
            return redirect(url_for("admin_debt_add"))
        if not oid or not db.session.get(Organization, oid):
            flash("Выберите организацию", "danger")
            return redirect(url_for("admin_debt_add"))
        pid_raw = request.form.get("product_id") or ""
        product_name = ""
        amount = 0.0
        pid = None
        if pid_raw:
            pid = int(pid_raw)
            p = db.session.get(Product, pid)
            if p:
                product_name = p.name
                amount = float(p.price) * qty
        if not product_name:
            product_name = request.form.get("manual_name", "").strip() or "Товар"
            try:
                amount = float(str(request.form.get("manual_amount", "0")).replace(",", ".")) * qty
            except ValueError:
                amount = 0
        if amount <= 0:
            flash("Сумма должна быть больше 0", "danger")
            return redirect(url_for("admin_debt_add"))
        db.session.add(Debt(
            organization_id=oid,
            product_id=pid,
            product_name=product_name,
            quantity=qty,
            amount=amount,
            description=request.form.get("description", "").strip(),
            status="open",
        ))
        db.session.commit()
        flash("Долг записан на организацию", "success")
        return redirect(url_for("admin_debts"))

    if not orgs:
        content = f"""
<div class="max-w-md mx-auto px-4 py-8">
{admin_nav('debts')}
<p class="text-teal-800/60 mb-4">Сначала добавьте организацию.</p>
<a href="/admin/orgs/add" class="btn">+ Организация</a>
</div>"""
        return render("Долг", content)

    o_opts = "".join(f'<option value="{o.id}">{o.name}</option>' for o in orgs)
    p_opts = '<option value="">— выбрать товар из магазина —</option>'
    for p in products:
        p_opts += f'<option value="{p.id}">{p.name} — {money(p.price)} сом</option>'
    content = f"""
<div class="max-w-md mx-auto px-4 py-8">
{admin_nav('debts')}
<h1 class="text-xl font-extrabold mb-2">Долг по товару</h1>
<p class="text-sm text-teal-800/60 mb-4">Товар из каталога → счёт организации</p>
<form method="post" class="card p-5 space-y-3">
  <label class="text-xs font-bold text-teal-800/60">Организация</label>
  <select name="organization_id" required>{o_opts}</select>
  <label class="text-xs font-bold text-teal-800/60">Товар из магазина</label>
  <select name="product_id">{p_opts}</select>
  <label class="text-xs font-bold text-teal-800/60">Количество</label>
  <input type="number" name="quantity" value="1" min="1" max="999">
  <p class="text-xs text-teal-800/50">Или вручную (если товара нет в списке):</p>
  <input name="manual_name" placeholder="Название вручную">
  <input name="manual_amount" type="number" step="0.01" placeholder="Цена за 1 шт (сом)">
  <textarea name="description" rows="2" placeholder="Комментарий"></textarea>
  <button class="btn w-full" type="submit">Записать долг</button>
</form></div>"""
    return render("Новый долг", content)


@app.route("/admin/debts/pay/<int:did>", methods=["POST"])
@admin_required
def admin_debt_pay(did):
    d = db.session.get(Debt, did)
    if d:
        d.status = "paid"
        d.paid_at = datetime.utcnow()
        db.session.commit()
        flash("Погашено", "success")
    return redirect(request.referrer or url_for("admin_debts"))


@app.route("/admin/debts/delete/<int:did>", methods=["POST"])
@admin_required
def admin_debt_delete(did):
    d = db.session.get(Debt, did)
    if d:
        db.session.delete(d)
        db.session.commit()
        flash("Удалено", "success")
    return redirect(url_for("admin_debts"))



@app.route("/health")
def health():
    return jsonify(ok=True, site=SITE_NAME)


@app.route("/api/products", methods=["GET", "POST"])
def api_products():
    if request.method == "POST":
        secret = os.environ.get("API_SECRET", "mir-api-secret-2026")
        key = request.headers.get("X-API-Key") or request.form.get("api_key") or (request.json or {}).get("api_key") if request.is_json else request.form.get("api_key")
        if key != secret:
            return jsonify(ok=False, error="Unauthorized"), 401
        name = (request.form.get("name") or request.form.get("title") or "").strip()
        if not name and request.is_json:
            name = (request.get_json(silent=True) or {}).get("name") or (request.get_json(silent=True) or {}).get("title") or ""
            name = name.strip()
        if not name:
            return jsonify(ok=False, error="name required"), 400
        try:
            price = float(str(request.form.get("price") or (request.get_json(silent=True) or {}).get("price") or 0).replace(",", "."))
        except ValueError:
            price = 0
        img = ""
        f = request.files.get("image")
        if f and f.filename:
            img = save_upload(f)
        prod = Product(name=name[:200], price=price, description=(request.form.get("description") or "")[:2000], image_url=img, in_stock=True)
        db.session.add(prod)
        db.session.commit()
        return jsonify(ok=True, id=prod.id, name=prod.name), 201
    items = []
    for p in Product.query.order_by(Product.created_at.desc()).limit(200).all():
        items.append(
            {
                "id": p.id,
                "name": p.name,
                "title": p.name,
                "price": p.price,
                "description": p.description or "",
                "image_url": p.image_url or "",
                "category": p.category.name if p.category else "",
            }
        )
    return jsonify(ok=True, items=items)


# ─── Init ─────────────────────────────────────────────────
with app.app_context():
    try:
        db.create_all()
        existing = {c.name for c in Category.query.all()}
        for n in DEFAULT_CATEGORIES:
            if n not in existing:
                db.session.add(Category(name=n))
        db.session.commit()
    except Exception as e:
        print("init db", e)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
