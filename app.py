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
  <a href="/catalog" class="bg-brand text-white text-sm font-semibold px-4 py-2 rounded-xl hover:opacity-90">Каталог</a>
</div>
</header>

<main class="flex-1">{{ content|safe }}</main>

<footer class="bg-gray-900 text-gray-400 mt-16 py-6 text-center text-xs">
  © 2026 Мир канцелярии
</footer>
</body></html>
'''

def page(title, content):
    return render_template_string(LAYOUT, title=title, content=content)

def product_card(p):
    return f'''<div class="card bg-white rounded-2xl overflow-hidden border border-gray-100 shadow-sm p-3">
<div class="aspect-square bg-gray-50 rounded-xl overflow-hidden mb-2">
<img src="{p.image_url}" class="w-full h-full object-cover"></div>
<h3 class="font-bold text-gray-800 text-sm line-clamp-2">{p.name}</h3>
<p class="text-xs text-gray-400 mt-1 line-clamp-2">{p.description or ""}</p>
<div class="font-extrabold text-brand mt-2">{p.price:,.0f} сом</div>
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

# Автоматическое создание/обновление таблиц при запуске
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)