from flask import Flask, request, redirect, url_for, flash, session, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==================== MODELS ====================
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), default='https://via.placeholder.com/400x300?text=Product')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Новый')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product')

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, default='')

def get_setting(key, default=''):
    s = Setting.query.filter_by(key=key).first()
    return s.value if s else default

def set_setting(key, value):
    s = Setting.query.filter_by(key=key).first()
    if s:
        s.value = value
    else:
        db.session.add(Setting(key=key, value=value))
    db.session.commit()

# ==================== HELPERS ====================
def get_cart():
    return session.get('cart', {})

def cart_count():
    return sum(get_cart().values())

def cart_total():
    total = 0
    for pid, qty in get_cart().items():
        p = Product.query.get(int(pid))
        if p: total += p.price * qty
    return total

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

ADMIN_PASSWORD = 'admin123'

# ==================== LAYOUT ====================
LAYOUT = '''
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }} — Каталог</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={theme:{extend:{colors:{primary:'#4f46e5',primaryDark:'#4338ca'}}}}</script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>.card:hover{transform:translateY(-3px);box-shadow:0 10px 20px -5px rgba(0,0,0,.12)}.card{transition:.2s}</style>
</head>
<body class="bg-gray-50 min-h-screen flex flex-col">
<nav class="bg-white shadow-sm sticky top-0 z-50">
<div class="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
<a href="/" class="text-xl font-bold text-primary flex items-center gap-2"><i class="fas fa-store"></i> Каталог</a>
<div class="flex items-center gap-3">
<a href="/catalog" class="text-sm text-gray-600 hover:text-primary hidden sm:inline">Каталог</a>
<a href="/cart" class="relative p-2"><i class="fas fa-clipboard-list text-lg text-gray-700"></i>
{% if cart_count %}<span class="absolute -top-0.5 -right-0.5 bg-amber-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">{{ cart_count }}</span>{% endif %}
</a>
<a href="/admin" class="p-2 text-gray-400"><i class="fas fa-user-shield"></i></a>
</div></div></nav>
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}<div class="max-w-6xl mx-auto px-4 mt-3 space-y-1">
{% for cat,msg in messages %}
<div class="px-4 py-2 rounded-lg text-sm {% if cat=='success' %}bg-green-100 text-green-800{% elif cat=='danger' %}bg-red-100 text-red-800{% else %}bg-blue-100 text-blue-800{% endif %}">{{ msg }}</div>
{% endfor %}</div>{% endif %}{% endwith %}
<main class="flex-1">{{ content|safe }}</main>
<footer class="bg-gray-900 text-gray-400 text-center text-sm py-6 mt-12">
<div class="mb-2">© 2026 Каталог · Кыргызстан · Предзаказ</div>
</footer>
</body></html>
'''

def page(title, content, **ctx):
    ctx.update(title=title, content=content, cart_count=cart_count(),
               categories=Category.query.all(), get_flashed_messages=__import__('flask').get_flashed_messages)
    return render_template_string(LAYOUT, **ctx)

