# -*- coding: utf-8 -*-
"""Мир Канцелярии — магазин с дизайном по макету."""
import os
import secrets
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
from catalog_seed import CATALOG_PRODUCTS

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
ADMIN_GATE = os.environ.get("ADMIN_GATE", "mir-secret-enter").strip()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ADMIN_IDS = [x.strip() for x in os.environ.get("TELEGRAM_ADMIN_IDS", "").split(",") if x.strip()]
API_SECRET = os.environ.get("API_SECRET", "mir-api-secret-2026")
SITE_NAME = os.environ.get("SITE_NAME", "Мир канцелярии")
SITE_PHONE = os.environ.get("SITE_PHONE", "")
PAYMENT_INFO = os.environ.get(
    "PAYMENT_INFO",
    "Перевод на карту — уточните реквизиты у менеджера после заявки",
)
PAYMENT_LINK_1 = os.environ.get("PAYMENT_LINK_1", "").strip()
PAYMENT_LINK_2 = os.environ.get("PAYMENT_LINK_2", "").strip()
PAYMENT_LINK_1_LABEL = os.environ.get("PAYMENT_LINK_1_LABEL", "Оплатить (ссылка 1)").strip()
PAYMENT_LINK_2_LABEL = os.environ.get("PAYMENT_LINK_2_LABEL", "Оплатить (ссылка 2)").strip()
SITE_TAGLINE = os.environ.get(
    "SITE_TAGLINE",
    "Канцтовары для школы, офиса и творчества. Оформите предзаказ — мы подтвердим наличие и способ оплаты."
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
    payment_method = db.Column(db.String(40), default="cash")  # cash / transfer
    total_price = db.Column(db.Float, default=0)
    status = db.Column(db.String(30), default="await_pay")  # await_pay / paid / done / cancel
    token = db.Column(db.String(40), default="")
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



class PaymentMethod(db.Model):
    """Способы оплаты из админки (реквизиты, QR, ссылка)."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    details = db.Column(db.Text, default="")
    qr_url = db.Column(db.String(500), default="")
    link_url = db.Column(db.String(500), default="")
    active = db.Column(db.Boolean, default=True)
    position = db.Column(db.Integer, default=0)


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, default="")


class BotState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(50), unique=True, nullable=False)
    step = db.Column(db.String(40), default="idle")  # idle | wait_price | wait_rename | wait_name_photo
    product_id = db.Column(db.Integer, nullable=True)
    draft_image = db.Column(db.String(500), default="")



def get_setting(key, default=""):
    s = Setting.query.filter_by(key=key).first()
    return s.value if s and s.value is not None else default


def set_setting(key, value):
    s = Setting.query.filter_by(key=key).first()
    if s:
        s.value = value
    else:
        db.session.add(Setting(key=key, value=value))
    db.session.commit()


def public_methods():
    return PaymentMethod.query.filter_by(active=True).order_by(PaymentMethod.position, PaymentMethod.id).all()



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
            return redirect(url_for("index"))
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
    pm = getattr(order, "payment_method", "cash")
    if pm == "link":
        pay = "Оплата по ссылке"
    elif pm == "transfer":
        pay = "Перевод на карту"
    else:
        pay = "Наличными / при получении"
    lines.append(f"💳 {pay}")
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
    products = Product.query.filter(Product.in_stock.is_(True)).order_by(Product.created_at.desc()).limit(8).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template("index.html", products=products, categories=categories)


@app.route("/catalog")
def catalog():
    q = request.args.get("q", "").strip()
    # скрытый вход в админку: особое слово в поиске (ADMIN_GATE)
    if ADMIN_GATE and q and q.strip().lower() == ADMIN_GATE.lower():
        session["admin"] = True
        return redirect(url_for("admin_dashboard"))
    cat_id = request.args.get("category", type=int)
    query = Product.query.filter(Product.in_stock.is_(True))
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
        pay_method = request.form.get("payment_method", "cash")
        if pay_method not in ("cash", "transfer", "link"):
            pay_method = "cash"
        order = Order(
            customer_name=name,
            customer_phone=phone,
            comment=comment,
            payment_method=pay_method or "link",
            total_price=cart_total(),
            status="await_pay",
            token=secrets.token_urlsafe(16),
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
        session["cart"] = {}
        try:
            tg_notify_order(order)
        except Exception as e:
            print("tg", e)
        return redirect(url_for("order_done", oid=order.id, token=order.token))
    return render_template(
            "checkout.html",
            total=cart_total(),
            payment_info=PAYMENT_INFO,
            payment_link_1=PAYMENT_LINK_1,
            payment_link_2=PAYMENT_LINK_2,
            payment_link_1_label=PAYMENT_LINK_1_LABEL,
            payment_link_2_label=PAYMENT_LINK_2_LABEL,
        )


# ─── Admin ────────────────────────────────────────────────


@app.route("/order/<int:oid>/<token>")
def order_done(oid, token):
    o = db.session.get(Order, oid)
    if not o or not o.token or o.token != token:
        abort(404)
    methods = public_methods()
    return render_template(
        "thanks.html",
        order=o,
        methods=methods,
        payment_info=PAYMENT_INFO,
        payment_link_1=PAYMENT_LINK_1,
        payment_link_2=PAYMENT_LINK_2,
        payment_link_1_label=PAYMENT_LINK_1_LABEL,
        payment_link_2_label=PAYMENT_LINK_2_LABEL,
    )


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    """Вход только через особое слово в поиске (ADMIN_GATE). Страницы пароля нет."""
    if session.get("admin"):
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("index"))


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
        "new_orders": Order.query.filter(Order.status.in_(["new", "await_pay"])).count(),
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
        # checkbox: если нет в форме при создании — считаем «в наличии»
        in_stock = request.form.get("in_stock") == "1" if product else (
            request.form.get("in_stock", "1") == "1"
        )
        if product:
            product.name = name
            product.price = price
            product.description = request.form.get("description", "").strip()
            product.category_id = cat_id
            product.in_stock = request.form.get("in_stock") == "1"
            if img:
                product.image_url = img
        else:
            product = Product(
                name=name,
                price=price,
                description=request.form.get("description", "").strip(),
                category_id=cat_id,
                image_url=img or "",
                in_stock=in_stock,
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
        if st in ("new", "await_pay", "paid", "done", "cancel"):
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




@app.route("/admin/payments")
@admin_required
def admin_payments():
    edit_id = request.args.get("edit", type=int)
    edit = db.session.get(PaymentMethod, edit_id) if edit_id else None
    methods = PaymentMethod.query.order_by(PaymentMethod.position, PaymentMethod.id).all()
    return render_template("admin_payments.html", admin_tab="payments", methods=methods, edit=edit)


@app.route("/admin/payments/save", methods=["POST"])
@admin_required
def admin_payment_save():
    title = request.form.get("title", "").strip()[:80]
    if not title:
        flash("Укажите название", "danger")
        return redirect(url_for("admin_payments"))
    pid = request.form.get("id", type=int)
    m = db.session.get(PaymentMethod, pid) if pid else None
    if not m:
        m = PaymentMethod(position=PaymentMethod.query.count())
        db.session.add(m)
    m.title = title
    m.details = request.form.get("details", "").strip()
    m.link_url = request.form.get("link_url", "").strip()[:500]
    m.active = bool(request.form.get("active"))
    if request.form.get("remove_qr"):
        m.qr_url = ""
    f = request.files.get("qr")
    if f and f.filename:
        path = save_upload(f)
        if path:
            m.qr_url = path
    db.session.commit()
    flash("Способ оплаты сохранён", "success")
    return redirect(url_for("admin_payments"))


@app.route("/admin/payments/<int:pid>/toggle", methods=["POST"])
@admin_required
def admin_payment_toggle(pid):
    m = db.session.get(PaymentMethod, pid)
    if m:
        m.active = not m.active
        db.session.commit()
    return redirect(url_for("admin_payments"))


@app.route("/admin/payments/<int:pid>/delete", methods=["POST"])
@admin_required
def admin_payment_delete(pid):
    m = db.session.get(PaymentMethod, pid)
    if m:
        db.session.delete(m)
        db.session.commit()
        flash("Удалено", "success")
    return redirect(url_for("admin_payments"))




@app.route("/admin/seed-demo", methods=["POST", "GET"])
@admin_required
def admin_seed_demo():
    """Добавить демо-товары с фото (если их ещё нет по имени)."""
    demo = [
        ("Набор гелевых ручек 12 шт", "Письменные принадлежности", 180,
         "Яркий набор гелевых ручек для школы и заметок.", "pens.jpg"),
        ("Скетчбук А5 на пружине", "Тетради и блокноты", 250,
         "Плотная бумага, удобен для набросков.", "notebook.jpg"),
        ("Набор маркеров 6 цветов", "Для творчества", 320,
         "Акриловые маркеры, насыщенный цвет.", "markers.jpg"),
        ("Рюкзак школьный", "Рюкзаки и сумки", 1890,
         "Лёгкий рюкзак с отделением для тетрадей.", "backpack.jpg"),
        ("Набор карандашей HB–6B", "Карандаши и грифели", 150,
         "Графитные карандаши для учёбы и рисования.", "pencils.jpg"),
        ("Степлер металлический", "Офисные товары", 220,
         "Надёжный степлер для бумаги.", "stapler.jpg"),
        ("Набор красок гуашь 12 цв", "Краски и кисти", 280,
         "Гуашь для ИЗО и творчества.", "paints.jpg"),
        ("Стикеры-закладки набор", "Стикеры и закладки", 90,
         "Клейкие закладки разных цветов.", "sticky.jpg"),
    ]
    added = 0
    for name, cat_name, price, desc, img in demo:
        if Product.query.filter_by(name=name).first():
            continue
        cat = Category.query.filter_by(name=cat_name).first()
        if not cat:
            cat = Category(name=cat_name)
            db.session.add(cat)
            db.session.flush()
        db.session.add(Product(
            name=name,
            description=desc,
            price=price,
            image_url=f"/static/img/products/{img}",
            category_id=cat.id,
            in_stock=True,
        ))
        added += 1
    db.session.commit()
    flash(f"Добавлено товаров: {added}", "success")
    return redirect(url_for("admin_products"))


@app.route("/health")
def health():
    return jsonify(ok=True, site=SITE_NAME)


with app.app_context():
    try:
        db.create_all()
        # soft migrate payment_method for old SQLite DBs
        try:
            from sqlalchemy import text as sql_text
            cols = [r[1] for r in db.session.execute(sql_text("PRAGMA table_info('order')")).fetchall()]
            if "token" not in cols:
                db.session.execute(sql_text("ALTER TABLE 'order' ADD COLUMN token VARCHAR(40) DEFAULT ''"))
                db.session.commit()
            if "payment_method" not in cols:
                db.session.execute(sql_text("ALTER TABLE 'order' ADD COLUMN payment_method VARCHAR(40) DEFAULT 'cash'"))
                db.session.commit()
        except Exception as mig_e:
            print("migrate", mig_e)
        existing = {c.name for c in Category.query.all()}
        for n in DEFAULT_CATEGORIES:
            if n not in existing:
                db.session.add(Category(name=n))
        db.session.commit()

        # демо-товары с фото (один раз, если каталог пуст)
        if Product.query.count() == 0:
            demo = [
                ("Набор гелевых ручек 12 шт", "Письменные принадлежности", 180,
                 "Яркий набор гелевых ручек для школы и заметок. Пишут мягко, не мажутся.",
                 "pens.jpg"),
                ("Скетчбук А5 на пружине", "Тетради и блокноты", 250,
                 "Плотная бумага 120 г/м², удобен для набросков и ежедневных записей.",
                 "notebook.jpg"),
                ("Набор маркеров 6 цветов", "Для творчества", 320,
                 "Акриловые маркеры для бумаги, дерева и пластика. Насыщенный цвет.",
                 "markers.jpg"),
                ("Рюкзак школьный", "Рюкзаки и сумки", 1890,
                 "Лёгкий рюкзак с отделением для тетрадей и карманом для бутылки.",
                 "backpack.jpg"),
                ("Набор карандашей HB–6B", "Карандаши и грифели", 150,
                 "Графитные карандаши разной мягкости для учёбы и рисования.",
                 "pencils.jpg"),
                ("Степлер металлический", "Офисные товары", 220,
                 "Надёжный степлер для бумаги, скобы №24/6 в комплекте не входят.",
                 "stapler.jpg"),
                ("Набор красок гуашь 12 цв", "Краски и кисти", 280,
                 "Гуашь для уроков ИЗО и творчества дома. Яркие цвета, удобные баночки.",
                 "paints.jpg"),
                ("Стикеры-закладки набор", "Стикеры и закладки", 90,
                 "Клейкие закладки разных цветов для учебников и документов.",
                 "sticky.jpg"),
            ]
            for name, cat_name, price, desc, img in demo:
                cat = Category.query.filter_by(name=cat_name).first()
                db.session.add(Product(
                    name=name,
                    description=desc,
                    price=price,
                    image_url=f"/static/img/products/{img}",
                    category_id=cat.id if cat else None,
                    in_stock=True,
                ))
            db.session.commit()
            print("demo products seeded")
        # Сохраняем каталог из репозитория и добавляем позиции без удаления существующих товаров.
        existing_catalog_images = {
            p.image_url for p in Product.query.filter(Product.image_url.like("/static/img/catalog/%")).all()
        }
        catalog_added = 0
        for item in CATALOG_PRODUCTS:
            if item["image_url"] in existing_catalog_images:
                continue
            category = Category.query.filter_by(name=item["category"]).first()
            db.session.add(Product(
                name=item["name"],
                description=item["description"],
                price=0,
                image_url=item["image_url"],
                category_id=category.id if category else None,
                in_stock=True,
            ))
            catalog_added += 1
        if catalog_added:
            db.session.commit()
            print(f"catalog products seeded: {catalog_added}")
    except Exception as e:
        print("init", e)




# ============================ TELEGRAM BOT ============================
def tg_api(method, **payload):
    if not TELEGRAM_TOKEN:
        return {}
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}",
            json=payload,
            timeout=30,
        )
        return r.json()
    except Exception as e:
        print("tg_api", e)
        return {}


def tg_is_admin(chat_id):
    return str(chat_id) in [str(x) for x in ADMIN_IDS]


def bot_state(chat_id):
    st = BotState.query.filter_by(chat_id=str(chat_id)).first()
    if not st:
        st = BotState(chat_id=str(chat_id), step="idle")
        db.session.add(st)
        db.session.commit()
    return st


def pending_products():
    """Товары без цены или скрытые — ждут разметки в боте."""
    return (
        Product.query.filter(
            db.or_(Product.price <= 0, Product.in_stock.is_(False))
        )
        .order_by(Product.created_at.asc())
        .all()
    )


def product_keyboard(pid):
    return {
        "inline_keyboard": [
            [
                {"text": "💰 Цена", "callback_data": f"price:{pid}"},
                {"text": "✏️ Имя", "callback_data": f"rename:{pid}"},
            ],
            [
                {"text": "🗑 Удалить", "callback_data": f"del:{pid}"},
                {"text": "⏭ Далее", "callback_data": f"next:{pid}"},
            ],
            [{"text": "✅ В каталог (как есть)", "callback_data": f"publish:{pid}"}],
        ]
    }


def resolve_product_image_path(p):
    """Локальный путь к файлу фото товара или None."""
    img = (p.image_url or "").strip()
    if not img:
        return None
    # /uploads/xxx.jpg
    if img.startswith("/uploads/"):
        local = os.path.join(UPLOAD, img.split("/uploads/")[-1])
        if os.path.isfile(local):
            return local
    # /static/img/products/xxx.jpg
    if img.startswith("/static/"):
        local = os.path.join(_BASE, img.lstrip("/").replace("/", os.sep))
        if os.path.isfile(local):
            return local
        # alternate under static/
        local2 = os.path.join(_BASE, "static", img.split("/static/")[-1])
        if os.path.isfile(local2):
            return local2
    # bare filename in uploads
    local = os.path.join(UPLOAD, os.path.basename(img))
    if os.path.isfile(local):
        return local
    return None


def tg_send_photo(chat_id, photo, caption="", reply_markup=None):
    """photo: путь к файлу, http(s) URL или file_id."""
    if not TELEGRAM_TOKEN:
        return {}
    data = {"chat_id": chat_id, "caption": caption[:1024], "parse_mode": "HTML"}
    if reply_markup:
        import json as _json
        data["reply_markup"] = _json.dumps(reply_markup)
    try:
        if isinstance(photo, str) and os.path.isfile(photo):
            with open(photo, "rb") as f:
                r = requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                    data=data,
                    files={"photo": f},
                    timeout=60,
                )
            return r.json()
        data["photo"] = photo
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
            data={k: v for k, v in data.items()},
            timeout=30,
        )
        # reply_markup as json in form
        return r.json()
    except Exception as e:
        print("tg_send_photo", e)
        return {}


def send_product_card(chat_id, p):
    price_txt = f"{p.price:,.0f} сом".replace(",", " ") if p.price and p.price > 0 else "без цены"
    status = "в каталоге" if p.in_stock and p.price > 0 else "черновик"
    caption = "<b>%s</b>\nID: %s\nЦена: %s\nСтатус: %s\n\nНажмите «Цена» и пришлите число, или «Имя» / «Удалить»." % (p.name, p.id, price_txt, status)
    kb = product_keyboard(p.id)
    local = resolve_product_image_path(p)
    if local:
        r = tg_send_photo(chat_id, local, caption=caption, reply_markup=kb)
        if r.get("ok"):
            return r
    img = (p.image_url or "").strip()
    if img.startswith("/uploads/") or img.startswith("/static/"):
        base = os.environ.get("SITE_URL", "").rstrip("/")
        if base:
            img = base + img
    if img.startswith("http://") or img.startswith("https://"):
        r = tg_send_photo(chat_id, img, caption=caption, reply_markup=kb)
        if r.get("ok"):
            return r
    extra = "\n\n⚠️ Фото не найдено на сервере" if p.image_url else ""
    return tg_api("sendMessage", chat_id=chat_id, text=caption + extra, parse_mode="HTML", reply_markup=kb)


def send_next_pending(chat_id, after_id=None):
    items = pending_products()
    if after_id:
        rest = [p for p in items if p.id != after_id]
        # prefer next after current in list order
        ids = [p.id for p in items]
        if after_id in ids:
            i = ids.index(after_id)
            rest = items[i + 1 :] + items[:i]
        items = rest if rest else []
    if not items:
        tg_api(
            "sendMessage",
            chat_id=chat_id,
            text="✅ Очередь пуста. Все товары с ценой и в каталоге.\n\n"
            "Пришлите <b>фото</b> — создам новый товар, потом зададите имя и цену.",
            parse_mode="HTML",
        )
        return
    p = items[0]
    send_product_card(chat_id, p)


@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json(silent=True) or {}
    # callback buttons
    if "callback_query" in data:
        cq = data["callback_query"]
        chat_id = cq.get("message", {}).get("chat", {}).get("id")
        uid = cq.get("from", {}).get("id")
        cb = (cq.get("data") or "").strip()
        tg_api("answerCallbackQuery", callback_query_id=cq.get("id"))
        if not tg_is_admin(uid):
            return jsonify(ok=True)
        st = bot_state(uid)
        if cb.startswith("price:"):
            pid = int(cb.split(":")[1])
            st.step = "wait_price"
            st.product_id = pid
            db.session.commit()
            tg_api("sendMessage", chat_id=chat_id, text="💰 Пришлите цену числом (например 250):")
        elif cb.startswith("rename:"):
            pid = int(cb.split(":")[1])
            st.step = "wait_rename"
            st.product_id = pid
            db.session.commit()
            tg_api("sendMessage", chat_id=chat_id, text="✏️ Пришлите новое название товара:")
        elif cb.startswith("del:"):
            pid = int(cb.split(":")[1])
            p = db.session.get(Product, pid)
            if p:
                name = p.name
                db.session.delete(p)
                db.session.commit()
                st.step = "idle"
                st.product_id = None
                db.session.commit()
                tg_api("sendMessage", chat_id=chat_id, text=f"🗑 Удалён: {name}")
            send_next_pending(chat_id, after_id=pid)
        elif cb.startswith("next:"):
            pid = int(cb.split(":")[1])
            st.step = "idle"
            db.session.commit()
            send_next_pending(chat_id, after_id=pid)
        elif cb.startswith("publish:"):
            pid = int(cb.split(":")[1])
            p = db.session.get(Product, pid)
            if p and p.price > 0:
                p.in_stock = True
                db.session.commit()
                tg_api("sendMessage", chat_id=chat_id, text=f"✅ «{p.name}» в каталоге за {p.price:,.0f} сом".replace(",", " "))
            elif p:
                tg_api("sendMessage", chat_id=chat_id, text="Сначала укажите цену (кнопка «Цена»).")
            send_next_pending(chat_id, after_id=pid)
        return jsonify(ok=True)

    msg = data.get("message") or data.get("edited_message") or {}
    chat = msg.get("chat") or {}
    chat_id = chat.get("id")
    uid = (msg.get("from") or {}).get("id")
    if not chat_id or not uid:
        return jsonify(ok=True)
    if not tg_is_admin(uid):
        tg_api("sendMessage", chat_id=chat_id, text="⛔ Нет доступа. Добавьте свой ID в TELEGRAM_ADMIN_IDS.")
        return jsonify(ok=True)

    text_msg = (msg.get("text") or "").strip()
    st = bot_state(uid)

    if text_msg in ("/start", "/help"):
        st.step = "idle"
        db.session.commit()
        tg_api(
            "sendMessage",
            chat_id=chat_id,
            text=(
                "👋 Бот магазина «Мир канцелярии»\n\n"
                "/tovary — товары по очереди (цена / имя / удалить)\n"
                "Пришлите <b>фото</b> — новый товар в очередь\n\n"
                "На каждом товаре кнопки:\n"
                "💰 Цена · ✏️ Имя · 🗑 Удалить · ⏭ Далее · ✅ В каталог"
            ),
            parse_mode="HTML",
        )
        return jsonify(ok=True)

    if text_msg in ("/tovary", "/queue", "/next"):
        st.step = "idle"
        db.session.commit()
        send_next_pending(chat_id)
        return jsonify(ok=True)

    # waiting price
    if st.step == "wait_price" and st.product_id:
        raw = text_msg.replace(" ", "").replace(",", ".")
        try:
            price = float(raw)
            if price < 0:
                raise ValueError
        except ValueError:
            tg_api("sendMessage", chat_id=chat_id, text="Нужно число, например: 150")
            return jsonify(ok=True)
        p = db.session.get(Product, st.product_id)
        if p:
            p.price = price
            p.in_stock = True
            db.session.commit()
            tg_api(
                "sendMessage",
                chat_id=chat_id,
                text=f"✅ «{p.name}» — {price:,.0f} сом, выложен в каталог.".replace(",", " "),
            )
        st.step = "idle"
        pid = st.product_id
        st.product_id = None
        db.session.commit()
        send_next_pending(chat_id, after_id=pid)
        return jsonify(ok=True)

    # waiting rename
    if st.step == "wait_rename" and st.product_id:
        if not text_msg:
            tg_api("sendMessage", chat_id=chat_id, text="Пришлите название текстом.")
            return jsonify(ok=True)
        p = db.session.get(Product, st.product_id)
        if p:
            p.name = text_msg[:200]
            db.session.commit()
            tg_api("sendMessage", chat_id=chat_id, text=f"✏️ Новое имя: {p.name}")
            send_product_card(chat_id, p)
        st.step = "idle"
        st.product_id = None
        db.session.commit()
        return jsonify(ok=True)

    # photo -> new product draft
    photos = msg.get("photo") or []
    if photos:
        # largest photo
        file_id = photos[-1]["file_id"]
        fi = tg_api("getFile", file_id=file_id)
        fp = (fi.get("result") or {}).get("file_path")
        local_url = ""
        if fp:
            try:
                r = requests.get(f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{fp}", timeout=60)
                if r.ok:
                    ext = fp.rsplit(".", 1)[-1].lower() if "." in fp else "jpg"
                    if ext not in ALLOWED_EXT:
                        ext = "jpg"
                    name = f"{uuid.uuid4().hex}.{ext}"
                    with open(os.path.join(UPLOAD, name), "wb") as f:
                        f.write(r.content)
                    local_url = "/uploads/" + name
            except Exception as e:
                print("photo save", e)
        p = Product(
            name="Новый товар",
            description="",
            price=0,
            image_url=local_url,
            in_stock=False,
        )
        db.session.add(p)
        db.session.commit()
        st.step = "wait_rename"
        st.product_id = p.id
        db.session.commit()
        tg_api(
            "sendMessage",
            chat_id=chat_id,
            text="📷 Товар создан (черновик). Пришлите <b>название</b>:",
            parse_mode="HTML",
        )
        return jsonify(ok=True)

    # wait name after photo already handled as wait_rename
    if text_msg:
        tg_api(
            "sendMessage",
            chat_id=chat_id,
            text="Команды: /tovary — очередь товаров. Или пришлите фото нового товара.",
        )
    return jsonify(ok=True)


@app.route("/admin/bot/setup", methods=["POST", "GET"])
@admin_required
def admin_bot_setup():
    """Ставит webhook на этот сайт. SITE_URL или авто из request."""
    base = os.environ.get("SITE_URL", "").rstrip("/") or request.url_root.rstrip("/")
    url = base + "/telegram-webhook"
    r = tg_api("setWebhook", url=url)
    flash(f"Webhook: {url} → {r}", "success" if r.get("ok") else "danger")
    return redirect(url_for("admin_dashboard"))



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
