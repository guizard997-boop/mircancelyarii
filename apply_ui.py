#!/usr/bin/env python3
"""Integrate the kawaii theme and catalog seed into this Flask/Jinja project.

Safe to rerun. Creates app.py.bak before the first app.py change.
"""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.py"
BASE = ROOT / "templates" / "base.html"
CARD = ROOT / "templates" / "partials" / "product_card.html"
CSS = ROOT / "static" / "css" / "kawaii.css"
JS = ROOT / "static" / "js" / "kawaii.js"

KAWAII_CSS = r'''/* Kawaii pink layer for the existing Jinja storefront. */
:root {
  --brand: #E0457F;
  --brand2: #F472B6;
  --brand-dark: #B8326A;
  --pink: #EC5C99;
  --pink2: #FFA1C4;
  --soft: #FFF8FB;
  --lilac: #FFD6E7;
  --ink: #4A2336;
  --muted: #8B6B7A;
  --grad-top: linear-gradient(90deg, #B8326A 0%, #E0457F 55%, #F472B6 100%);
  --grad-btn: linear-gradient(135deg, #F472B6 0%, #E0457F 58%, #C63874 100%);
  --grad-hero: linear-gradient(120deg, #FFF3F8 0%, #FFE4EF 48%, #FFF8FB 100%);
  --grad-banner: linear-gradient(100deg, #B8326A 0%, #D84081 55%, #F472B6 100%);
  --shadow: 0 14px 40px rgba(224, 69, 127, .14);
}
body { background: var(--soft); color: var(--ink); }
.topbar { background: var(--grad-top); }
.header { border-bottom-color: #FFD6E7; }
.logo-mark { background: linear-gradient(145deg, #FFA1C4, #E0457F); box-shadow: 0 6px 16px rgba(224,69,127,.25); }
.logo-text { color: var(--brand-dark); }
.nav a:hover, .icon-btn:hover { background: #FFF0F6; color: var(--brand); }
.nav a.active { background: var(--grad-btn); }
.search-form input { border-color: #FFD6E7; }
.search-form input:focus { border-color: #F472B6; box-shadow: 0 0 0 3px rgba(244,114,182,.2); }
.btn { background: var(--grad-btn); box-shadow: 0 8px 22px rgba(224,69,127,.24); }
.btn-pink { background: linear-gradient(135deg,#FFA1C4,#E0457F,#B8326A); }
.hero { background: var(--grad-hero); }
.hero::before { background: radial-gradient(circle,rgba(244,114,182,.20),transparent 70%); }
.hero-script { color: #D84E86; }
.hero-title { color: #4A2336; }
.hero-sub, .muted { color: var(--muted); }
.hero-feat, .cat-card { border-color: #FFD6E7; }
.hero-neon { color: #B8326A; }
.cat-card:hover, .prod-card:hover { border-color: #F7A8C8; box-shadow: 0 16px 36px rgba(224,69,127,.16); }
.cat-thumb { background: linear-gradient(135deg,#FFF0F6,#FFD6E7); }
.prod-card { border: 1px solid #F8DFE9; border-radius: 22px; }
.prod-heart { color: #E0457F; }
.prod-price-now { color: #B8326A; }
.prod-add { border: 0; border-radius: 50%; width: 42px; height: 42px; color: #fff; background: var(--grad-btn); box-shadow: 0 4px 0 #B8326A; cursor: pointer; }
.prod-add:hover { transform: translateY(-1px); filter: brightness(1.04); }
.banner-pre { background: var(--grad-banner); }
.flash-ok { border-color: #F7A8C8; background: #FFF0F6; color: #8A2852; }
.cart-badge { background: #E0457F; }
.bottom-nav { border-color: #FFD6E7; }
.footer { background: #FFF0F6; }
.footer-title { color: #B8326A; }
#toasts { position: fixed; right: 16px; bottom: 84px; z-index: 1000; display: grid; gap: 8px; }
.kawaii-toast { max-width: min(360px, calc(100vw - 32px)); padding: 12px 16px; border: 1px solid #FFD6E7; border-radius: 18px; background: #fff; color: #4A2336; box-shadow: 0 12px 30px rgba(74,35,54,.16); animation: toast-in .2s ease-out; }
.kawaii-toast.out { opacity: 0; transform: translateY(8px); transition: .22s ease; }
@keyframes toast-in { from { opacity: 0; transform: translateY(8px) scale(.98); } to { opacity: 1; transform: none; } }
@media (max-width: 720px) { main { padding-bottom: 84px; } #toasts { bottom: 96px; } }
'''