# ==================== PUBLIC ====================
@app.route('/')
def index():
    products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    cats = Category.query.all()
    cards = ''
    for p in products:
        cat = f'<span class="text-xs text-primary bg-indigo-50 px-2 py-0.5 rounded-full">{p.category.name}</span>' if p.category else ''
        cards += f'''<div class="card bg-white rounded-2xl overflow-hidden border border-gray-100 shadow-sm">
<a href="/product/{p.id}"><div class="aspect-[4/3] bg-gray-100 overflow-hidden"><img src="{p.image_url}" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x300'"></div></a>
<div class="p-4">{cat}<a href="/product/{p.id}"><h3 class="font-semibold mt-1 line-clamp-2 hover:text-primary">{p.name}</h3></a>
<div class="flex justify-between items-center mt-2"><span class="font-bold">{p.price:,.0f} сом</span>
<form action="/cart/add/{p.id}" method="post"><button class="w-9 h-9 rounded-full bg-primary text-white"><i class="fas fa-plus text-xs"></i></button></form></div></div></div>'''
    if not products:
        cards = '<div class="col-span-full text-center py-16 text-gray-500"><i class="fas fa-box-open text-5xl text-gray-300 mb-3"></i><p class="text-lg font-medium">Каталог пока пуст</p><p class="text-sm">Товары появятся скоро</p></div>'
    cat_links = ''.join(f'<a href="/catalog?category={c.id}" class="bg-white rounded-xl shadow p-3 text-center text-sm font-medium hover:shadow-md transition">{c.name}</a>' for c in cats)
    content = f'''
<section class="bg-gradient-to-br from-indigo-600 to-purple-700 text-white py-16 px-4">
<div class="max-w-6xl mx-auto"><h1 class="text-4xl font-extrabold mb-3">Каталог с предзаказом</h1>
<p class="text-indigo-100 mb-6">Выберите товары и оставьте заявку — мы свяжемся с вами</p>
<a href="/catalog" class="inline-block bg-white text-primary font-semibold px-6 py-3 rounded-full">Смотреть каталог</a></div></section>
{('<div class="max-w-6xl mx-auto px-4 -mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3">'+cat_links+'</div>') if cat_links else ''}
<div class="max-w-6xl mx-auto px-4 py-12"><h2 class="text-2xl font-bold mb-6">Товары</h2>
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">{cards}</div></div>
<div class="bg-white border-t py-12 px-4"><div class="max-w-6xl mx-auto grid md:grid-cols-3 gap-8 text-center">
<div><div class="w-12 h-12 mx-auto mb-3 rounded-xl bg-indigo-50 flex items-center justify-center"><i class="fas fa-search text-primary text-xl"></i></div><h3 class="font-semibold mb-1">1. Выберите</h3><p class="text-sm text-gray-500">Товары из каталога</p></div>
<div><div class="w-12 h-12 mx-auto mb-3 rounded-xl bg-indigo-50 flex items-center justify-center"><i class="fas fa-phone text-primary text-xl"></i></div><h3 class="font-semibold mb-1">2. Оставьте заявку</h3><p class="text-sm text-gray-500">Имя и телефон</p></div>
<div><div class="w-12 h-12 mx-auto mb-3 rounded-xl bg-indigo-50 flex items-center justify-center"><i class="fas fa-comments text-primary text-xl"></i></div><h3 class="font-semibold mb-1">3. Мы свяжемся</h3><p class="text-sm text-gray-500">Уточним детали</p></div>
</div></div>'''
    return page('Главная', content)

@app.route('/catalog')
def catalog():
    q = request.args.get('q', '').strip()
    cat_id = request.args.get('category', type=int)
    sort = request.args.get('sort', 'newest')
    query = Product.query
    if q: query = query.filter(Product.name.ilike(f'%{q}%'))
    if cat_id: query = query.filter(Product.category_id == cat_id)
    if sort == 'price_asc': query = query.order_by(Product.price.asc())
    elif sort == 'price_desc': query = query.order_by(Product.price.desc())
    else: query = query.order_by(Product.created_at.desc())
    products = query.all()
    cats = Category.query.all()
    cat_opts = ''.join(f'<option value="{c.id}" {"selected" if cat_id==c.id else ""}>{c.name}</option>' for c in cats)
    cards = ''
    for p in products:
        cat = f'<span class="text-xs text-primary bg-indigo-50 px-2 py-0.5 rounded-full">{p.category.name}</span>' if p.category else ''
        cards += f'''<div class="card bg-white rounded-2xl overflow-hidden border shadow-sm">
<a href="/product/{p.id}"><div class="aspect-[4/3] bg-gray-100"><img src="{p.image_url}" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x300'"></div></a>
<div class="p-4">{cat}<a href="/product/{p.id}"><h3 class="font-semibold mt-1 hover:text-primary">{p.name}</h3></a>
<div class="flex justify-between items-center mt-2"><span class="font-bold">{p.price:,.0f} сом</span>
<form action="/cart/add/{p.id}" method="post"><button class="w-9 h-9 rounded-full bg-primary text-white"><i class="fas fa-plus text-xs"></i></button></form></div></div></div>'''
    if not products:
        cards = '<div class="col-span-full text-center py-16 text-gray-500">Ничего не найдено</div>'
    content = f'''<div class="max-w-6xl mx-auto px-4 py-8">
<div class="flex flex-col lg:flex-row gap-6">
<aside class="lg:w-56"><div class="bg-white rounded-2xl border p-4 sticky top-20">
<form method="get" class="space-y-3">
<input name="q" value="{q}" placeholder="Поиск..." class="w-full border rounded-lg px-3 py-2 text-sm">
<select name="category" class="w-full border rounded-lg px-3 py-2 text-sm"><option value="">Все категории</option>{cat_opts}</select>
<select name="sort" class="w-full border rounded-lg px-3 py-2 text-sm">
<option value="newest" {"selected" if sort=="newest" else ""}>Новые</option>
<option value="price_asc" {"selected" if sort=="price_asc" else ""}>Цена ↑</option>
<option value="price_desc" {"selected" if sort=="price_desc" else ""}>Цена ↓</option>
</select>
<button class="w-full bg-primary text-white py-2 rounded-lg text-sm font-medium">Применить</button>
</form></div></aside>
<div class="flex-1"><h1 class="text-2xl font-bold mb-4">Каталог <span class="text-sm font-normal text-gray-500">({len(products)})</span></h1>
<div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">{cards}</div></div></div></div>'''
    return page('Каталог', content)

