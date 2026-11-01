# ============================================================
# KAWAII PINK UI для «Мир канцелярии»  (заменяет ui_upgrade.py)
# В app.py заменить:
#   1) LAYOUT = '''...'''        -> LAYOUT ниже
#   2) def product_card(p)       -> product_card ниже
#   3) маршрут add_to_cart       -> add_to_cart ниже
#   4) маршрут index()           -> index ниже
# Цвета tailwind (brand/brand2/accent/soft) перекрашены в розовый,
# поэтому админка, каталог, корзина и оформление перекрасятся сами.
# ============================================================

LAYOUT = '''
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#FF8FC0">
<title>{{ title }} — Мир канцелярии</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={theme:{extend:{colors:{brand:'#E0457F',brand2:'#FF7EB6',accent:'#FF5C8A',soft:'#FFF0F6'}}}}</script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
@import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@600;700&family=Nunito:wght@400;600;700;800&display=swap');
:root{--ink:#5A2A44;--mute:#9A5F7E;--line:#FFD0E3;--pink:#FF8FC0;--deep:#E0457F;--soft:#FFF0F6}
html{scroll-behavior:smooth}
body{font-family:'Nunito',system-ui,sans-serif;color:var(--ink);background-color:#FFF6FA;
 background-image:radial-gradient(#FFD6E7 1.6px,transparent 1.8px);background-size:26px 26px;padding-bottom:env(safe-area-inset-bottom)}
h1,h2,h3,.kawaii-font{font-family:'Comfortaa','Nunito',sans-serif;font-weight:700}
::selection{background:#FFC2DB}
:focus-visible{outline:3px dashed #E0457F;outline-offset:3px;border-radius:14px}

/* перекраска жёстких цветов из старых страниц */
.text-gray-900,.text-gray-800,.text-gray-700,.text-gray-600{color:var(--ink)!important}
.text-gray-500,.text-gray-400,.text-gray-300{color:var(--mute)!important}
.border-gray-100,.border-gray-200,.border-violet-100,.border-orange-100,.border-white\\/50,.border,.border-t,.border-b{border-color:var(--line)!important}
.divide-gray-100>*{border-color:var(--line)!important}
.bg-white{background-color:#fff}
.bg-gray-50,.bg-violet-50,.bg-orange-50,.bg-violet-100{background-color:#FFF0F6!important}
.bg-pink-50{background-color:#FFE4F0!important}.bg-sky-50{background-color:#FFEFE5!important}
.bg-amber-50{background-color:#FFF3D9!important}.bg-emerald-50{background-color:#F1E8FF!important}.bg-rose-50{background-color:#FFE0E6!important}
.rounded-xl{border-radius:1.1rem}.rounded-2xl{border-radius:1.6rem}.rounded-3xl{border-radius:2.2rem}
.shadow-sm,.shadow-lg,.shadow{box-shadow:0 4px 0 #FFD0E3!important}
.bg-gradient-to-r,.bg-gradient-to-br{background-image:linear-gradient(135deg,#FFE4F0,#FFF3D9)!important}
.text-emerald-500,.text-sky-500,.text-amber-500{color:#E0457F!important}
input,select,textarea{border:2px solid var(--line)!important;border-radius:1.1rem!important;background:#fff}
input:focus,select:focus,textarea:focus{border-color:#FF8FC0!important;box-shadow:0 0 0 4px #FFE0EE!important;outline:none}

/* кнопки-«конфетки» */
.btn-grad,.btn-orange{background:linear-gradient(180deg,#FF8FC0,#E0457F);box-shadow:0 5px 0 #B8326A;border-radius:999px!important;transition:transform .12s,box-shadow .12s}
.btn-orange{background:linear-gradient(180deg,#FFA3C4,#FF5C8A);box-shadow:0 5px 0 #CC3A68}
.btn-grad:hover,.btn-orange:hover{filter:brightness(1.05)}
.btn-grad:active,.btn-orange:active{transform:translateY(4px);box-shadow:0 1px 0 #B8326A}

/* карточки-«стикеры» */
.card{border:2px solid var(--line)!important;box-shadow:0 6px 0 #FFC2DB!important;transition:transform .18s,box-shadow .18s}
@media (hover:hover){.card:hover{transform:translateY(-5px) rotate(-.6deg);box-shadow:0 11px 0 #FFB3D1!important}}
.card img{transition:transform .4s}
@media (hover:hover){.card:hover img{transform:scale(1.07)}}

.sticker{display:inline-block;background:#fff;border:2px solid var(--line);border-radius:999px;padding:.25rem .9rem;font-weight:800;font-size:.8rem;color:var(--deep);box-shadow:0 3px 0 #FFD0E3}
.skel{background:linear-gradient(90deg,#FFF0F6 25%,#FFD6E7 37%,#FFF0F6 63%);background-size:400% 100%;animation:sh 1.4s infinite}
@keyframes sh{0%{background-position:100% 50%}100%{background-position:0 50%}}
.rv{opacity:0;transform:translateY(14px);transition:opacity .5s,transform .5s}.rv.in{opacity:1;transform:none}
@keyframes floaty{0%,100%{transform:translateY(0) rotate(-4deg)}50%{transform:translateY(-12px) rotate(4deg)}}
.floaty{animation:floaty 4s ease-in-out infinite}.floaty.d2{animation-delay:-1.3s}.floaty.d3{animation-delay:-2.6s}
@keyframes blink{0%,92%,100%{transform:scaleY(1)}96%{transform:scaleY(.1)}}
.eye{transform-origin:center;transform-box:fill-box;animation:blink 5s infinite}

/* тост и сердечки */
#toasts{position:fixed;left:50%;transform:translateX(-50%);bottom:92px;z-index:100;display:flex;flex-direction:column;gap:8px;align-items:center;pointer-events:none;width:calc(100% - 24px);max-width:420px}
.toast{pointer-events:auto;background:#fff;color:var(--ink);border:2px solid #FF8FC0;border-radius:999px;padding:11px 18px;font-size:14px;font-weight:800;display:flex;gap:10px;align-items:center;box-shadow:0 5px 0 #FFB3D1;animation:tin .28s cubic-bezier(.3,1.6,.5,1) both}
.toast.out{animation:tout .25s both}
@keyframes tin{from{opacity:0;transform:translateY(14px) scale(.9)}to{opacity:1;transform:none}}
@keyframes tout{to{opacity:0;transform:translateY(8px)}}
.heart{position:fixed;z-index:120;pointer-events:none;font-size:18px;animation:hf .9s ease-out forwards}
@keyframes hf{to{opacity:0;transform:translate(var(--dx),-70px) scale(1.4)}}
@keyframes pop{40%{transform:scale(1.4)}}
.pop{animation:pop .35s}
.line-clamp-2{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}.rv{opacity:1;transform:none}html{scroll-behavior:auto}}
@media (max-width:767px){body{padding-bottom:88px}}
</style>
</head>
<body class="min-h-screen flex flex-col">
<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:z-[200] focus:bg-white focus:p-3 focus:rounded-xl">Перейти к содержимому</a>

<header class="sticky top-0 z-50" style="background:rgba(255,246,250,.92);backdrop-filter:blur(10px);border-bottom:3px dotted #FFB3D1">
<div class="max-w-7xl mx-auto px-4 h-16 flex items-center gap-3">
<a href="/" class="flex items-center gap-2 flex-shrink-0" aria-label="Мир канцелярии — на главную">
<div class="w-11 h-11 rounded-full btn-grad flex items-center justify-center text-xl" style="box-shadow:0 4px 0 #B8326A">🎀</div>
<div class="hidden sm:block leading-tight kawaii-font"><div class="text-brand text-[15px]">Мир</div><div class="text-[11px] text-gray-500 -mt-0.5">канцелярии</div></div>
</a>
<a href="/catalog" class="hidden md:inline-flex items-center gap-1.5 btn-grad text-white text-sm font-bold px-5 py-2.5"><i class="fas fa-heart text-xs"></i> Каталог</a>
<form action="/catalog" method="get" class="flex-1 max-w-xl" role="search">
<div class="relative">
<input id="q" type="search" name="q" value="{{ request.args.get('q','') }}" placeholder="Найти ручки, тетради, наклейки…" autocomplete="off" class="w-full pl-11 pr-4 py-2.5 text-sm rounded-full">
<span class="absolute left-4 top-1/2 -translate-y-1/2">🔍</span>
</div>
</form>
<a href="/cart" class="relative hidden md:flex w-11 h-11 items-center justify-center rounded-full bg-white" style="border:2px solid #FFD0E3;box-shadow:0 3px 0 #FFD0E3" aria-label="Предзаказ">
<span class="text-xl">🛍️</span>
<span data-cart-badge class="absolute -top-1 -right-1 bg-accent text-white text-[10px] font-bold rounded-full h-5 min-w-5 px-1 flex items-center justify-center {% if not cart_count %}hidden{% endif %}">{{ cart_count }}</span>
</a>
</div>
</header>

{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}<div id="flash" class="hidden">{% for cat,msg in messages %}<i data-cat="{{ cat }}">{{ msg }}</i>{% endfor %}</div>{% endif %}
{% endwith %}

<main id="main" class="flex-1">{{ content|safe }}</main>

<!-- волна перед подвалом -->
<svg viewBox="0 0 1440 60" preserveAspectRatio="none" class="w-full h-8 mt-16 block" aria-hidden="true"><path fill="#FFD6E7" d="M0 30c60 20 120 20 180 0s120-20 180 0 120 20 180 0 120-20 180 0 120 20 180 0 120-20 180 0 120 20 180 0V60H0z"/></svg>
<footer style="background:#FFD6E7;color:var(--ink)">
<div class="max-w-7xl mx-auto px-4 py-10 grid sm:grid-cols-3 gap-8 text-sm">
<div>
<div class="flex items-center gap-2 mb-3"><div class="w-9 h-9 rounded-full btn-grad flex items-center justify-center">🎀</div><span class="kawaii-font text-lg">Мир канцелярии</span></div>
<p>Всё для учёбы, творчества и вдохновения. Предзаказ по Кыргызстану 🌸</p>
</div>
<div>
<h4 class="kawaii-font mb-3">Каталог</h4>
<ul class="space-y-1.5">{% for c in categories %}<li><a href="/catalog?category={{ c.id }}" class="hover:underline decoration-wavy">♡ {{ c.name }}</a></li>{% endfor %}</ul>
</div>
<div>
<h4 class="kawaii-font mb-3">Как заказать</h4>
<ol class="space-y-1.5 list-decimal list-inside"><li>Добавьте товары в предзаказ</li><li>Оставьте имя и телефон</li><li>Мы свяжемся и подтвердим</li></ol>
</div>
</div>
<div class="text-center text-xs pb-5" style="color:var(--mute)">© 2026 Мир канцелярии · Кыргызстан · сделано с ♡</div>
</footer>

<nav class="md:hidden fixed bottom-3 inset-x-3 z-50 grid grid-cols-3 text-[11px] font-extrabold rounded-full bg-white" style="border:2px solid #FF8FC0;box-shadow:0 5px 0 #FFB3D1;margin-bottom:env(safe-area-inset-bottom)" aria-label="Основная навигация">
<a href="/" class="flex flex-col items-center py-2 {% if request.path=='/' %}text-brand{% else %}text-gray-500{% endif %}"><span class="text-lg">🏠</span>Главная</a>
<a href="/catalog" class="flex flex-col items-center py-2 {% if request.path.startswith('/catalog') %}text-brand{% else %}text-gray-500{% endif %}"><span class="text-lg">🌸</span>Каталог</a>
<a href="/cart" class="relative flex flex-col items-center py-2 {% if request.path.startswith('/cart') %}text-brand{% else %}text-gray-500{% endif %}"><span class="text-lg">🛍️</span>Предзаказ
<span data-cart-badge class="absolute top-0.5 left-1/2 ml-2 bg-accent text-white text-[10px] rounded-full h-4 min-w-4 px-1 flex items-center justify-center {% if not cart_count %}hidden{% endif %}">{{ cart_count }}</span></a>
</nav>
<div id="toasts" aria-live="polite"></div>

<script>
(function(){
  var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
  function toast(msg,type){
    var t=document.createElement('div');t.className='toast';
    var e={success:'💖',danger:'😿',warning:'🌷'}[type]||'✨';
    t.innerHTML='<span>'+e+'</span><span></span>';t.lastChild.textContent=msg;
    $('#toasts').appendChild(t);
    setTimeout(function(){t.classList.add('out');setTimeout(function(){t.remove()},260)},2800);
  }
  window.toast=toast;
  $$('#flash i').forEach(function(i){toast(i.textContent,i.dataset.cat)});
  function setBadge(n){$$('[data-cart-badge]').forEach(function(b){b.textContent=n;b.classList.toggle('hidden',!n);b.classList.remove('pop');void b.offsetWidth;b.classList.add('pop')})}
  function hearts(el){
    if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;
    var r=el.getBoundingClientRect(),set=['💖','🌸','✨','💕','🎀'];
    for(var i=0;i<6;i++){var h=document.createElement('span');h.className='heart';h.textContent=set[i%5];
      h.style.left=(r.left+r.width/2)+'px';h.style.top=(r.top+r.height/2)+'px';h.style.setProperty('--dx',(Math.random()*90-45)+'px');
      h.style.animationDelay=(i*50)+'ms';document.body.appendChild(h);setTimeout(function(x){x.remove()},1100,h)}
  }
  document.addEventListener('submit',function(e){
    var f=e.target;
    if(!f.action||f.action.indexOf('/cart/add/')<0)return;
    e.preventDefault();
    var btn=f.querySelector('button'),old=btn.innerHTML;btn.disabled=true;
    fetch(f.action,{method:'POST',body:new FormData(f),headers:{'X-Requested-With':'fetch'}})
      .then(function(r){return r.json()})
      .then(function(d){setBadge(d.count);hearts(btn);toast('«'+d.name+'» уже в предзаказе','success');btn.innerHTML='<i class="fas fa-check text-xs"></i>'})
      .catch(function(){toast('Не получилось добавить. Проверьте интернет и повторите','danger')})
      .finally(function(){setTimeout(function(){btn.disabled=false;btn.innerHTML=old},900)});
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){e.preventDefault();$('#q').focus()}
  });
  $$('img[data-skel]').forEach(function(img){
    var p=img.parentElement;p.classList.add('skel');
    function done(){p.classList.remove('skel')}
    if(img.complete)done();else{img.addEventListener('load',done);img.addEventListener('error',done)}
  });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.08});
    $$('.rv').forEach(function(el){io.observe(el)});
  }else{$$('.rv').forEach(function(el){el.classList.add('in')})}
})();
</script>
</body></html>
'''


