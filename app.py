
from flask import Flask, request, redirect, url_for, flash, session, render_template_string, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
import os, uuid

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

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    image_url = db.Column(db.String(500), default='https://via.placeholder.com/400x300?text=Product')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship('Category', backref='products')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Новый')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==================== HELPERS ====================
def get_cart():
    return session.get('cart', {})

def cart_count():
    return sum(get_cart().values())

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
.btn-grad{background:linear-gradient(135deg,#6C5CE7,#A66CFF)}
.btn-orange{background:linear-gradient(135deg,#FF6B35,#FF8F66)}
</style>
</head>
<body class="bg-white min-h-screen flex flex-col">
<header class="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-gray-100 shadow-sm">
<div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-3">
  <a href="/" class="flex items-center gap-2">
    <div class="w-10 h-10 rounded-xl btn-grad flex items-center justify-center text-white font-extrabold text-lg">М</div>
    <div class="leading-tight">
      <div class="font-extrabold text-brand text-sm">МИР</div>
      <div class="text-[10px] text-gray-500 -mt-0.5 tracking-wide">КАНЦЕЛЯРИИ</div>
    </div>
  </a>
  <div class="flex items-center gap-4">
    <a href="/catalog" class="bg-brand text-white text-sm font-semibold px-4 py-2 rounded-xl hover:opacity-90">Каталог</a>
    <a href="/cart" class="relative p-2 rounded-xl hover:bg-soft" title="Предзаказ">
      <i class="fas fa-shopping-bag text-xl text-gray-600"></i>
      {% if cart_count %}<span class="absolute -top-0.5 -right-0.5 bg-accent text-white text-[10px] font-bold rounded-full h-5 w-5 flex items-center justify-center">{{ cart_count }}</span>{% endif %}
    </a>
  </div>
</div>
</header>

{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}<div class="max-w-7xl mx-auto px-4 mt-3 space-y-1">
{% for cat,msg in messages %}
<div class="px-4 py-2.5 rounded-xl text-sm font-medium {% if cat=='success' %}bg-green-50 text-green-700 border border-green-100{% else %}bg-blue-50 text-blue-700 border border-blue-100{% endif %}">{{ msg }}</div>
{% endfor %}</div>{% endif %}{% endwith %}

<main class="flex-1">{{ content|safe }}</main>

<footer class="bg-gray-900 text-gray-400 mt-16 py-6 text-center text-xs">
  © 2026 Мир канцелярии · Кыргызстан
</footer>
</body></html>
'''

def page(title, content):
    from flask import get_flashed_messages
    return render_template_string(LAYOUT, title=title, content=content, cart_count=cart_count(), get_flashed_messages=get_flashed_messages)

def product_card(p):
    return f'''<div class="card bg-white rounded-2xl overflow-hidden border border-gray-100 shadow-sm p-3">
<a href="/product/{p.id}">
  <div class="aspect-square bg-gray-50 rounded-xl overflow-hidden mb-2">
    <img src="{p.image_url}" class="w-full h-full object-cover" onerror="this.src='https://via.placeholder.com/400x400?text=Фото'">
  </div>
  <h3 class="font-bold text-gray-800 text-sm line-clamp-2">{p.name}</h3>
</a>
<p class="text-xs text-gray-400 mt-1 line-clamp-2">{p.description or ""}</p>
<div class="flex justify-between items-center mt-3">
  <span class="font-extrabold text-brand">{p.price:,.0f} сом</span>
  <form action="/cart/add/{p.id}" method="post">
    <button class="w-8 h-8 rounded-lg btn-grad text-white flex items-center justify-center"><i class="fas fa-plus text-xs"></i></button>
  </form>
</div>
</div>'''

# ==================== PUBLIC ROUTES ====================
@app.route('/')
def index():
    products = Product.query.order_by(Product.created_at.desc()).all()
    cards = ''.join(product_card(p) for p in products) or '<div class="col-span-full text-center py-12 text-gray-400">Товаров пока нет</div>'
    
    content = f'''
<div class="max-w-7xl mx-auto px-4 py-8">
  <h1 class="text-2xl font-extrabold mb-6">Каталог товаров</h1>
  <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">{cards}</div>
</div>'''
    return page('Главная', content)

@app.route('/catalog')
def catalog():
    return redirect(url_for('index'))

@app.route('/product/<int:pid>')
def product_detail(pid):
    p = Product.query.get_or_404(pid)
    content = f'''<div class="max-w-4xl mx-auto px-4 py-8">
<div class="grid md:grid-cols-2 gap-8">
<div class="bg-gray-50 rounded-2xl overflow-hidden border border-gray-100">
<img src="{p.image_url}" class="w-full aspect-square object-cover" onerror="this.src='https://via.placeholder.com/600'"></div>
<div>
<h1 class="text-2xl font-extrabold mb-2">{p.name}</h1>
<div class="text-2xl font-extrabold text-brand mb-4">{p.price:,.0f} сом</div>
<p class="text-gray-500 mb-6">{p.description or "Описание скоро появится"}</p>
<form action="/cart/add/{p.id}" method="post">
<button class="btn-grad text-white font-bold px-6 py-2.5 rounded-xl">В корзину</button>
</form></div></div></div>'''
    return page(p.name, content)

@app.route('/cart')
def cart():
    items_html, total = '', 0
    for pid, qty in get_cart().items():
        p = Product.query.get(int(pid))
        if not p: continue
        sub = p.price * qty; total += sub
        items_html += f'''<div class="p-4 flex justify-between items-center border-b">
<div><div class="font-bold">{p.name}</div><div class="text-sm text-gray-400">{p.price:,.0f} сом x {qty}</div></div>
<div class="font-bold text-brand">{sub:,.0f} сом</div></div>'''
    
    content = f'''<div class="max-w-2xl mx-auto px-4 py-8">
<h1 class="text-2xl font-extrabold mb-6">Корзина</h1>
{"<div class='bg-white rounded-xl border mb-4'>"+items_html+"<div class='p-4 font-bold flex justify-between'><span>Итого:</span><span class='text-brand'>"+f"{total:,.0f}"+" сом</span></div></div>" if items_html else "<div class='text-center py-8 text-gray-400'>Корзина пуста</div>"}
</div>'''
    return page('Корзина', content)

@app.route('/cart/add/<int:pid>', methods=['POST'])
def cart_add(pid):
    cart_data = get_cart()
    cart_data[str(pid)] = cart_data.get(str(pid), 0) + 1
    session['cart'] = cart_data
    flash('Товар добавлен в корзину', 'success')
    return redirect(request.referrer or url_for('index'))

# Автоматическое пересоздание таблиц при конфликте базы данных
with app.app_context():
    try:
        db.create_all()
    except Exception:
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)