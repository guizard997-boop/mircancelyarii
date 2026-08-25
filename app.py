from flask import Flask, request, redirect, url_for, flash, session, render_template_string, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import os, uuid, json, requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mir-kancelyarii-secret-key-2026-kg')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def save_upload(file_storage):
    if not file_storage or not file_storage.filename or not allowed_file(file_storage.filename):
        return None
    ext = file_storage.filename.rsplit('.', 1)[1].lower()
    name = f'{uuid.uuid4().hex}.{ext}'
    file_storage.save(os.path.join(UPLOAD_FOLDER, name))
    return f'/uploads/{name}'

# ==================== MODELS ====================
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
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
    if s: s.value = value
    else: db.session.add(Setting(key=key, value=value))
    db.session.commit()

class BotState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(50), unique=True, nullable=False)
    step = db.Column(db.String(50), default='idle')
    draft_name = db.Column(db.String(300), default='')
    draft_image = db.Column(db.String(500), default='')

# ==================== HELPERS ====================
def get_cart():
    return session.get('cart', {})

def cart_count():
    return sum(get_cart().values())

def cart_total():
    t = 0
    for pid, qty in get_cart().items():
        p = Product.query.get(int(pid))
        if p: t += p.price * qty
    return t

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ==================== BOT API ENDPOINT ====================
@app.route('/api/products', methods=['POST'])
def api_add_product():
    try:
        title = request.form.get('title')
        description = request.form.get('description', '')
        
        if not title:
            return jsonify({"error": "Название обязательно"}), 400

        image_url = 'https://via.placeholder.com/400x300?text=Product'
        if 'image' in request.files:
            uploaded_file = request.files['image']
            saved_path = save_upload(uploaded_file)
            if saved_path:
                image_url = saved_path

        new_product = Product(
            name=title,
            description=description,
            price=0.0,
            image_url=image_url
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Товар успешно создан!",
            "product_id": new_product.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== LAYOUT ====================
LAYOUT = '''
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ title }} — Мир канцелярии</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={theme:{extend:{colors:{brand:'#6C5CE7',brand2:'#A66CFF',accent:'#FF6B35',soft:'#F8F7FF'}}}}</script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
body{font-family:'Nunito',system-ui,sans-serif}
.card{transition:.25s}.card:hover{transform:translateY(-4px);box-shadow:0 12px 28px -8px rgba(108,92,231,.2)}
.hero-grad{background:linear-gradient(135deg,#f8f7ff 0%,#fff 50%,#fff5f0 100%)}
.btn-grad{background:linear-gradient(135deg,#6C5CE7,#A66CFF)}
.btn-orange{background:linear-gradient(135deg,#FF6B35,#FF8F66)}
</style>
</head>
<body class="bg-white min-h-screen flex flex-col">
<!-- HEADER -->
<header class="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-gray-100 shadow-sm">
<div class="max-w-7xl mx-auto px-4 h-16 flex items-center gap-3">
  <a href="/" class="flex items-center gap-2 flex-shrink-0">
    <div class="w-10 h-10 rounded-xl btn-grad flex items-center justify-center text-white font-extrabold text-lg">М</div>
    <div class="hidden sm:block leading-tight">
      <div class="font-extrabold text-brand text-sm">МИР</div>
      <div class="text-[10px] text-gray-500 -mt-0.5 tracking-wide">КАНЦЕЛЯРИИ</div>
    </div>
  </a>
  <a href="/catalog" class="hidden md:inline-flex items-center gap-1.5 bg-brand text-white text-sm font-semibold px-4 py-2 rounded-xl hover:opacity-90 transition">
    <i class="fas fa-th-large"></i> Каталог
  </a>
  <form action="/catalog" method="get" class="flex-1 max-w-xl">
    <div class="relative">
      <input type="text" name="q" value="{{ request.args.get('q','') }}" placeholder="Поиск товаров..."
        class="w-full pl-4 pr-10 py-2.5 bg-gray-50 border border-gray-200 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-brand/40 focus:border-brand">
      <button type="submit" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-brand"><i class="fas fa-search"></i></button>
    </div>
  </form>
  <a href="/cart" class="relative p-2 rounded-xl hover:bg-soft transition" title="Предзаказ">
    <i class="fas fa-shopping-bag text-xl text-gray-600"></i>
    {% if cart_count %}<span class="absolute -top-0.5 -right-0.5 bg-accent text-white text-[10px] font-bold rounded-full h-5 w-5 flex items-center justify-center">{{ cart_count }}</span>{% endif %}
  </a>
</div>
</header>

{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}<div class="max-w-7xl mx-auto px-4 mt-3 space-y-1">
{% for cat,msg in messages %}
<div class="px-4 py-2.5 rounded-xl text-sm font-medium {% if cat=='success' %}bg-green-50 text-green-700 border border-green-100{% elif cat=='danger' %}bg-red-50 text-red-700 border border-red-100{% else %}bg-blue-50 text-blue-700 border border-blue-100{% endif %}">{{ msg }}</div>
{% endfor %}</div>{% endif %}{% endwith %}

<main class="flex-1">{{ content|safe }}</main>

<footer class="bg-gray-900 text-gray-400 mt-16">
<div class="max-w-7xl mx-auto px-4 py-10 grid sm:grid-cols-3 gap-8 text-sm">
  <div>
    <div class="flex items-center gap-2 mb-3">
      <div class="w-8 h-8 rounded-lg btn-grad flex items-center justify-center text-white font-bold">М</div>
      <span class="text-white font-bold">Мир канцелярии</span>
    </div>
    <p class="text-gray-500">Всё для учёбы, творчества и вдохновения. Предзаказ по Кыргызстану.</p>
  </div>
  <div>
    <h4 class="text-white font-semibold mb-3">Каталог</h4>
    <ul class="space-y-1">
    {% for c in categories %}
    <li><a href="/catalog?category={{ c.id }}" class="hover:text-white transition">{{ c.name }}</a></li>
    {% endfor %}
    </ul>
  </div>
  <div>
    <h4 class="text-white font-semibold mb-3">Контакты</h4>
    <p class="text-gray-500">Оставьте предзаказ — мы свяжемся с вами</p>
  </div>
</div>
<div class="border-t border-gray-800 text-center text-xs text-gray-600 py-4">© 2026 Мир канцелярии · Кыргызстан</div>
</footer>
</body></html>
'''

def page(title, content):
    from flask import get_flashed_messages, request as req
    return render_template_string(LAYOUT, title=title, content=content, cart_count=cart_count(),
                                 categories=Category.query.all(), get_flashed_messages=get_flashed_messages, request=req)

def product_card(p):
    cat = f'<span class="text-[10px] font-semibold text-brand bg-soft px-2 py-0.5 rounded-full">{p.category.name}</span>' if p.category else ''
    return f'''<div class="card bg-white rounded-2xl overflow-hidden border border-gray-100 shadow-sm">
<a href="/product/{p.id}"><div class="aspect-square bg-gray-50 overflow-hidden">
<img src="{p.image_url}" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400?text=Фото'"></div></a>
<div class="p-3.5">{cat}
<a href="/product/{p.id}"><h3 class="font-bold text-gray-800 mt-1.5 text-sm line-clamp-2 hover:text-brand transition">{p.name}</h3></a>
<div class="flex justify-between items-center mt-2.5">
<span class="font-extrabold text-brand">{p.price:,.0f} <span class="text-xs font-semibold">сом</span></span>
<form action="/cart/add/{p.id}" method="post">
<button class="w-9 h-9 rounded-xl btn-grad text-white flex items-center justify-center shadow-md hover:opacity-90"><i class="fas fa-plus text-xs"></i></button>
</form></div></div></div>'''

# ==================== PUBLIC ROUTES ====================
@app.route('/')
def index():
    products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    cats = Category.query.all()
    cat_colors = ['bg-violet-50','bg-pink-50','bg-sky-50','bg-amber-50','bg-emerald-50','bg-rose-50']
    cat_html = ''
    for i, c in enumerate(cats):
        cnt = Product.query.filter_by(category_id=c.id).count()
        cat_html += f'''<a href="/catalog?category={c.id}" class="card {cat_colors[i%len(cat_colors)]} rounded-2xl p-5 text-center border border-white/50">
<div class="w-14 h-14 mx-auto mb-3 rounded-2xl bg-white shadow-sm flex items-center justify-center text-2xl">📦</div>
<div class="font-bold text-gray-800 text-sm">{c.name}</div>
<div class="text-xs text-gray-400 mt-1">{cnt} товар(ов)</div></a>'''
    cards = ''.join(product_card(p) for p in products) or '<div class="col-span-full text-center py-16 text-gray-400"><i class="fas fa-box-open text-5xl mb-3"></i><p class="font-semibold text-lg">Каталог пока пуст</p><p class="text-sm">Товары появятся скоро</p></div>'
    content = f'''
<section class="hero-grad overflow-hidden">
<div class="max-w-7xl mx-auto px-4 py-12 md:py-20 grid md:grid-cols-2 gap-8 items-center">
  <div>
    <h1 class="text-3xl sm:text-4xl lg:text-5xl font-extrabold leading-tight mb-4">
      Мир канцелярии —<br>
      <span class="text-brand">всё для учёбы,</span><br>
      <span class="text-brand2">творчества</span><br>
      <span class="text-accent">и вдохновения!</span>
    </h1>
    <p class="text-gray-500 mb-6 max-w-md">Качественные товары для школы, офиса и творчества. Оформите предзаказ — мы свяжемся с вами.</p>
    <a href="/catalog" class="inline-flex items-center gap-2 btn-orange text-white font-bold px-6 py-3 rounded-full shadow-lg hover:opacity-90 transition">
      Перейти в каталог <i class="fas fa-arrow-right text-sm"></i>
    </a>
  </div>
  <div class="hidden md:flex justify-center">
    <div class="relative w-80 h-80">
      <div class="absolute inset-0 bg-gradient-to-br from-violet-200 to-orange-100 rounded-full blur-2xl opacity-60"></div>
      <div class="relative text-center text-8xl leading-none pt-12">✏️📚🎨</div>
    </div>
  </div>
</div>
</section>

<div class="max-w-7xl mx-auto px-4 -mt-6 relative z-10">
<div class="bg-white rounded-2xl shadow-lg border border-gray-100 grid grid-cols-2 md:grid-cols-4 divide-x divide-gray-100 overflow-hidden">
  <div class="p-4 text-center"><div class="text-brand text-xl mb-1"><i class="fas fa-th"></i></div><div class="font-bold text-sm">Широкий ассортимент</div><div class="text-xs text-gray-400">Много товаров</div></div>
  <div class="p-4 text-center"><div class="text-amber-500 text-xl mb-1"><i class="fas fa-star"></i></div><div class="font-bold text-sm">Качество</div><div class="text-xs text-gray-400">Проверенные товары</div></div>
  <div class="p-4 text-center"><div class="text-emerald-500 text-xl mb-1"><i class="fas fa-clipboard-check"></i></div><div class="font-bold text-sm">Предзаказ</div><div class="text-xs text-gray-400">Удобно и быстро</div></div>
  <div class="p-4 text-center"><div class="text-sky-500 text-xl mb-1"><i class="fas fa-headset"></i></div><div class="font-bold text-sm">На связи</div><div class="text-xs text-gray-400">Всегда ответим</div></div>
</div></div>

{"<section class='max-w-7xl mx-auto px-4 py-14'><h2 class='text-2xl font-extrabold text-center mb-2'>Популярные категории</h2><div class='w-16 h-1 bg-brand mx-auto rounded mb-8'></div><div class='grid grid-cols-2 sm:grid-cols-3 md:grid-cols-"+str(min(len(cats),6))+" gap-4'>"+cat_html+"</div></section>" if cats else ""}

<section class="max-w-7xl mx-auto px-4 py-8">
<div class="flex justify-between items-end mb-6">
  <div><h2 class="text-2xl font-extrabold">Товары</h2><p class="text-gray-400 text-sm">Выберите и оставьте предзаказ</p></div>
  <a href="/catalog" class="text-brand font-semibold text-sm hover:underline">Весь каталог →</a>
</div>
<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">{cards}</div>
</section>
'''
    return page('Главная', content)

@app.route('/catalog')
def catalog():
    q = request.args.get('q', '').strip()
    cat_id = request.args.get('category', type=int)
    sort = request.args.get('sort', 'newest')
    query = Product.query
    if q: query = query.filter(Product.name.ilike(f'%{q}%') | Product.description.ilike(f'%{q}%'))
    if cat_id: query = query.filter(Product.category_id == cat_id)
    if sort == 'price_asc': query = query.order_by(Product.price.asc())
    elif sort == 'price_desc': query = query.order_by(Product.price.desc())
    else: query = query.order_by(Product.created_at.desc())
    products = query.all()
    cats = Category.query.all()
    cat_opts = ''.join(f'<option value="{c.id}" {"selected" if cat_id==c.id else ""}>{c.name}</option>' for c in cats)
    cards = ''.join(product_card(p) for p in products) or '<div class="col-span-full text-center py-16 text-gray-400">Ничего не найдено</div>'
    title = f'Поиск: {q}' if q else 'Каталог'
    content = f'''<div class="max-w-7xl mx-auto px-4 py-8">
<div class="flex flex-col lg:flex-row gap-6">
<aside class="lg:w-60 flex-shrink-0">
<div class="bg-soft rounded-2xl border border-violet-100 p-5 sticky top-20">
<h3 class="font-bold mb-3 flex items-center gap-2"><i class="fas fa-filter text-brand"></i> Фильтры</h3>
<form method="get" class="space-y-3">
<input name="q" value="{q}" placeholder="Поиск..." class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-brand/30 focus:outline-none">
<select name="category" class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm"><option value="">Все категории</option>{cat_opts}</select>
<select name="sort" class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm">
<option value="newest" {"selected" if sort=="newest" else ""}>Сначала новые</option>
<option value="price_asc" {"selected" if sort=="price_asc" else ""}>Цена: по возрастанию</option>
<option value="price_desc" {"selected" if sort=="price_desc" else ""}>Цена: по убыванию</option>
</select>
<button class="w-full btn-grad text-white py-2.5 rounded-xl text-sm font-bold">Применить</button>
<a href="/catalog" class="block text-center text-xs text-gray-400 mt-2 hover:text-brand">Сбросить</a>
</form></div></aside>
<div class="flex-1">
<div class="flex justify-between items-center mb-5">
<h1 class="text-2xl font-extrabold">{title}</h1>
<span class="text-sm text-gray-400">{len(products)} товар(ов)</span>
</div>
<div class="grid grid-cols-2 sm:grid-cols-2 xl:grid-cols-3 gap-4">{cards}</div>
</div></div></div>'''
    return page(title, content)

@app.route('/product/<int:pid>')
def product_detail(pid):
    p = Product.query.get_or_404(pid)
    cat = f'<span class="text-xs font-semibold text-brand bg-soft px-3 py-1 rounded-full">{p.category.name}</span>' if p.category else ''
    content = f'''<div class="max-w-7xl mx-auto px-4 py-8">
<nav class="text-sm text-gray-400 mb-6"><a href="/" class="hover:text-brand">Главная</a> / <a href="/catalog" class="hover:text-brand">Каталог</a> / <span class="text-gray-700">{p.name}</span></nav>
<div class="grid md:grid-cols-2 gap-10">
<div class="bg-gray-50 rounded-3xl overflow-hidden border border-gray-100">
<img src="{p.image_url}" class="w-full aspect-square object-cover" onerror="this.src='https://via.placeholder.com/600'"></div>
<div class="flex flex-col justify-center">
{cat}
<h1 class="text-3xl font-extrabold mt-3 mb-3 text-gray-900">{p.name}</h1>
<div class="text-3xl font-extrabold text-brand mb-5">{p.price:,.0f} <span class="text-lg">сом</span></div>
<p class="text-gray-500 mb-8 leading-relaxed">{p.description or "Описание скоро появится"}</p>
<form action="/cart/add/{p.id}" method="post" class="flex flex-wrap gap-3 items-center">
<input type="number" name="quantity" value="1" min="1" class="w-20 border border-gray-200 rounded-xl px-3 py-3 text-center font-semibold">
<button class="btn-grad text-white font-bold px-8 py-3 rounded-xl shadow-lg hover:opacity-90 flex items-center gap-2">
<i class="fas fa-shopping-bag"></i> В предзаказ</button>
</form></div></div></div>'''
    return page(p.name, content)

@app.route('/cart')
def cart():
    items_html, total = '', 0
    for pid, qty in get_cart().items():
        p = Product.query.get(int(pid))
        if not p: continue
        sub = p.price * qty; total += sub
        items_html += f'''<div class="p-4 flex flex-col sm:flex-row gap-4 items-center border-b border-gray-50">
<img src="{p.image_url}" class="w-20 h-20 object-cover rounded-xl bg-gray-50" onerror="this.src='https://via.placeholder.com/80'">
<div class="flex-1 text-center sm:text-left"><a href="/product/{p.id}" class="font-bold hover:text-brand">{p.name}</a>
<p class="text-sm text-gray-400">{p.price:,.0f} сом</p></div>
<form action="/cart/update/{p.id}" method="post" class="flex gap-2 items-center">
<input type="number" name="quantity" value="{qty}" min="0" class="w-16 border rounded-lg px-2 py-1.5 text-center text-sm">
<button class="text-sm text-brand font-semibold">OK</button></form>
<div class="font-extrabold text-brand w-24 text-right">{sub:,.0f} сом</div>
<a href="/cart/remove/{p.id}" class="text-red-400 hover:text-red-600 text-sm ml-2"><i class="fas fa-trash"></i></a></div>'''
    
    checkout_form = f'''<div class="bg-gray-50 p-6 rounded-2xl border border-gray-100 mt-6">
<h2 class="text-lg font-extrabold mb-4">Оформить предзаказ</h2>
<form action="/checkout" method="post" class="space-y-4">
<div><label class="block text-sm font-semibold mb-1">Ваше имя</label>
<input type="text" name="name" required class="w-full border rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-brand/40"></div>
<div><label class="block text-sm font-semibold mb-1">Номер телефона</label>
<input type="text" name="phone" required placeholder="+996 ..." class="w-full border rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-brand/40"></div>
<button class="w-full btn-orange text-white font-bold py-3 rounded-xl shadow-lg hover:opacity-90">Подтвердить предзаказ</button>
</form></div>''' if items_html else ''

    content = f'''<div class="max-w-4xl mx-auto px-4 py-8">
<h1 class="text-2xl font-extrabold mb-6">Предзаказ</h1>
{"<div class='bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden mb-6'>"+items_html+"<div class='p-4 bg-gray-50 flex justify-between items-center font-extrabold'><span>Итого:</span><span class='text-xl text-brand'>"+f"{total:,.0f}"+" сом</span></div></div>"+checkout_form if items_html else "<div class='text-center py-12 text-gray-400'>Корзина пуста</div>"}
</div>'''
    return page('Корзина', content)

@app.route('/cart/add/<int:pid>', methods=['POST'])
def cart_add(pid):
    cart_data = get_cart()
    qty = int(request.form.get('quantity', 1))
    cart_data[str(pid)] = cart_data.get(str(pid), 0) + qty
    session['cart'] = cart_data
    flash('Товар добавлен в корзину', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/cart/update/<int:pid>', methods=['POST'])
def cart_update(pid):
    cart_data = get_cart()
    qty = int(request.form.get('quantity', 1))
    if qty > 0:
        cart_data[str(pid)] = qty
    else:
        cart_data.pop(str(pid), None)
    session['cart'] = cart_data
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:pid>')
def cart_remove(pid):
    cart_data = get_cart()
    cart_data.pop(str(pid), None)
    session['cart'] = cart_data
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    c = get_cart()
    if not c: return redirect(url_for('index'))
    name = request.form.get('name')
    phone = request.form.get('phone')
    tot = cart_total()
    
    order = Order(customer_name=name, customer_phone=phone, total_price=tot)
    db.session.add(order)
    db.session.flush()
    
    for pid, qty in c.items():
        p = Product.query.get(int(pid))
        if p:
            db.session.add(OrderItem(order_id=order.id, product_id=p.id, quantity=qty, price=p.price))
            
    db.session.commit()
    session['cart'] = {}
    flash('Предзаказ успешно оформлен! Мы свяжемся с вами.', 'success')
    return redirect(url_for('index'))

# ==================== FULL ADMIN PANEL ====================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Неверный пароль', 'danger')
    return page('Вход в админку', '''
    <div class="max-w-md mx-auto my-16 p-6 bg-white rounded-2xl border shadow-sm">
        <h2 class="text-xl font-bold mb-4 text-center">Панель управления</h2>
        <form method="post" class="space-y-4">
            <input type="password" name="password" placeholder="Пароль администратора" class="w-full border p-3 rounded-xl">
            <button class="w-full btn-grad text-white font-bold p-3 rounded-xl">Войти</button>
        </form>
    </div>
    ''')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    products = Product.query.order_by(Product.id.desc()).all()
    orders = Order.query.order_by(Order.id.desc()).all()
    categories = Category.query.all()
    
    prod_rows = ''.join([f'''
    <tr class="border-b">
        <td class="p-3"><img src="{p.image_url}" class="w-12 h-12 object-cover rounded-lg"></td>
        <td class="p-3 font-bold">{p.name}</td>
        <td class="p-3">{p.category.name if p.category else 'Без категории'}</td>
        <td class="p-3 text-brand font-bold">{p.price:,.0f} сом</td>
        <td class="p-3">
            <a href="/admin/product/edit/{p.id}" class="text-blue-600 mr-2"><i class="fas fa-edit"></i></a>
            <a href="/admin/product/delete/{p.id}" onclick="return confirm('Удалить?')" class="text-red-500"><i class="fas fa-trash"></i></a>
        </td>
    </tr>''' for p in products]) or '<tr><td colspan="5" class="p-4 text-center text-gray-400">Товаров нет</td></tr>'

    cat_rows = ''.join([f'''
    <tr class="border-b">
        <td class="p-3">{c.name}</td>
        <td class="p-3 text-right">
            <a href="/admin/category/delete/{c.id}" onclick="return confirm('Удалить категорию?')" class="text-red-500"><i class="fas fa-trash"></i></a>
        </td>
    </tr>''' for c in categories]) or '<tr><td colspan="2" class="p-4 text-center text-gray-400">Категорий нет</td></tr>'

    order_rows = ''.join([f'''
    <tr class="border-b">
        <td class="p-3 font-bold">#{o.id}</td>
        <td class="p-3">{o.customer_name}<br><span class="text-xs text-gray-400">{o.customer_phone}</span></td>
        <td class="p-3 font-bold text-brand">{o.total_price:,.0f} сом</td>
        <td class="p-3"><span class="px-2 py-1 rounded-full text-xs font-bold bg-yellow-100 text-yellow-800">{o.status}</span></td>
        <td class="p-3"><a href="/admin/order/delete/{o.id}" class="text-red-500"><i class="fas fa-trash"></i></a></td>
    </tr>''' for o in orders]) or '<tr><td colspan="5" class="p-4 text-center text-gray-400">Заказов нет</td></tr>'

    content = f'''
    <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-3xl font-extrabold">Админ-панель</h1>
            <div class="flex gap-3">
                <a href="/admin/product/new" class="btn-grad text-white px-4 py-2 rounded-xl font-bold text-sm">+ Добавить товар</a>
                <a href="/admin/logout" class="bg-gray-100 text-gray-600 px-4 py-2 rounded-xl text-sm font-semibold">Выйти</a>
            </div>
        </div>

        <div class="grid lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2 space-y-8">
                <!-- Товары -->
                <div class="bg-white rounded-2xl border p-5 shadow-sm">
                    <h2 class="text-lg font-bold mb-4">Все товары ({len(products)})</h2>
                    <div class="overflow-x-auto"><table class="w-full text-left text-sm"><thead><tr class="border-b bg-gray-50"><th class="p-3">Фото</th><th class="p-3">Название</th><th class="p-3">Категория</th><th class="p-3">Цена</th><th class="p-3">Действия</th></tr></thead><tbody>{prod_rows}</tbody></table></div>
                </div>

                <!-- Заказы -->
                <div class="bg-white rounded-2xl border p-5 shadow-sm">
                    <h2 class="text-lg font-bold mb-4">Предзаказы ({len(orders)})</h2>
                    <div class="overflow-x-auto"><table class="w-full text-left text-sm"><thead><tr class="border-b bg-gray-50"><th class="p-3">ID</th><th class="p-3">Клиент</th><th class="p-3">Сумма</th><th class="p-3">Статус</th><th class="p-3">Удалить</th></tr></thead><tbody>{order_rows}</tbody></table></div>
                </div>
            </div>

            <!-- Боковая колонка (Категории) -->
            <div class="space-y-6">
                <div class="bg-white rounded-2xl border p-5 shadow-sm">
                    <h2 class="text-lg font-bold mb-4">Категории</h2>
                    <form action="/admin/category/new" method="post" class="flex gap-2 mb-4">
                        <input type="text" name="name" required placeholder="Новая категория" class="flex-1 border px-3 py-1.5 rounded-xl text-sm">
                        <button class="bg-brand text-white px-3 py-1.5 rounded-xl text-sm font-bold">+</button>
                    </form>
                    <table class="w-full text-left text-sm"><tbody>{cat_rows}</tbody></table>
                </div>
            </div>
        </div>
    </div>
    '''
    return page('Админка', content)

@app.route('/admin/product/new', methods=['GET', 'POST'])
@admin_required
def admin_product_new():
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price', 0))
        description = request.form.get('description', '')
        category_id = request.form.get('category_id', type=int)
        
        image_url = 'https://via.placeholder.com/400x300?text=Product'
        if 'image' in request.files:
            file_path = save_upload(request.files['image'])
            if file_path: image_url = file_path

        p = Product(name=name, price=price, description=description, category_id=category_id, image_url=image_url)
        db.session.add(p)
        db.session.commit()
        flash('Товар добавлен', 'success')
        return redirect(url_for('admin_dashboard'))

    cats = Category.query.all()
    cat_opts = ''.join(f'<option value="{c.id}">{c.name}</option>' for c in cats)
    return page('Новый товар', f'''
    <div class="max-w-xl mx-auto py-8 px-4">
        <h1 class="text-2xl font-bold mb-6">Добавить новый товар</h1>
        <form method="post" enctype="multipart/form-data" class="bg-white p-6 rounded-2xl border space-y-4">
            <div><label class="block text-sm font-bold mb-1">Название</label><input type="text" name="name" required class="w-full border rounded-xl p-2.5"></div>
            <div><label class="block text-sm font-bold mb-1">Цена (сом)</label><input type="number" step="0.1" name="price" required class="w-full border rounded-xl p-2.5"></div>
            <div><label class="block text-sm font-bold mb-1">Категория</label><select name="category_id" class="w-full border rounded-xl p-2.5"><option value="">Без категории</option>{cat_opts}</select></div>
            <div><label class="block text-sm font-bold mb-1">Изображение</label><input type="file" name="image" accept="image/*" class="w-full border rounded-xl p-2.5"></div>
            <div><label class="block text-sm font-bold mb-1">Описание</label><textarea name="description" class="w-full border rounded-xl p-2.5 h-24"></textarea></div>
            <button class="w-full btn-grad text-white font-bold py-3 rounded-xl">Сохранить</button>
        </form>
    </div>
    ''')

@app.route('/admin/product/delete/<int:pid>')
@admin_required
def admin_product_delete(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash('Товар удален', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/category/new', methods=['POST'])
@admin_required
def admin_category_new():
    name = request.form.get('name')
    if name:
        db.session.add(Category(name=name))
        db.session.commit()
        flash('Категория добавлена', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/category/delete/<int:cid>')
@admin_required
def admin_category_delete(cid):
    c = Category.query.get_or_404(cid)
    db.session.delete(c)
    db.session.commit()
    flash('Категория удалена', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/order/delete/<int:oid>')
@admin_required
def admin_order_delete(oid):
    o = Order.query.get_or_404(oid)
    db.session.delete(o)
    db.session.commit()
    flash('Заказ удален', 'success')
    return redirect(url_for('admin_dashboard'))

# Автоматическое создание таблиц
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)