def product_card(p):
    cat = f'<span class="sticker !text-[10px] !py-0.5">{p.category.name}</span>' if p.category else ''
    price_html = (f'<span class="font-extrabold text-brand text-lg">{p.price:,.0f} <span class="text-xs font-bold">сом</span></span>'
                  if p.price and p.price > 0 else '<span class="font-bold text-brand text-sm">Цена по запросу</span>')
    return f'''<div class="card bg-white rounded-3xl overflow-hidden">
<a href="/product/{p.id}" aria-label="{p.name}"><div class="aspect-square bg-gray-50 overflow-hidden">
<img src="{p.image_url}" alt="{p.name}" loading="lazy" decoding="async" data-skel class="w-full h-full object-cover"
onerror="this.src='https://via.placeholder.com/400x400/FFD6E7/E0457F?text=%E2%99%A1'"></div></a>
<div class="p-3.5">{cat}
<a href="/product/{p.id}"><h3 class="text-gray-800 mt-1.5 text-sm line-clamp-2 min-h-[2.5rem] hover:text-brand transition">{p.name}</h3></a>
<div class="flex justify-between items-center mt-2.5">
{price_html}
<form action="/cart/add/{p.id}" method="post">
<button class="w-11 h-11 btn-grad text-white flex items-center justify-center" aria-label="Добавить «{p.name}» в предзаказ"><i class="fas fa-plus text-sm"></i></button>
</form></div></div></div>'''