@app.route('/product/<int:pid>')
def product_detail(pid):
    p = Product.query.get_or_404(pid)
    content = f'''<div class="max-w-6xl mx-auto px-4 py-8">
<div class="grid md:grid-cols-2 gap-8">
<div class="bg-white rounded-2xl overflow-hidden border"><img src="{p.image_url}" class="w-full aspect-square object-cover" onerror="this.src='https://via.placeholder.com/600'"></div>
<div>
{"<span class='text-sm text-primary bg-indigo-50 px-3 py-1 rounded-full'>"+p.category.name+"</span>" if p.category else ""}
<h1 class="text-3xl font-bold mt-3 mb-3">{p.name}</h1>
<div class="text-3xl font-extrabold text-primary mb-4">{p.price:,.0f} сом</div>
<p class="text-gray-600 mb-6">{p.description or "Описание отсутствует"}</p>
<form action="/cart/add/{p.id}" method="post" class="flex gap-3 items-center">
<input type="number" name="quantity" value="1" min="1" class="w-20 border rounded-lg px-3 py-2 text-center">
<button class="bg-primary text-white font-semibold px-8 py-3 rounded-xl hover:bg-primaryDark">В предзаказ</button>
</form></div></div></div>'''
    return page(p.name, content)

@app.route('/cart')
def cart():
    items_html = ''
    total = 0
    for pid, qty in get_cart().items():
        p = Product.query.get(int(pid))
        if not p: continue
        sub = p.price * qty
        total += sub
        items_html += f'''<div class="p-4 flex flex-col sm:flex-row gap-4 items-center border-b">
<img src="{p.image_url}" class="w-20 h-20 object-cover rounded-xl" onerror="this.src='https://via.placeholder.com/80'">
<div class="flex-1"><a href="/product/{p.id}" class="font-semibold hover:text-primary">{p.name}</a>
<p class="text-sm text-gray-500">{p.price:,.0f} сом</p></div>
<form action="/cart/update/{p.id}" method="post" class="flex gap-2 items-center">
<input type="number" name="quantity" value="{qty}" min="0" class="w-16 border rounded px-2 py-1 text-center text-sm">
<button class="text-sm text-primary">OK</button></form>
<div class="font-bold w-24 text-right">{sub:,.0f} сом</div>
<a href="/cart/remove/{p.id}" class="text-red-500 text-sm">✕</a></div>'''
    if items_html:
        content = f'''<div class="max-w-3xl mx-auto px-4 py-8"><h1 class="text-2xl font-bold mb-6">Предзаказ</h1>
<div class="bg-white rounded-2xl border overflow-hidden">{items_html}
<div class="p-5 bg-gray-50 flex flex-col sm:flex-row justify-between items-center gap-3">
<a href="/catalog" class="text-primary text-sm">← Продолжить выбор</a>
<span class="text-xl font-bold">{total:,.0f} сом</span>
<a href="/checkout" class="bg-primary text-white px-6 py-2.5 rounded-xl font-semibold">Оставить предзаказ</a>
</div></div></div>'''
    else:
        content = '''<div class="max-w-3xl mx-auto px-4 py-16 text-center"><i class="fas fa-clipboard-list text-5xl text-gray-300 mb-4"></i>
<h2 class="text-xl font-semibold mb-2">Предзаказ пуст</h2><a href="/catalog" class="inline-block mt-4 bg-primary text-white px-6 py-3 rounded-xl">В каталог</a></div>'''
    return page('Предзаказ', content)

