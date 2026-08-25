From flask import Flask, request, redirect, url_for, flash, session, render_template_string, send_from_directory
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
    if s: s.value = value
    else: db.session.add(Setting(key=key, value=value))
    db.session.commit()

class BotState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(50), unique=True, nullable=False)
    step = db.Column(db.String(50), default='idle')  # idle, wait_name, wait_price
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

ADMIN_PASSWORD = 'admin123'

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

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

def page(title, content, **ctx):
    from flask import get_flashed_messages, request as req
    ctx.update(title=title, content=content, cart_count=cart_count(),
               categories=Category.query.all(), get_flashed_messages=get_flashed_messages, request=req)
    return render_template_string(LAYOUT, **ctx)

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

# ==================== PUBLIC ====================
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
<!-- HERO -->
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

<!-- BENEFITS -->
<div class="max-w-7xl mx-auto px-4 -mt-6 relative z-10">
<div class="bg-white rounded-2xl shadow-lg border border-gray-100 grid grid-cols-2 md:grid-cols-4 divide-x divide-gray-100 overflow-hidden">
  <div class="p-4 text-center"><div class="text-brand text-xl mb-1"><i class="fas fa-th"></i></div><div class="font-bold text-sm">Широкий ассортимент</div><div class="text-xs text-gray-400">Много товаров</div></div>
  <div class="p-4 text-center"><div class="text-amber-500 text-xl mb-1"><i class="fas fa-star"></i></div><div class="font-bold text-sm">Качество</div><div class="text-xs text-gray-400">Проверенные товары</div></div>
  <div class="p-4 text-center"><div class="text-emerald-500 text-xl mb-1"><i class="fas fa-clipboard-check"></i></div><div class="font-bold text-sm">Предзаказ</div><div class="text-xs text-gray-400">Удобно и быстро</div></div>
  <div class="p-4 text-center"><div class="text-sky-500 text-xl mb-1"><i class="fas fa-headset"></i></div><div class="font-bold text-sm">На связи</div><div class="text-xs text-gray-400">Всегда ответим</div></div>
</div></div>

<!-- CATEGORIES -->
{"<section class='max-w-7xl mx-auto px-4 py-14'><h2 class='text-2xl font-extrabold text-center mb-2'>Популярные категории</h2><div class='w-16 h-1 bg-brand mx-auto rounded mb-8'></div><div class='grid grid-cols-2 sm:grid-cols-3 md:grid-cols-"+str(min(len(cats),6))+" gap-4'>"+cat_html+"</div></section>" if cats else ""}

<!-- PRODUCTS -->
<section class="max-w-7xl mx-auto px-4 py-8">
<div class="flex justify-between items-end mb-6">
  <div><h2 class="text-2xl font-extrabold">Товары</h2><p class="text-gray-400 text-sm">Выберите и оставьте предзаказ</p></div>
  <a href="/catalog" class="text-brand font-semibold text-sm hover:underline">Весь каталог →</a>
</div>
<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">{cards}</div>
</section>

<!-- CTA -->
<section class="max-w-7xl mx-auto px-4 py-8">
<div class="rounded-2xl bg-gradient-to-r from-violet-50 to-orange-50 border border-violet-100 p-6 md:p-8 flex flex-col md:flex-row items-center gap-4 justify-between">
  <div class="flex items-center gap-4">
    <div class="text-4xl">🎁</div>
    <div><div class="font-extrabold text-lg">Оформите предзаказ прямо сейчас!</div>
    <div class="text-sm text-gray-500">Выберите товары — мы свяжемся с вами для уточнения</div></div>
  </div>
  <a href="/catalog" class="btn-grad text-white font-bold px-6 py-3 rounded-full whitespace-nowrap">В каталог</a>
</div></section>
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
<a href="/cart/remove/{p.id}" class="text-red-400 hover:text-red-600 text-sm ml-2"><i class