@app.route('/cart/add/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    p = Product.query.get_or_404(pid)
    qty = max(1, request.form.get('quantity', 1, type=int))
    cart = get_cart()
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session['cart'] = cart
    if request.headers.get('X-Requested-With') == 'fetch':
        from flask import jsonify
        return jsonify(ok=True, name=p.name, count=sum(cart.values()))
    flash(f'«{p.name}» добавлен в предзаказ', 'success')
    return redirect(request.referrer or url_for('catalog'))


MASCOT = '''<svg viewBox="0 0 240 240" class="w-full h-full" role="img" aria-label="Милый маскот магазина">
<ellipse cx="120" cy="226" rx="70" ry="9" fill="#FFB3D1" opacity=".6"/>
<circle cx="120" cy="128" r="88" fill="#FFC4DD" stroke="#FF8FC0" stroke-width="5"/>
<path d="M120 48c-30-26-62-8-50 16 8 14 38 10 50-6zM120 48c30-26 62-8 50 16-8 14-38 10-50-6z" fill="#FF5C8A" stroke="#E0457F" stroke-width="4" stroke-linejoin="round"/>
<circle cx="120" cy="52" r="11" fill="#E0457F"/>
<g class="eye"><ellipse cx="88" cy="128" rx="11" ry="14" fill="#5A2A44"/><circle cx="92" cy="122" r="4.5" fill="#fff"/></g>
<g class="eye"><ellipse cx="152" cy="128" rx="11" ry="14" fill="#5A2A44"/><circle cx="156" cy="122" r="4.5" fill="#fff"/></g>
<ellipse cx="68" cy="152" rx="15" ry="9" fill="#FF8FB1" opacity=".75"/><ellipse cx="172" cy="152" rx="15" ry="9" fill="#FF8FB1" opacity=".75"/>
<path d="M108 150q12 14 24 0" fill="none" stroke="#5A2A44" stroke-width="5" stroke-linecap="round"/>
<g transform="rotate(28 196 190)"><rect x="188" y="150" width="16" height="64" rx="4" fill="#FFD84D" stroke="#5A2A44" stroke-width="3"/><path d="M188 214l8 16 8-16z" fill="#FFE9C9" stroke="#5A2A44" stroke-width="3" stroke-linejoin="round"/><rect x="188" y="150" width="16" height="12" rx="3" fill="#FF8FB1" stroke="#5A2A44" stroke-width="3"/></g>
</svg>'''


@app.route('/')
def index():
    products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    cats = Category.query.all()
    tints = ['bg-pink-50', 'bg-sky-50', 'bg-amber-50', 'bg-emerald-50', 'bg-rose-50', 'bg-violet-50']
    emojis = ['🖍️', '📒', '🎀', '✂️', '🧸', '🌈']
    cat_html = ''
    for i, c in enumerate(cats):
        cnt = Product.query.filter_by(category_id=c.id).count()
        cat_html += f'''<a href="/catalog?category={c.id}" class="card {tints[i % 6]} rounded-3xl p-5 text-center">
<div class="w-16 h-16 mx-auto mb-3 rounded-full bg-white flex items-center justify-center text-3xl" style="border:2px solid #FFD0E3">{emojis[i % 6]}</div>
<div class="kawaii-font text-sm">{c.name}</div><div class="text-xs text-gray-400 mt-1">{cnt} шт.</div></a>'''
    cards = ''.join(product_card(p) for p in products) or '''<div class="col-span-full text-center py-16">
<div class="text-5xl mb-3">(｡•́︿•̀｡)</div><p class="kawaii-font text-lg">Тут пока пусто</p><p class="text-sm text-gray-400">Скоро появятся новые товары</p></div>'''
    cat_block = (f"<section class='max-w-7xl mx-auto px-4 pt-14 rv'><h2 class='text-2xl text-center mb-6'>🌸 Выбирай категорию 🌸</h2>"
                 f"<div class='grid grid-cols-2 sm:grid-cols-3 md:grid-cols-{min(len(cats), 6)} gap-4'>{cat_html}</div></section>") if cats else ''
    content = f'''
<section class="relative overflow-hidden">
<span class="floaty absolute text-4xl left-[6%] top-10 hidden sm:block" aria-hidden="true">✨</span>
<span class="floaty d2 absolute text-3xl right-[8%] top-16 hidden sm:block" aria-hidden="true">🌸</span>
<span class="floaty d3 absolute text-3xl left-[44%] bottom-6 hidden md:block" aria-hidden="true">💖</span>
<div class="max-w-7xl mx-auto px-4 py-10 md:py-16 grid md:grid-cols-2 gap-6 items-center">
<div class="text-center md:text-left">
<span class="sticker mb-4">🎀 предзаказ по всему Кыргызстану</span>
<h1 class="text-3xl sm:text-4xl lg:text-5xl leading-tight mb-4">Милая канцелярия<br>для учёбы и творчества</h1>
<p class="text-gray-500 mb-7 max-w-md mx-auto md:mx-0">Ручки, тетради, наклейки и краски, от которых хочется учиться. Выбери любимое и оставь предзаказ, мы позвоним сами.</p>
<a href="/catalog" class="btn-orange inline-flex items-center gap-2 text-white font-extrabold px-8 py-3.5 text-lg">Смотреть каталог 💕</a>
</div>
<div class="flex justify-center"><div class="w-60 h-60 sm:w-72 sm:h-72 floaty">{MASCOT}</div></div>
</div></section>

<div class="max-w-7xl mx-auto px-4 rv">
<div class="bg-white rounded-3xl grid grid-cols-2 md:grid-cols-4 gap-px overflow-hidden" style="border:2px solid #FFD0E3;box-shadow:0 6px 0 #FFC2DB">
<div class="p-4 text-center"><div class="text-2xl mb-1">🛍️</div><div class="font-extrabold text-sm">Много товаров</div><div class="text-xs text-gray-400">на любой вкус</div></div>
<div class="p-4 text-center"><div class="text-2xl mb-1">⭐</div><div class="font-extrabold text-sm">Качество</div><div class="text-xs text-gray-400">проверенное нами</div></div>
<div class="p-4 text-center"><div class="text-2xl mb-1">📝</div><div class="font-extrabold text-sm">Предзаказ</div><div class="text-xs text-gray-400">быстро и просто</div></div>
<div class="p-4 text-center"><div class="text-2xl mb-1">💬</div><div class="font-extrabold text-sm">Всегда на связи</div><div class="text-xs text-gray-400">ответим по телефону</div></div>
</div></div>

{cat_block}

<section class="max-w-7xl mx-auto px-4 py-12 rv">
<div class="flex justify-between items-end mb-6">
<div><h2 class="text-2xl">🍓 Новинки</h2><p class="text-gray-400 text-sm">Выбери и оставь предзаказ</p></div>
<a href="/catalog" class="sticker hover:bg-soft">Весь каталог ›</a>
</div>
<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">{cards}</div>
</section>

<section class="max-w-7xl mx-auto px-4 rv">
<div class="rounded-3xl bg-gradient-to-r p-6 md:p-8 flex flex-col md:flex-row items-center gap-4 justify-between" style="border:2px dashed #FF8FC0">
<div class="flex items-center gap-4 text-center md:text-left"><div class="text-4xl">🎁</div>
<div><div class="kawaii-font text-lg">Оформи предзаказ прямо сейчас</div><div class="text-sm text-gray-500">Мы свяжемся с тобой и всё уточним</div></div></div>
<a href="/catalog" class="btn-grad text-white font-extrabold px-7 py-3 whitespace-nowrap">В каталог</a>
</div></section>
'''
    return page('Главная', content)
