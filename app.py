# -*- coding: utf-8 -*-
"""Мир Канцелярии — магазин с дизайном по макету."""
import os
import uuid
from datetime import datetime
from functools import wraps

import requests
from flask import (
    Flask, request, redirect, url_for, session, flash,
    render_template, send_from_directory, abort, jsonify,
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
app.secret_key = os.environ.get("SECRET_KEY", "mir-kanc-design-2026")

db_url = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(DATA_DIR, "shop.db"))
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

db = SQLAlchemy(app)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ADMIN_IDS = [x.strip() for x in os.environ.get("TELEGRAM_ADMIN_IDS", "").split(",") if x.strip()]
API_SECRET = os.environ.get("API_SECRET", "mir-api-secret-2026")
SITE_NAME = os.environ.get("SITE_NAME", "Мир Канцелярии")
SITE_PHONE = os.environ.get("SITE_PHONE", "")
SITE_TAGLINE = os.environ.get(
    "SITE_TAGLINE", "Стильные канцтовары для учёбы, работы и твоих больших идей"
)
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}

DEFAULT_CATEGORIES = [
    "Письменные принадлежности",
    "Тетради и блокноты",
    "Рюкзаки и сумки",
    "Для творчества",
    "Офисные товары",
    "Школьные товары",
    "Ручки и маркеры",
    "Карандаши и грифели",
    "Бумага и альбомы",
    "Краски и кисти",
    "Пеналы",
    "Файлы и папки",
    "Клей и скотч",
    "Стикеры и закладки",
    "Линейки и чертежные",
    "Калькуляторы",
    "Подарки и сувениры",
    "Для дошкольников",
]


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
    status = db.Column(db.String(30), default="new")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=True)
    product_name = db.Column(db.String(200), default="")
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, default=0)


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
            print("tg", e)


@app.context_processor
def inject_globals():
    return {
        "site_name": SITE_NAME,
        "tagline": SITE_TAGLINE,
        "phone": SITE_PHONE,
        "cart_count": cart_count(),
    }


@app.route("/uploads/<path:filename>")
def uploaded(filename):
    return send_from_directory(UPLOAD, filename)


@app.route("/")
def index():
    products = Product.query.filter_by(in_stock=True).order_by(Product.created_at.desc()).limit(8).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template("index.html", products=products, categories=categories)


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
    categories = Category.query.order_by(Category.name).all()
    return render_template(
        "catalog.html", products=products, categories=categories, q=q, category_id=cat_id
    )


@app.route("/product/<int:pid>")
def product_detail(pid):
    product = db.session.get(Product, pid)
    if not product:
        abort(404)
    return render_template("product.html", product=product)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/cart")
def cart_page():
    return render_template("cart.html", items=cart_items(), total=cart_total())


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
        return render_template("thanks.html", order=order)
    return render_template("checkout.html", total=cart_total())


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
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/")


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    debt_open = db.session.query(db.func.coalesce(db.func.sum(Debt.amount), 0)).filter_by(status="open").scalar() or 0
    stats = {
        "products": Product.query.count(),
        "new_orders": Order.query.filter_by(status="new").count(),
        "orders": Order.query.count(),
        "debts": debt_open,
    }
    return render_template("admin_dashboard.html", admin_tab="dash", stats=stats)


@app.route("/admin/products")
@admin_required
def admin_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("admin_products.html", admin_tab="products", products=products)


@app.route("/admin/products/add", methods=["GET", "POST"])
@app.route("/admin/products/edit/<int:pid>", methods=["GET", "POST"])
@admin_required
def admin_product_form(pid=None):
    product = db.session.get(Product, pid) if pid else None
    categories = Category.query.order_by(Category.name).all()
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
        if product:
            product.name = name
            product.price = price
            product.description = request.form.get("description", "").strip()
            product.category_id = cat_id
            product.in_stock = bool(request.form.get("in_stock"))
            if img:
                product.image_url = img
        else:
            product = Product(
                name=name,
                price=price,
                description=request.form.get("description", "").strip(),
                category_id=cat_id,
                image_url=img or "",
                in_stock=bool(request.form.get("in_stock")),
            )
            db.session.add(product)
        db.session.commit()
        flash("Сохранено", "success")
        return redirect(url_for("admin_products"))
    return render_template(
        "admin_product_form.html", admin_tab="products", product=product, categories=categories
    )


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
    return render_template("admin_orders.html", admin_tab="orders", orders=orders)


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