KAWAII_JS = r'''(() => {
  const toastRoot = document.getElementById('toasts');
  const showToast = (message) => {
    if (!toastRoot) return;
    const item = document.createElement('div');
    item.className = 'kawaii-toast';
    item.setAttribute('role', 'status');
    item.textContent = `💖 ${message}`;
    toastRoot.appendChild(item);
    window.setTimeout(() => {
      item.classList.add('out');
      window.setTimeout(() => item.remove(), 240);
    }, 2600);
  };

  document.addEventListener('submit', async (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement) || !form.matches('[data-ajax-cart]')) return;
    event.preventDefault();
    const button = form.querySelector('button[type="submit"]');
    if (button) button.disabled = true;
    try {
      const response = await fetch(form.action, {
        method: 'POST', body: new FormData(form),
        headers: { 'X-Requested-With': 'fetch' }, credentials: 'same-origin'
      });
      if (!response.ok) throw new Error('Request failed');
      const result = await response.json();
      document.querySelectorAll('[data-cart-badge]').forEach((badge) => {
        badge.textContent = String(result.count || 0);
        badge.hidden = !result.count;
      });
      showToast(`«${result.name}» добавлен в предзаказ`);
    } catch (_) {
      showToast('Не удалось добавить товар. Попробуйте ещё раз.');
    } finally {
      if (button) button.disabled = false;
    }
  });
})();
'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count > 1:
        raise ValueError(f"Expected one {label} anchor, found {count}")
    return text if count == 0 else text.replace(old, new, 1)


def main() -> int:
    for path in (APP, BASE, CARD):
        if not path.is_file():
            print(f"Required project file missing: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1

    app = APP.read_text(encoding="utf-8")
    if "from catalog_seed import seed as seed_catalog" not in app:
        if "import os\n" not in app:
            print("Could not find the app.py import anchor; no files changed.", file=sys.stderr)
            return 1
        app = app.replace("import os\n", "import os\nfrom catalog_seed import seed as seed_catalog\n", 1)
    seed_anchor = '''        db.session.commit()
    except Exception as e:
        print("init", e)'''
    if "seed_catalog(app, db, Product, Category)" not in app:
        if app.count(seed_anchor) != 1:
            print("Could not find the database initialization anchor; no files changed.", file=sys.stderr)
            return 1
        app = app.replace(seed_anchor, '''        db.session.commit()
        seed_catalog(app, db, Product, Category)
    except Exception as e:
        print("init", e)''', 1)
    cart_anchor = '''    session["cart"] = c
    flash(f"{p.name} добавлен в предзаказ", "success")
    return redirect(request.referrer or url_for("catalog"))'''
    if "X-Requested-With" not in app:
        if app.count(cart_anchor) != 1:
            print("Could not find the cart-add route anchor; no files changed.", file=sys.stderr)
            return 1
        app = app.replace(cart_anchor, '''    session["cart"] = c
    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify(ok=True, name=p.name, count=cart_count())
    flash(f"{p.name} добавлен в предзаказ", "success")
    return redirect(request.referrer or url_for("catalog"))''', 1)

    base = BASE.read_text(encoding="utf-8")
    stylesheet = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/style.css\') }}">'
    if "css/kawaii.css" not in base:
        if stylesheet not in base:
            print("Could not find the stylesheet anchor; no files changed.", file=sys.stderr)
            return 1
        base = base.replace(stylesheet, stylesheet + "\n<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/kawaii.css') }}\">", 1)
    if 'id="toasts"' not in base:
        if "</body>" not in base:
            print("Could not find the closing body tag; no files changed.", file=sys.stderr)
            return 1
        base = base.replace("</body>", '''<div id="toasts" aria-live="polite" aria-atomic="true"></div>
<script src="{{ url_for('static', filename='js/kawaii.js') }}" defer></script>
</body>''', 1)
    base = base.replace("👑", "🎀")
    base = base.replace('<span class="cart-badge">{{ cart_count }}</span>', '<span class="cart-badge" data-cart-badge>{{ cart_count }}</span>')

    old_card = CARD.read_text(encoding="utf-8")
    new_card = '''<article class="prod-card">
  <a href="{{ url_for('product_detail', pid=p.id) }}" class="prod-link">
    <div class="prod-img">
      <img src="{{ p.image_url or 'https://placehold.co/400x400/fff0f6/e0457f?text=+' }}" alt="{{ p.name }}" loading="lazy"
           onerror="this.src='https://placehold.co/400x400/fff0f6/e0457f?text=+'">
      <span class="prod-heart" aria-hidden="true">♥</span>
    </div>
    <div class="prod-body">
      <div class="prod-name">{{ p.name }}</div>
      <div class="prod-price">
        {% if p.price and p.price > 0 %}<span class="prod-price-now">{{ '{:,.0f}'.format(p.price).replace(',', ' ') }} сом</span>{% else %}<span class="prod-price-now">Цена по запросу</span>{% endif %}
      </div>
    </div>
  </a>
  <form action="{{ url_for('cart_add', pid=p.id) }}" method="post" data-ajax-cart>
    <input type="hidden" name="qty" value="1">
    <button class="prod-add" type="submit" aria-label="Добавить {{ p.name }} в предзаказ">＋</button>
  </form>
</article>
'''
    if "data-ajax-cart" not in old_card:
        old_card = new_card

    if APP.read_text(encoding="utf-8") != app and not (ROOT / "app.py.bak").exists():
        shutil.copy2(APP, ROOT / "app.py.bak")
    APP.write_text(app, encoding="utf-8")
    BASE.write_text(base, encoding="utf-8")
    CARD.write_text(new_card, encoding="utf-8")
    CSS.parent.mkdir(parents=True, exist_ok=True)
    CSS.write_text(KAWAII_CSS, encoding="utf-8")
    JS.parent.mkdir(parents=True, exist_ok=True)
    JS.write_text(KAWAII_JS, encoding="utf-8")
    print("Kawaii theme, async cart add, and catalog seed integrated for this Jinja app.")
    print("Run python app.py (or the existing Procfile command) to test locally.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