@app.route('/cart/add/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    p = Product.query.get_or_404(pid)
    qty = int(request.form.get('quantity', 1))
    cart = get_cart()
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session['cart'] = cart
    flash(f'«{p.name}» добавлен в предзаказ', 'success')
    return redirect(request.referrer or url_for('catalog'))

@app.route('/cart/update/<int:pid>', methods=['POST'])
def update_cart(pid):
    qty = int(request.form.get('quantity', 1))
    cart = get_cart()
    if qty <= 0: cart.pop(str(pid), None)
    else: cart[str(pid)] = qty
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:pid>')
def remove_from_cart(pid):
    cart = get_cart()
    cart.pop(str(pid), None)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not get_cart():
        flash('Предзаказ пуст', 'warning')
        return redirect(url_for('catalog'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        if not name or not phone:
            flash('Укажите имя и телефон', 'danger')
            return redirect(url_for('checkout'))
        order = Order(customer_name=name, customer_phone=phone, total_price=cart_total())
        db.session.add(order)
        db.session.flush()
        for pid, qty in get_cart().items():
            p = Product.query.get(int(pid))
            if p:
                db.session.add(OrderItem(order_id=order.id, product_id=p.id, quantity=qty, price=p.price))
        db.session.commit()
        session['cart'] = {}
        flash(f'Предзаказ #{order.id} принят! Мы свяжемся с вами.', 'success')
        return redirect(url_for('index'))
    items = ''
    total = 0
    for pid, qty in get_cart().items():
        p = Product.query.get(int(pid))
        if p:
            sub = p.price * qty
            total += sub
            items += f'<div class="flex justify-between text-sm"><span>{p.name} × {qty}</span><span>{sub:,.0f} сом</span></div>'
    phones = get_setting('phones', '')
    rekvizity = get_setting('rekvizity', '')
    rekvizity_image = get_setting('rekvizity_image', '')
    phones_html = ''
    if phones:
        phones_html = '<div class="mt-4 pt-4 border-t"><h4 class="font-semibold text-sm mb-2">Связаться с нами</h4>' + ''.join(f'<a href="tel:{line.strip()}" class="block text-primary text-sm mb-1"><i class="fas fa-phone mr-1"></i> {line.strip()}</a>' for line in phones.strip().splitlines() if line.strip()) + '</div>'
    rekv_html = ''
    if rekvizity or rekvizity_image:
        rekv_html = '<div class="mt-4 pt-4 border-t"><h4 class="font-semibold text-sm mb-2">Реквизиты для оплаты</h4>'
        if rekvizity:
            rekv_html += f'<pre class="text-xs text-gray-600 whitespace-pre-wrap bg-gray-50 p-3 rounded-lg">{rekvizity}</pre>'
        if rekvizity_image:
            rekv_html += f'<img src="{rekvizity_image}" class="mt-2 max-h-40 rounded-lg border" onerror="this.style.display=\'none\'">'
        rekv_html += '</div>'
    content = f'''<div class="max-w-3xl mx-auto px-4 py-8"><h1 class="text-2xl font-bold mb-6">Оставить предзаказ</h1>
<div class="grid md:grid-cols-5 gap-6">
<div class="md:col-span-3 bg-white rounded-2xl border p-6">
<p class="text-sm text-gray-500 mb-4">Укажите имя и телефон — мы свяжемся с вами</p>
<form method="post" class="space-y-4">
<div><label class="text-sm font-medium">Имя *</label><input name="name" required class="w-full border rounded-xl px-4 py-2.5 mt-1" placeholder="Как к вам обращаться"></div>
<div><label class="text-sm font-medium">Телефон *</label><input name="phone" required class="w-full border rounded-xl px-4 py-2.5 mt-1" placeholder="+996 XXX XXX XXX"></div>
<button class="w-full bg-primary text-white font-semibold py-3 rounded-xl mt-2">Отправить предзаказ</button>
</form></div>
<div class="md:col-span-2 bg-white rounded-2xl border p-6 h-fit">
<h3 class="font-semibold mb-3">Состав</h3><div class="space-y-2 mb-4">{items}</div>
<div class="border-t pt-3 flex justify-between font-bold"><span>Итого</span><span class="text-primary">{total:,.0f} сом</span></div>
{phones_html}{rekv_html}
</div></div></div>'''
    return page('Предзаказ', content)

# ==================== ADMIN ====================
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin'): return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Неверный пароль', 'danger')
    content = '''<div class="min-h-[60vh] flex items-center justify-center px-4">
<div class="bg-white rounded-2xl border shadow p-8 w-full max-w-sm text-center">
<div class="w-14 h-14 mx-auto mb-4 rounded-2xl bg-indigo-50 flex items-center justify-center"><i class="fas fa-user-shield text-2xl text-primary"></i></div>
<h1 class="text-xl font-bold mb-1">Админ-панель</h1>
<p class="text-sm text-gray-500 mb-5">Введите пароль</p>
<form method="post"><input type="password" name="password" required autofocus class="w-full border rounded-xl px-4 py-2.5 mb-3" placeholder="••••••">
<button class="w-full bg-primary text-white font-semibold py-2.5 rounded-xl">Войти</button></form>
<p class="text-xs text-gray-400 mt-3">Пароль: admin123</p></div></div>'''
    return page('Вход', content)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    pc, oc, nc = Product.query.count(), Order.query.count(), Order.query.filter_by(status='Новый').count()
    orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    rows = ''.join(f'<tr class="border-t"><td class="px-4 py-2"><a href="/admin/orders/{o.id}" class="text-primary">#{o.id}</a></td><td class="px-4 py-2">{o.customer_name}</td><td class="px-4 py-2">{o.total_price:,.0f} сом</td><td class="px-4 py-2"><span class="text-xs px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">{o.status}</span></td><td class="px-4 py-2 text-gray-500 text-sm">{o.created_at.strftime("%d.%m %H:%M")}</td></tr>' for o in orders)
    content = f'''<div class="max-w-6xl mx-auto px-4 py-8">
<div class="flex gap-4 mb-6 flex-wrap">
<a href="/admin/dashboard" class="text-sm font-medium text-primary">Дашборд</a>
<a href="/admin/products" class="text-sm text-gray-600 hover:text-primary">Товары</a>
<a href="/admin/orders" class="text-sm text-gray-600 hover:text-primary">Заявки</a>
<a href="/admin/categories" class="text-sm text-gray-600 hover:text-primary">Категории</a>
<a href="/admin/settings" class="text-sm text-gray-600 hover:text-primary">Реквизиты</a>
<a href="/admin/logout" class="text-sm text-red-500 ml-auto">Выйти</a></div>
<h1 class="text-2xl font-bold mb-6">Дашборд</h1>
<div class="grid grid-cols-3 gap-4 mb-8">
<div class="bg-white rounded-2xl border p-5 text-center"><div class="text-2xl font-bold">{pc}</div><div class="text-sm text-gray-500">Товаров</div></div>
<div class="bg-white rounded-2xl border p-5 text-center"><div class="text-2xl font-bold">{oc}</div><div class="text-sm text-gray-500">Заявок</div></div>
<div class="bg-white rounded-2xl border p-5 text-center"><div class="text-2xl font-bold text-amber-600">{nc}</div><div class="text-sm text-gray-500">Новых</div></div>
</div>
<div class="bg-white rounded-2xl border overflow-hidden"><div class="px-4 py-3 font-semibold border-b">Последние заявки</div>
<table class="w-full text-sm"><thead class="bg-gray-50 text-gray-500"><tr><th class="text-left px-4 py-2">#</th><th class="text-left px-4 py-2">Клиент</th><th class="text-left px-4 py-2">Сумма</th><th class="text-left px-4 py-2">Статус</th><th class="text-left px-4 py-2">Дата</th></tr></thead>
<tbody>{rows if rows else '<tr><td colspan="5" class="px-4 py-8 text-center text-gray-400">Пока нет заявок</td></tr>'}</tbody></table></div></div>'''
    return page('Админ', content)

@app.route('/admin/products')
@admin_required
def admin_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    rows = ''.join(f'''<tr class="border-t"><td class="px-4 py-3"><div class="flex items-center gap-3"><img src="{p.image_url}" class="w-10 h-10 rounded object-cover" onerror="this.src='https://via.placeholder.com/40'"><span class="font-medium">{p.name}</span></div></td>
<td class="px-4 py-3 text-gray-500">{p.category.name if p.category else "—"}</td>
<td class="px-4 py-3 font-medium">{p.price:,.0f} сом</td>
<td class="px-4 py-3 text-right"><a href="/admin/products/edit/{p.id}" class="text-primary text-sm mr-2">Изменить</a>
<form action="/admin/products/delete/{p.id}" method="post" class="inline" onsubmit="return confirm('Удалить?')"><button class="text-red-500 text-sm">Удалить</button></form></td></tr>''' for p in products)
    content = f'''<div class="max-w-6xl mx-auto px-4 py-8">
<div class="flex gap-4 mb-6 flex-wrap">
<a href="/admin/dashboard" class="text-sm text-gray-600 hover:text-primary">Дашборд</a>
<a href="/admin/products" class="text-sm font-medium text-primary">Товары</a>
<a href="/admin/orders" class="text-sm text-gray-600 hover:text-primary">Заявки</a>
<a href="/admin/categories" class="text-sm text-gray-600 hover:text-primary">Категории</a>
<a href="/admin/settings" class="text-sm text-gray-600 hover:text-primary">Реквизиты</a>
<a href="/admin/logout" class="text-sm text-red-500 ml-auto">Выйти</a></div>
<div class="flex justify-between items-center mb-6"><h1 class="text-2xl font-bold">Товары</h1>
<a href="/admin/products/add" class="bg-primary text-white px-4 py-2 rounded-xl text-sm font-medium">+ Добавить</a></div>
<div class="bg-white rounded-2xl border overflow-hidden"><table class="w-full text-sm">
<thead class="bg-gray-50 text-gray-500"><tr><th class="text-left px-4 py-2">Товар</th><th class="text-left px-4 py-2">Категория</th><th class="text-left px-4 py-2">Цена</th><th class="text-right px-4 py-2">Действия</th></tr></thead>
<tbody>{rows if rows else '<tr><td colspan="4" class="px-4 py-12 text-center text-gray-400">Нет товаров. Добавьте первый!</td></tr>'}</tbody></table></div></div>'''
    return page('Товары', content)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@app.route('/admin/products/edit/<int:pid>', methods=['GET', 'POST'])
@admin_required
def admin_product_form(pid=None):
    p = Product.query.get(pid) if pid else None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = float(request.form.get('price', 0))
        if not name or price <= 0:
            flash('Название и цена обязательны', 'danger')
            return redirect(request.url)
        if p:
            p.name, p.description, p.price = name, request.form.get('description', ''), price
            p.image_url = request.form.get('image_url', '') or p.image_url
            p.category_id = request.form.get('category_id', type=int) or None
        else:
            p = Product(name=name, description=request.form.get('description', ''), price=price,
                        image_url=request.form.get('image_url', '') or 'https://via.placeholder.com/400x300?text=Product',
                        category_id=request.form.get('category_id', type=int) or None)
            db.session.add(p)
        db.session.commit()
        flash('Сохранено', 'success')
        return redirect(url_for('admin_products'))
    cats = Category.query.all()
    cat_opts = ''.join(f'<option value="{c.id}" {"selected" if p and p.category_id==c.id else ""}>{c.name}</option>' for c in cats)
    content = f'''<div class="max-w-xl mx-auto px-4 py-8">
<a href="/admin/products" class="text-sm text-primary">← Назад</a>
<h1 class="text-2xl font-bold mt-2 mb-6">{"Редактировать" if p else "Добавить"} товар</h1>
<form method="post" class="bg-white rounded-2xl border p-6 space-y-4">
<div><label class="text-sm font-medium">Название *</label><input name="name" required value="{p.name if p else ""}" class="w-full border rounded-xl px-4 py-2.5 mt-1"></div>
<div><label class="text-sm font-medium">Описание</label><textarea name="description" rows="3" class="w-full border rounded-xl px-4 py-2.5 mt-1">{p.description if p else ""}</textarea></div>
<div><label class="text-sm font-medium">Цена, сом *</label><input name="price" type="number" step="0.01" required value="{p.price if p else ""}" class="w-full border rounded-xl px-4 py-2.5 mt-1"></div>
<div><label class="text-sm font-medium">Категория</label><select name="category_id" class="w-full border rounded-xl px-4 py-2.5 mt-1"><option value="">Без категории</option>{cat_opts}</select></div>
<div><label class="text-sm font-medium">URL картинки</label><input name="image_url" value="{p.image_url if p else ""}" class="w-full border rounded-xl px-4 py-2.5 mt-1" placeholder="https://..."></div>
<button class="bg-primary text-white font-semibold px-6 py-2.5 rounded-xl">Сохранить</button>
</form></div>'''
    return page('Товар', content)

@app.route('/admin/products/delete/<int:pid>', methods=['POST'])
@admin_required
def admin_delete_product(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash('Удалено', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    status = request.args.get('status')
    q = Order.query.order_by(Order.created_at.desc())
    if status: q = q.filter_by(status=status)
    orders = q.all()
    filters = ''.join(f'<a href="/admin/orders?status={s}" class="px-3 py-1 rounded-lg text-sm {"bg-primary text-white" if status==s else "bg-gray-100"}">{s}</a>' for s in ['Новый','В обработке','Готов','Выдан','Отменён'])
    rows = ''.join(f'<tr class="border-t"><td class="px-4 py-2"><a href="/admin/orders/{o.id}" class="text-primary">#{o.id}</a></td><td class="px-4 py-2">{o.customer_name}</td><td class="px-4 py-2">{o.customer_phone}</td><td class="px-4 py-2">{o.total_price:,.0f} сом</td><td class="px-4 py-2"><span class="text-xs px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">{o.status}</span></td><td class="px-4 py-2 text-gray-500 text-sm">{o.created_at.strftime("%d.%m.%Y %H:%M")}</td></tr>' for o in orders)
    content = f'''<div class="max-w-6xl mx-auto px-4 py-8">
<div class="flex gap-4 mb-6 flex-wrap">
<a href="/admin/dashboard" class="text-sm text-gray-600 hover:text-primary">Дашборд</a>
<a href="/admin/products" class="text-sm text-gray-600 hover:text-primary">Товары</a>
<a href="/admin/orders" class="text-sm font-medium text-primary">Заявки</a>
<a href="/admin/categories" class="text-sm text-gray-600 hover:text-primary">Категории</a>
<a href="/admin/settings" class="text-sm text-gray-600 hover:text-primary">Реквизиты</a>
<a href="/admin/logout" class="text-sm text-red-500 ml-auto">Выйти</a></div>
<div class="flex justify-between items-center mb-4 flex-wrap gap-2"><h1 class="text-2xl font-bold">Заявки</h1>
<div class="flex gap-1 flex-wrap"><a href="/admin/orders" class="px-3 py-1 rounded-lg text-sm {"bg-primary text-white" if not status else "bg-gray-100"}">Все</a>{filters}</div></div>
<div class="bg-white rounded-2xl border overflow-hidden"><table class="w-full text-sm">
<thead class="bg-gray-50 text-gray-500"><tr><th class="text-left px-4 py-2">#</th><th class="text-left px-4 py-2">Клиент</th><th class="text-left px-4 py-2">Телефон</th><th class="text-left px-4 py-2">Сумма</th><th class="text-left px-4 py-2">Статус</th><th class="text-left px-4 py-2">Дата</th></tr></thead>
<tbody>{rows if rows else '<tr><td colspan="6" class="px-4 py-12 text-center text-gray-400">Нет заявок</td></tr>'}</tbody></table></div></div>'''
    return page('Заявки', content)

@app.route('/admin/orders/<int:oid>')
@admin_required
def admin_order_detail(oid):
    o = Order.query.get_or_404(oid)
    items = ''.join(f'<div class="flex justify-between py-2 border-b text-sm"><span>{i.product.name if i.product else "?"} × {i.quantity}</span><span>{i.quantity*i.price:,.0f} сом</span></div>' for i in o.items)
    opts = ''.join(f'<option value="{s}" {"selected" if o.status==s else ""}>{s}</option>' for s in ['Новый','В обработке','Готов','Выдан','Отменён'])
    content = f'''<div class="max-w-3xl mx-auto px-4 py-8">
<a href="/admin/orders" class="text-sm text-primary">← Назад</a>
<h1 class="text-2xl font-bold mt-2 mb-6">Заявка #{o.id}</h1>
<div class="grid md:grid-cols-3 gap-6">
<div class="md:col-span-2 bg-white rounded-2xl border p-5">
<h3 class="font-semibold mb-3">Состав</h3>{items}
<div class="flex justify-between font-bold pt-3 mt-2"><span>Итого</span><span>{o.total_price:,.0f} сом</span></div>
</div>
<div class="space-y-4">
<div class="bg-white rounded-2xl border p-5 text-sm space-y-2">
<div><span class="text-gray-500">Имя:</span> <strong>{o.customer_name}</strong></div>
<div><span class="text-gray-500">Телефон:</span> <strong>{o.customer_phone}</strong></div>
<div><span class="text-gray-500">Дата:</span> {o.created_at.strftime("%d.%m.%Y %H:%M")}</div>
</div>
<div class="bg-white rounded-2xl border p-5">
<form action="/admin/orders/{o.id}/status" method="post">
<select name="status" class="w-full border rounded-xl px-3 py-2 text-sm mb-3">{opts}</select>
<button class="w-full bg-primary text-white py-2 rounded-xl text-sm font-medium">Обновить статус</button>
</form></div></div></div></div>'''
    return page(f'Заявка #{oid}', content)

@app.route('/admin/orders/<int:oid>/status', methods=['POST'])
@admin_required
def admin_update_status(oid):
    o = Order.query.get_or_404(oid)
    s = request.form.get('status')
    if s in ['Новый','В обработке','Готов','Выдан','Отменён']:
        o.status = s
        db.session.commit()
        flash('Статус обновлён', 'success')
    return redirect(url_for('admin_order_detail', oid=oid))

@app.route('/admin/categories', methods=['GET', 'POST'])
@admin_required
def admin_categories():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name and not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
            db.session.commit()
            flash('Добавлено', 'success')
        return redirect(url_for('admin_categories'))
    cats = Category.query.all()
    rows = ''.join(
        f'<div class="flex justify-between items-center px-4 py-3 border-b"><span>{c.name}</span>'
        f'<form action="/admin/categories/delete/{c.id}" method="post" onsubmit="return confirm(\'Удалить?\')">'
        f'<button class="text-red-500 text-sm">Удалить</button></form></div>'
        for c in cats
    )
    content = f'''<div class="max-w-xl mx-auto px-4 py-8">
<div class="flex gap-4 mb-6 flex-wrap">
<a href="/admin/dashboard" class="text-sm text-gray-600 hover:text-primary">Дашборд</a>
<a href="/admin/products" class="text-sm text-gray-600 hover:text-primary">Товары</a>
<a href="/admin/orders" class="text-sm text-gray-600 hover:text-primary">Заявки</a>
<a href="/admin/categories" class="text-sm font-medium text-primary">Категории</a>
<a href="/admin/settings" class="text-sm text-gray-600 hover:text-primary">Реквизиты</a>
<a href="/admin/logout" class="text-sm text-red-500 ml-auto">Выйти</a></div>
<h1 class="text-2xl font-bold mb-6">Категории</h1>
<form method="post" class="flex gap-2 mb-6"><input name="name" required placeholder="Новая категория" class="flex-1 border rounded-xl px-4 py-2.5">
<button class="bg-primary text-white px-5 py-2.5 rounded-xl font-medium">Добавить</button></form>
<div class="bg-white rounded-2xl border overflow-hidden">{rows if rows else '<p class="p-8 text-center text-gray-400">Нет категорий</p>'}</div></div>'''
    return page('Категории', content)

@app.route('/admin/categories/delete/<int:cid>', methods=['POST'])
@admin_required
def admin_delete_category(cid):
    c = Category.query.get_or_404(cid)
    db.session.delete(c)
    db.session.commit()
    flash('Удалено', 'success')
    return redirect(url_for('admin_categories'))


@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    if request.method == 'POST':
        set_setting('phones', request.form.get('phones', '').strip())
        set_setting('rekvizity', request.form.get('rekvizity', '').strip())
        set_setting('rekvizity_image', request.form.get('rekvizity_image', '').strip())
        flash('Настройки сохранены', 'success')
        return redirect(url_for('admin_settings'))
    phones = get_setting('phones', '+996 XXX XXX XXX')
    rekvizity = get_setting('rekvizity', '')
    rekvizity_image = get_setting('rekvizity_image', '')
    content = f"""<div class="max-w-xl mx-auto px-4 py-8">
<div class="flex gap-4 mb-6 flex-wrap">
<a href="/admin/dashboard" class="text-sm text-gray-600 hover:text-primary">Дашборд</a>
<a href="/admin/products" class="text-sm text-gray-600 hover:text-primary">Товары</a>
<a href="/admin/orders" class="text-sm text-gray-600 hover:text-primary">Заявки</a>
<a href="/admin/categories" class="text-sm text-gray-600 hover:text-primary">Категории</a>
<a href="/admin/settings" class="text-sm font-medium text-primary">Реквизиты</a>
<a href="/admin/logout" class="text-sm text-red-500 ml-auto">Выйти</a></div>
<h1 class="text-2xl font-bold mb-6">Реквизиты и контакты</h1>
<form method="post" class="bg-white rounded-2xl border p-6 space-y-5">
<div>
<label class="text-sm font-medium">Номера для связи</label>
<p class="text-xs text-gray-400 mb-1">Каждый номер с новой строки</p>
<textarea name="phones" rows="3" class="w-full border rounded-xl px-4 py-2.5 mt-1" placeholder="+996 700 123 456&#10;+996 555 987 654">{phones}</textarea>
</div>
<div>
<label class="text-sm font-medium">Реквизиты (текст)</label>
<p class="text-xs text-gray-400 mb-1">Банк, счёт, ФИО, ИНН и т.д.</p>
<textarea name="rekvizity" rows="5" class="w-full border rounded-xl px-4 py-2.5 mt-1" placeholder="Банк: ...&#10;Счёт: ...&#10;ФИО: ...">{rekvizity}</textarea>
</div>
<div>
<label class="text-sm font-medium">Фото / QR реквизитов (URL картинки)</label>
<input name="rekvizity_image" value="{rekvizity_image}" class="w-full border rounded-xl px-4 py-2.5 mt-1" placeholder="https://...">
{"<img src='"+rekvizity_image+"' class='mt-3 max-h-48 rounded-xl border' onerror=\"this.style.display='none'\">" if rekvizity_image else ""}
</div>
<button class="bg-primary text-white font-semibold px-6 py-2.5 rounded-xl">Сохранить</button>
</form></div>"""
    return page('Реквизиты', content)


# ==================== INIT ====================
with app.app_context():
    db.create_all()
    if Category.query.count() == 0:
        for n in ['Электроника', 'Одежда', 'Аксессуары', 'Другое']:
            db.session.add(Category(name=n))
        db.session.commit()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