@app.route("/admin/orgs")
@admin_required
def admin_orgs():
    orgs = Organization.query.order_by(Organization.name).all()
    for o in orgs:
        o.open_debt = sum(d.amount or 0 for d in o.debts if d.status == "open")
    return render_template("admin_orgs.html", admin_tab="orgs", orgs=orgs)


@app.route("/admin/orgs/add", methods=["GET", "POST"])
@app.route("/admin/orgs/edit/<int:oid>", methods=["GET", "POST"])
@admin_required
def admin_org_form(oid=None):
    org = db.session.get(Organization, oid) if oid else None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Укажите название", "danger")
            return redirect(request.url)
        if org:
            org.name = name
            org.phone = request.form.get("phone", "").strip()
            org.note = request.form.get("note", "").strip()
        else:
            db.session.add(
                Organization(
                    name=name,
                    phone=request.form.get("phone", "").strip(),
                    note=request.form.get("note", "").strip(),
                )
            )
        db.session.commit()
        flash("Сохранено", "success")
        return redirect(url_for("admin_orgs"))
    return render_template("admin_org_form.html", admin_tab="orgs", org=org)


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
    org_map = {x.id: x.name for x in Organization.query.all()}
    total = db.session.query(db.func.coalesce(db.func.sum(Debt.amount), 0)).filter_by(status="open").scalar() or 0
    return render_template(
        "admin_debts.html",
        admin_tab="debts",
        debts=debts,
        org_map=org_map,
        total=total,
        status=status,
    )


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
        db.session.add(
            Debt(
                organization_id=oid,
                product_id=pid,
                product_name=product_name,
                quantity=qty,
                amount=amount,
                description=request.form.get("description", "").strip(),
                status="open",
            )
        )
        db.session.commit()
        flash("Долг записан", "success")
        return redirect(url_for("admin_debts"))
    return render_template(
        "admin_debt_form.html", admin_tab="debts", orgs=orgs, products=products
    )


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


@app.route("/admin/categories", methods=["GET", "POST"])
@admin_required
def admin_categories():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name and not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
            db.session.commit()
            flash("Добавлено", "success")
        return redirect(url_for("admin_categories"))
    categories = Category.query.order_by(Category.name).all()
    return render_template("admin_categories.html", admin_tab="cats", categories=categories)


@app.route("/api/products", methods=["GET", "POST"])
def api_products():
    if request.method == "POST":
        key = request.headers.get("X-API-Key") or request.form.get("api_key")
        if key != API_SECRET:
            return jsonify(ok=False, error="Unauthorized"), 401
        name = (request.form.get("name") or request.form.get("title") or "").strip()
        if not name:
            return jsonify(ok=False, error="name required"), 400
        try:
            price = float(str(request.form.get("price") or 0).replace(",", "."))
        except ValueError:
            price = 0
        img = ""
        f = request.files.get("image")
        if f and f.filename:
            img = save_upload(f)
        prod = Product(name=name[:200], price=price, image_url=img, in_stock=True)
        db.session.add(prod)
        db.session.commit()
        return jsonify(ok=True, id=prod.id), 201
    items = []
    for p in Product.query.order_by(Product.created_at.desc()).limit(200).all():
        items.append(
            {
                "id": p.id,
                "name": p.name,
                "title": p.name,
                "price": p.price,
                "image_url": p.image_url or "",
                "category": p.category.name if p.category else "",
            }
        )
    return jsonify(ok=True, items=items)


@app.route("/health")
def health():
    return jsonify(ok=True, site=SITE_NAME)


with app.app_context():
    try:
        db.create_all()
        existing = {c.name for c in Category.query.all()}
        for n in DEFAULT_CATEGORIES:
            if n not in existing:
                db.session.add(Category(name=n))
        db.session.commit()
    except Exception as e:
        print("init", e)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
