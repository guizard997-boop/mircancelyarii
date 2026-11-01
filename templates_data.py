# -*- coding: utf-8 -*-
"""Шаблоны и стили сайта (современный светлый дизайн). Логика — в app.py."""

CSS = r'''
:root{--bg:#050505;--sf:#0D0D0D;--sf2:#161616;--ink:#F4F4F4;--mut:#8F8F8F;--line:#2A2A2A;--rs:2px;--rm:2px;--rl:2px}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;background:var(--bg)}
body{margin:0;font:16px/1.55 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:radial-gradient(1200px 600px at 50% -10%,#1d1d1d 0,transparent 70%) var(--bg);background-attachment:fixed;min-height:100vh;display:flex;flex-direction:column}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:200;opacity:.06;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>")}
main{flex:1}h1,h2,h3,h4{font-family:Cormorant,Georgia,serif;font-weight:700;letter-spacing:.01em;line-height:1.05;margin:0}
a{color:inherit;text-decoration:none}img{display:block;max-width:100%}button{font-family:inherit}
::selection{background:var(--ink);color:var(--bg)}::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:#333}
.wrap{width:100%;max-width:1200px;margin:0 auto;padding:0 20px}
svg.i{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;flex:none}
:focus-visible{outline:2px dashed var(--ink);outline-offset:3px}
.hdr{position:sticky;top:0;z-index:40;background:rgba(5,5,5,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.hdr .wrap{display:flex;align-items:center;gap:16px;height:68px}
.logo{display:flex;align-items:center;gap:12px;font:700 21px Cormorant,Georgia,serif;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;animation:flick 7s infinite}
.logo b{display:grid;place-items:center;width:36px;height:36px;border:1px solid var(--ink)}
@keyframes flick{0%,93%,100%{opacity:1}94%{opacity:.5}95%{opacity:1}97%{opacity:.35}98%{opacity:1}}
.search{flex:1;max-width:520px;position:relative}
.search input{width:100%;height:44px;border:1px solid var(--line);background:var(--sf);padding:0 16px 0 44px;font:400 15px Inter,sans-serif;color:var(--ink);border-radius:var(--rs)}
.search input::placeholder{color:var(--mut)}.search svg{position:absolute;left:15px;top:12px;color:var(--mut)}
.ibtn{position:relative;display:grid;place-items:center;width:44px;height:44px;border:1px solid var(--line);background:var(--sf)}.ibtn:hover{border-color:var(--ink)}
.badge{position:absolute;top:-7px;right:-7px;min-width:20px;height:20px;padding:0 5px;background:var(--ink);color:var(--bg);font:800 11px/20px Inter,sans-serif;text-align:center}.badge[hidden]{display:none}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:48px;padding:0 26px;border:1px solid var(--ink);border-radius:var(--rs);background:var(--ink);color:var(--bg);font:700 12px Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;cursor:pointer;transition:background .15s,color .15s}
.btn:hover{background:var(--bg);color:var(--ink)}.btn[disabled]{opacity:.5}
.btn.sec{background:transparent;color:var(--ink);border-color:#444}.btn.sec:hover{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.btn.sm{height:34px;padding:0 14px;font-size:11px}.btn.red{background:transparent;color:#ddd;border:1px dashed #666}.btn.red:hover{background:var(--ink);color:var(--bg)}.btn.blk{width:100%}
.chips{display:flex;gap:8px;overflow-x:auto;padding:16px 0;scrollbar-width:none}.chips::-webkit-scrollbar{display:none}
.chip{flex:none;height:38px;padding:0 16px;display:inline-flex;align-items:center;border:1px solid var(--line);background:var(--sf);font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.chip:hover{border-color:var(--ink);color:var(--ink)}.chip.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.hero{position:relative;display:grid;grid-template-columns:1.05fr 1fr;gap:32px;align-items:center;padding:56px 0 28px;overflow:hidden}
.hero h1{font-size:clamp(46px,7vw,96px);text-shadow:0 0 34px rgba(255,255,255,.22)}.hero h1 em{font-style:italic;font-weight:600;color:var(--mut)}
.hero p{color:var(--mut);font-size:18px;max-width:460px;margin:22px 0 32px}
.scene{width:100%;height:auto;display:block}.web{position:absolute;left:-8px;top:-8px;width:210px;opacity:.5;pointer-events:none}
.bat{transform-box:fill-box;transform-origin:center;animation:flap .45s ease-in-out infinite alternate}@keyframes flap{to{transform:scaleY(.72) translateY(2px)}}
.fog{position:absolute;left:-10%;right:-10%;bottom:-40px;height:180px;background:radial-gradient(ellipse at 50% 100%,rgba(255,255,255,.12),transparent 70%);pointer-events:none}
.sec-h{display:flex;justify-content:space-between;align-items:end;margin:36px 0 18px;padding-bottom:10px;border-bottom:1px solid var(--line)}.sec-h h2{font-size:38px}
.sec-h a{color:var(--mut);font-weight:600;font-size:12px;letter-spacing:.14em;text-transform:uppercase}.sec-h a:hover{color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px}
.pc{background:var(--sf);border:1px solid var(--line);display:flex;flex-direction:column;transition:border-color .2s,transform .2s,box-shadow .2s}
@media(hover:hover){.pc:hover{border-color:var(--ink);transform:translateY(-3px);box-shadow:0 18px 40px -20px rgba(255,255,255,.3)}}
.pc .im{display:block;aspect-ratio:1;background:#111;overflow:hidden}
.pc .im img,.ci img{width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.08) brightness(.92);transition:filter .35s,transform .5s}
@media(hover:hover){.pc:hover .im img{filter:none;transform:scale(1.04)}}
.pc .bd{padding:14px;display:flex;flex-direction:column;gap:6px;flex:1}.pc .cat{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.pc h3{font:600 21px/1.12 Cormorant,Georgia,serif;letter-spacing:0;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.25em}
.pc .row{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:8px}
.price{font:700 26px Cormorant,Georgia,serif}.price small{font:500 11px Inter,sans-serif;color:var(--mut);letter-spacing:.1em;text-transform:uppercase}
.add{width:42px;height:42px;border:1px solid var(--ink);background:var(--ink);color:var(--bg);display:grid;place-items:center;cursor:pointer;transition:background .15s,color .15s}.add:hover{background:var(--bg);color:var(--ink)}
.tools{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}.tools select{height:40px;border:1px solid var(--line);padding:0 12px;background:var(--sf);color:var(--ink);font:500 14px Inter,sans-serif}
.pager{display:flex;gap:6px;justify-content:center;margin:30px 0}.pager a{min-width:40px;height:40px;display:grid;place-items:center;border:1px solid var(--line);background:var(--sf);font-weight:600}.pager a.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.empty{text-align:center;padding:64px 0;color:var(--mut)}.empty h2{color:var(--ink);margin-bottom:8px;font-size:40px}.empty .btn{margin-top:20px}
.crumbs{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);padding-top:22px}.crumbs a:hover{color:var(--ink)}
.pd{display:grid;grid-template-columns:1fr 1fr;gap:44px;padding:22px 0 10px}
.pd .ph{aspect-ratio:1;overflow:hidden;background:#111;border:1px solid var(--line)}.pd .ph img{width:100%;height:100%;object-fit:cover}
.pd h1{font-size:clamp(34px,4.6vw,60px);margin:10px 0 16px}.pd .price{font-size:40px;margin-bottom:18px}
.pd .desc{color:var(--mut);max-width:520px;white-space:pre-line}.buy{display:flex;gap:12px;margin-top:28px;flex-wrap:wrap}
.qty{display:inline-flex;align-items:center;border:1px solid var(--line);background:var(--sf);height:48px}
.qty button{width:42px;height:100%;border:0;background:none;cursor:pointer;color:var(--ink);display:grid;place-items:center}.qty button:hover{background:var(--ink);color:var(--bg)}
.qty input{width:44px;border:0;text-align:center;font:600 15px Inter,sans-serif;background:none;color:var(--ink);height:100%;-moz-appearance:textfield}
.qty input::-webkit-outer-spin-button,.qty input::-webkit-inner-spin-button{-webkit-appearance:none}
.two{display:grid;grid-template-columns:1fr 360px;gap:24px;align-items:start;padding:20px 0 10px}.two.eq{grid-template-columns:1fr 1fr}
.box{background:var(--sf);border:1px solid var(--line);padding:22px}
.h1{font-size:46px;margin:28px 0 6px}
.ci{display:grid;grid-template-columns:72px 1fr auto;gap:14px;align-items:center;padding:14px 0;border-bottom:1px solid var(--line)}.ci:last-child{border:0}
.ci img{width:72px;height:72px;background:#111}.ci .nm{font:600 20px Cormorant,Georgia,serif}.ci .sm{color:var(--mut);font-size:14px}
.ctl{display:flex;align-items:center;gap:10px}.ctl .qty{height:38px}.ctl .qty button{width:34px}.ctl .qty span{min-width:26px;text-align:center;font-weight:600}
.ctl .x{border:0;background:none;color:var(--mut);cursor:pointer;display:grid;place-items:center;width:34px;height:34px}.ctl .x:hover{color:var(--ink)}
.sum{position:sticky;top:90px}.sum .tot{display:flex;justify-content:space-between;align-items:baseline;font-weight:600;margin:14px 0 18px}.sum .tot b{font:700 34px Cormorant,Georgia,serif}
.sum .ln{display:flex;justify-content:space-between;gap:10px;font-size:14px;color:var(--mut);padding:3px 0}
label.f{display:block;font-weight:600;font-size:12px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:14px}
label.f input,label.f select,label.f textarea{display:block;width:100%;margin-top:7px;height:48px;border:1px solid var(--line);border-radius:var(--rs);padding:0 14px;font:400 16px Inter,sans-serif;background:var(--bg);color:var(--ink);text-transform:none;letter-spacing:0}
label.f textarea{height:auto;padding:12px 14px;min-height:110px;resize:vertical}label.f input[type=file]{padding:11px 12px;height:auto}
label.ck{display:flex;gap:10px;align-items:center;font-weight:500;margin-bottom:14px}label.ck input{accent-color:#fff}
input:focus,select:focus,textarea:focus{outline:1px solid var(--ink);outline-offset:0;border-color:var(--ink)}
.hint{font-size:13px;color:var(--mut);font-weight:400;letter-spacing:0;text-transform:none}
.pay{border:1px solid var(--line);padding:16px;background:var(--sf);display:grid;grid-template-columns:1fr auto;gap:14px;margin-bottom:12px}
.pay h4{margin:0 0 8px;font:700 24px Cormorant,Georgia,serif}.pay pre{margin:0 0 12px;white-space:pre-wrap;font:500 14px/1.7 Inter,sans-serif;word-break:break-word}
.pay .qr{width:120px;height:120px;object-fit:contain;border:1px solid var(--line);background:#fff;padding:4px}
.ok-ic{display:grid;place-items:center;width:58px;height:58px;border:1px solid var(--ink);margin-bottom:16px}.ok-ic svg{width:28px;height:28px}
.an{display:flex;gap:6px;overflow-x:auto;padding:16px 0 4px;scrollbar-width:none}.an a{flex:none;padding:8px 16px;border:1px solid transparent;font-weight:600;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}.an a.on{border-color:var(--ink);color:var(--ink)}.an a:hover{color:var(--ink)}.an .out{margin-left:auto}
.scroll{overflow-x:auto}
.tbl{width:100%;border-collapse:collapse;background:var(--sf);border:1px solid var(--line);font-size:14px}
.tbl th{background:var(--sf2);text-align:left;color:var(--mut);font-weight:600;padding:10px 14px;white-space:nowrap;font-size:11px;letter-spacing:.12em;text-transform:uppercase}.tbl td{padding:12px 14px;border-top:1px solid var(--line);vertical-align:middle}
.tag{display:inline-block;padding:2px 10px;border:1px solid #555;font:600 11px Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#ccc;white-space:nowrap}
.tag.new{background:var(--ink);color:var(--bg);border-color:var(--ink)}.tag.ok{border-color:#ddd;color:#fff}.tag.bad{border-style:dashed;color:#888;text-decoration:line-through}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:14px 0 22px}.stat b{display:block;font:700 44px Cormorant,Georgia,serif}.stat span{color:var(--mut);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.thumb{width:44px;height:44px;object-fit:cover;background:#111}.cell{display:flex;align-items:center;gap:12px}
.note{border:1px dashed #777;padding:12px 14px;font-size:14px;margin:12px 0;color:#ddd}
.acts{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.acts form{margin:0}
.ft{position:relative;background:var(--sf);border-top:1px solid var(--line);margin-top:76px;padding:42px 0 8px}
.ft::before{content:"";position:absolute;left:0;right:0;top:-14px;height:14px;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='24' height='14' viewBox='0 0 24 14'><path d='M0 14L12 0L24 14Z' fill='%230D0D0D'/></svg>") repeat-x}
.ft .wrap{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:28px}.ft h4{font-size:22px;margin-bottom:10px}.ft a{display:block;color:var(--mut);font-size:14px;padding:3px 0}.ft a:hover{color:var(--ink)}
.copy{color:var(--mut);font-size:12px;letter-spacing:.08em;padding-top:26px;padding-bottom:22px}
.nav-b{display:none;position:fixed;left:0;right:0;bottom:0;z-index:40;background:rgba(5,5,5,.96);backdrop-filter:blur(12px);border-top:1px solid var(--line);grid-template-columns:repeat(3,1fr);padding-bottom:env(safe-area-inset-bottom)}
.nav-b a{display:flex;flex-direction:column;align-items:center;gap:2px;padding:9px 0 8px;font-size:10px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);position:relative}.nav-b a.on{color:var(--ink)}.nav-b .badge{top:3px;right:calc(50% - 24px)}
#toasts{position:fixed;left:50%;transform:translateX(-50%);bottom:24px;z-index:300;display:flex;flex-direction:column;gap:8px;align-items:center;pointer-events:none;width:calc(100% - 24px);max-width:420px}
.toast{background:var(--ink);color:var(--bg);padding:12px 18px;font-size:14px;font-weight:600;box-shadow:0 12px 40px -8px rgba(255,255,255,.25);animation:tin .2s ease both}.toast.bad{outline:1px dashed #000;outline-offset:-5px}.toast.out{animation:tout .2s ease both}
@keyframes tin{from{opacity:0;transform:translateY(10px)}}@keyframes tout{to{opacity:0;transform:translateY(6px)}}
@media(max-width:860px){.hero,.pd,.two,.two.eq{grid-template-columns:1fr}.sum{position:static}.ft .wrap{grid-template-columns:1fr 1fr}.hero{padding-top:44px}.scene{max-width:420px;margin:0 auto}}
@media(max-width:600px){.wrap{padding:0 14px}.grid{grid-template-columns:repeat(2,1fr);gap:10px}.logo span{display:none}.cart-h{display:none}.pc .bd{padding:10px}.pc h3{font-size:18px}.nav-b{display:grid}body{padding-bottom:64px}#toasts{bottom:78px}.pay{grid-template-columns:1fr}.ci{grid-template-columns:64px 1fr}.ci .ctl{grid-column:1/-1}.ft .wrap{grid-template-columns:1fr}.h1{font-size:38px}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}html{scroll-behavior:auto}}
'''

JS = r'''
(function(){
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
function toast(m,t){var e=document.createElement('div');e.className='toast '+(t||'');e.textContent=m;$('#toasts').appendChild(e);setTimeout(function(){e.classList.add('out');setTimeout(function(){e.remove()},220)},2600)}
$$('#flash i').forEach(function(i){var c=i.dataset.c;toast(i.textContent,c==='success'?'ok':c==='danger'?'bad':'')});
function badge(n){$$('[data-badge]').forEach(function(b){b.textContent=n;b.hidden=!n})}
document.addEventListener('submit',function(e){var f=e.target;if(!f.matches||!f.matches('[data-add]'))return;e.preventDefault();var b=f.querySelector('button');b.disabled=true;
fetch(f.action,{method:'POST',body:new FormData(f),headers:{'X-Requested-With':'fetch'}}).then(function(r){return r.json()}).then(function(d){badge(d.count);toast('Добавлено: '+d.name,'ok')}).catch(function(){toast('Не удалось добавить. Повторите','bad')}).finally(function(){setTimeout(function(){b.disabled=false},500)})});
document.addEventListener('click',function(e){
var c=e.target.closest('[data-copy]');if(c&&navigator.clipboard){navigator.clipboard.writeText(c.dataset.copy).then(function(){toast('Скопировано','ok')})}
var q=e.target.closest('[data-step]');if(q){var i=q.parentNode.querySelector('input');i.value=Math.min(99,Math.max(1,(+i.value||1)+(+q.dataset.step)))}});
document.addEventListener('keydown',function(e){if(e.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){var s=$('#q');if(s){e.preventDefault();s.focus()}}});
$$('input[type=file][data-preview]').forEach(function(i){i.addEventListener('change',function(){var p=$(i.dataset.preview);if(i.files[0]&&p){p.src=URL.createObjectURL(i.files[0]);p.hidden=false}})});
})();
'''

SPRITE = r'''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-home" viewBox="0 0 24 24"><path d="M3 11l9-8 9 8v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/></symbol>
<symbol id="i-grid" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></symbol>
<symbol id="i-bag" viewBox="0 0 24 24"><path d="M6 7h12l1 13H5z"/><path d="M9 7a3 3 0 0 1 6 0"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></symbol>
<symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
<symbol id="i-minus" viewBox="0 0 24 24"><path d="M5 12h14"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="m5 12 5 5 9-10"/></symbol>
<symbol id="i-copy" viewBox="0 0 24 24"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></symbol>
<symbol id="i-bat" viewBox="0 0 64 32"><path d="M32 14 L8 5 Q11 13 3 19 Q12 17 16 24 Q21 18 26 22 L32 16 L38 22 Q43 18 48 24 Q52 17 61 19 Q53 13 56 5 Z M28 11 L27 3 L31 8 L33 8 L37 3 L36 11 Z"/></symbol>
</svg>'''

T = {}

T['base.html'] = r'''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#050505">
<title>{{ title }} — Мир канцелярии</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,600;0,700;1,600&family=Inter:wght@400;500;600&display=swap&subset=cyrillic" rel="stylesheet">
<style>{% raw %}''' + CSS + r'''{% endraw %}</style></head><body>
''' + SPRITE + r'''
<header class="hdr"><div class="wrap">
<a class="logo" href="/" aria-label="Мир канцелярии"><b><svg class="i"><use href="#i-moon"/></svg></b><span>Мир канцелярии</span></a>
<form class="search" action="/catalog" role="search"><svg class="i"><use href="#i-search"/></svg><input id="q" type="search" name="q" value="{{ request.args.get('q','') }}" placeholder="Поиск по каталогу" autocomplete="off" aria-label="Поиск"></form>
<a class="ibtn cart-h" href="/cart" aria-label="Корзина"><svg class="i"><use href="#i-bag"/></svg><span class="badge" data-badge {% if not cart_count %}hidden{% endif %}>{{ cart_count }}</span></a>
</div></header>
{% with m=get_flashed_messages(with_categories=true) %}{% if m %}<div id="flash" hidden>{% for c,t in m %}<i data-c="{{ c }}">{{ t }}</i>{% endfor %}</div>{% endif %}{% endwith %}
<main>{% block body %}{% endblock %}</main>
<footer class="ft"><div class="wrap">
<div><div class="logo"><b><svg class="i"><use href="#i-moon"/></svg></b><span>Мир канцелярии</span></div></div>
<div><h4>Каталог</h4>{% for c in categories[:8] %}<a href="/catalog?category={{ c.id }}">{{ c.name }}</a>{% endfor %}<a href="/catalog">Все товары</a></div>
<div><h4>Связаться</h4>{% for p in phones %}<a href="tel:{{ p|tel }}">{{ p }}</a>{% endfor %}{% if whatsapp %}<a href="https://wa.me/{{ whatsapp|tel|replace('+','') }}" rel="noopener">WhatsApp</a>{% endif %}{% if not phones and not whatsapp %}<a href="/cart">Оформить предзаказ</a>{% endif %}</div>
</div><div class="wrap copy">© 2026 Мир канцелярии</div></footer>
<nav class="nav-b" aria-label="Навигация">
<a href="/" class="{{ 'on' if request.path=='/' }}"><svg class="i"><use href="#i-home"/></svg>Главная</a>
<a href="/catalog" class="{{ 'on' if request.path.startswith('/catalog') }}"><svg class="i"><use href="#i-grid"/></svg>Каталог</a>
<a href="/cart" class="{{ 'on' if request.path.startswith('/cart') }}"><svg class="i"><use href="#i-bag"/></svg>Корзина<span class="badge" data-badge {% if not cart_count %}hidden{% endif %}>{{ cart_count }}</span></a>
</nav>
<div id="toasts" aria-live="polite"></div>
<script>{% raw %}''' + JS + r'''{% endraw %}</script></body></html>'''

T['macros.html'] = r'''{% macro card(p) %}<article class="pc"><a class="im" href="/product/{{ p.id }}"><img src="{{ p|img }}" alt="{{ p.name }}" loading="lazy" decoding="async"></a>
<div class="bd">{% if p.category %}<span class="cat">{{ p.category.name }}</span>{% endif %}<a href="/product/{{ p.id }}"><h3>{{ p.name }}</h3></a>
<div class="row">{% if p.price and p.price>0 %}<span class="price">{{ p.price|money }} <small>сом</small></span>{% else %}<span class="price"><small>Цена по запросу</small></span>{% endif %}
<form action="/cart/add/{{ p.id }}" method="post" data-add><button class="add" aria-label="В корзину: {{ p.name }}"><svg class="i"><use href="#i-plus"/></svg></button></form></div></div></article>{% endmacro %}
{% macro pay(m) %}<div class="pay"><div><h4>{{ m.title }}</h4>{% if m.details %}<pre>{{ m.details }}</pre><button type="button" class="btn sec sm" data-copy="{{ m.details }}"><svg class="i" style="width:16px;height:16px"><use href="#i-copy"/></svg>Копировать</button>{% endif %}</div>{% if m.qr_url %}<img class="qr" src="{{ m.qr_url }}" alt="QR: {{ m.title }}">{% endif %}</div>{% endmacro %}'''

T['home.html'] = r'''{% extends 'base.html' %}{% from 'macros.html' import card %}{% block body %}<div class="wrap">
<section class="hero"><svg class="web" viewBox="0 0 200 200" fill="none" stroke="#fff" stroke-width="1" aria-hidden="true"><path d="M0 0L200.0 0.0M0 0L184.8 76.5M0 0L141.4 141.4M0 0L76.5 184.8M0 0L0.0 200.0M40.0 0.0Q33.7 6.7 37.0 15.3M37.0 15.3Q28.6 19.1 28.3 28.3M28.3 28.3Q19.1 28.6 15.3 37.0M15.3 37.0Q6.7 33.7 0.0 40.0M80.0 0.0Q67.5 13.4 73.9 30.6M73.9 30.6Q57.2 38.2 56.6 56.6M56.6 56.6Q38.2 57.2 30.6 73.9M30.6 73.9Q13.4 67.5 0.0 80.0M120.0 0.0Q101.2 20.1 110.9 45.9M110.9 45.9Q85.8 57.3 84.9 84.9M84.9 84.9Q57.3 85.8 45.9 110.9M45.9 110.9Q20.1 101.2 0.0 120.0M160.0 0.0Q135.0 26.8 147.8 61.2M147.8 61.2Q114.4 76.4 113.1 113.1M113.1 113.1Q76.4 114.4 61.2 147.8M61.2 147.8Q26.8 135.0 0.0 160.0M200.0 0.0Q168.7 33.6 184.8 76.5M184.8 76.5Q143.0 95.6 141.4 141.4M141.4 141.4Q95.6 143.0 76.5 184.8M76.5 184.8Q33.6 168.7 0.0 200.0"/></svg><div style="position:relative"><h1>Канцелярия для <em>долгих ночей</em></h1><p>Ручки, тетради, краски и всё для тех, кто пишет, рисует и учится допоздна. Выберите нужное и оставьте предзаказ.</p><a class="btn" href="/catalog">Открыть каталог</a></div><div><svg class="scene" viewBox="0 0 520 460" role="img" aria-label="Луна и летучие мыши"><defs><radialGradient id="mg" cx="38%" cy="32%" r="78%"><stop offset="0" stop-color="#FAFAFA"/><stop offset="1" stop-color="#8E8E8E"/></radialGradient></defs>
<circle cx="300" cy="225" r="175" fill="url(#mg)"/><g fill="#000" opacity=".16"><circle cx="240" cy="160" r="30"/><circle cx="360" cy="285" r="38"/><circle cx="285" cy="330" r="18"/><circle cx="385" cy="165" r="16"/><circle cx="210" cy="265" r="13"/></g>
<use class="bat" href="#i-bat" x="205" y="185" width="150" height="75" fill="#050505"/><use class="bat" href="#i-bat" x="335" y="110" width="72" height="36" fill="#050505" style="animation-delay:-.2s"/>
<use class="bat" href="#i-bat" x="25" y="85" width="90" height="45" fill="#F4F4F4" style="animation-delay:-.1s"/><use class="bat" href="#i-bat" x="420" y="30" width="64" height="32" fill="#F4F4F4" style="animation-delay:-.3s"/>
<use class="bat" href="#i-bat" x="40" y="335" width="60" height="30" fill="#F4F4F4" style="animation-delay:-.25s"/><use class="bat" href="#i-bat" x="425" y="360" width="84" height="42" fill="#F4F4F4"/></svg></div><div class="fog"></div></section>
{% if categories %}<div class="chips">{% for c in categories %}<a class="chip" href="/catalog?category={{ c.id }}">{{ c.name }}</a>{% endfor %}</div>{% endif %}
<div class="sec-h"><h2>Новинки</h2><a href="/catalog">Весь каталог</a></div>
{% if products %}<div class="grid">{% for p in products %}{{ card(p) }}{% endfor %}</div>{% else %}<div class="empty"><h2>Каталог скоро наполнится</h2><p>Загляните позже.</p></div>{% endif %}
</div>{% endblock %}'''

T['catalog.html'] = r'''{% extends 'base.html' %}{% from 'macros.html' import card %}{% block body %}<div class="wrap">
<h1 class="h1">{{ 'Поиск: ' ~ q if q else 'Каталог' }}</h1>
<div class="chips"><a class="chip {{ 'on' if not cur }}" href="{{ url_for('catalog', q=q or None, sort=sort if sort!='new' else None) }}">Все</a>{% for c in categories %}<a class="chip {{ 'on' if cur==c.id }}" href="{{ url_for('catalog', category=c.id, q=q or None, sort=sort if sort!='new' else None) }}">{{ c.name }}</a>{% endfor %}</div>
<form class="tools" method="get">{% if q %}<input type="hidden" name="q" value="{{ q }}">{% endif %}{% if cur %}<input type="hidden" name="category" value="{{ cur }}">{% endif %}
<span class="hint">{{ total }} {{ 'товар' if total%10==1 and total%100!=11 else 'товара' if total%10 in (2,3,4) and total%100 not in (12,13,14) else 'товаров' }}</span>
<select name="sort" onchange="this.form.submit()" aria-label="Сортировка"><option value="new" {{ 'selected' if sort=='new' }}>Сначала новые</option><option value="asc" {{ 'selected' if sort=='asc' }}>Сначала дешевле</option><option value="desc" {{ 'selected' if sort=='desc' }}>Сначала дороже</option></select></form>
<div style="height:14px"></div>
{% if products %}<div class="grid">{% for p in products %}{{ card(p) }}{% endfor %}</div>
{% if pages>1 %}<div class="pager">{% for n in range(1,pages+1) %}<a class="{{ 'on' if n==page }}" href="{{ url_for('catalog', category=cur or None, q=q or None, sort=sort if sort!='new' else None, page=n) }}">{{ n }}</a>{% endfor %}</div>{% endif %}
{% else %}<div class="empty"><h2>Ничего не найдено</h2><p>Измените запрос или выберите другую категорию.</p><a class="btn" href="/catalog">Сбросить фильтры</a></div>{% endif %}
</div>{% endblock %}'''

T['product.html'] = r'''{% extends 'base.html' %}{% from 'macros.html' import card %}{% block body %}<div class="wrap">
<nav class="crumbs"><a href="/">Главная</a> / <a href="/catalog">Каталог</a>{% if p.category %} / <a href="/catalog?category={{ p.category.id }}">{{ p.category.name }}</a>{% endif %}</nav>
<div class="pd"><div class="ph"><img src="{{ p|img }}" alt="{{ p.name }}"></div>
<div><h1>{{ p.name }}</h1>{% if p.price and p.price>0 %}<div class="price">{{ p.price|money }} <small>сом</small></div>{% else %}<div class="price"><small>Цена по запросу</small></div>{% endif %}
{% if p.description %}<p class="desc">{{ p.description }}</p>{% endif %}
<form class="buy" action="/cart/add/{{ p.id }}" method="post" data-add><div class="qty"><button type="button" data-step="-1" aria-label="Меньше"><svg class="i"><use href="#i-minus"/></svg></button><input name="quantity" value="1" inputmode="numeric" aria-label="Количество"><button type="button" data-step="1" aria-label="Больше"><svg class="i"><use href="#i-plus"/></svg></button></div><button class="btn">В корзину</button><a class="btn sec" href="/cart">Перейти в корзину</a></form></div></div>
{% if related %}<div class="sec-h"><h2>Похожие товары</h2></div><div class="grid">{% for r in related %}{{ card(r) }}{% endfor %}</div>{% endif %}
</div>{% endblock %}'''

T['cart.html'] = r'''{% extends 'base.html' %}{% block body %}<div class="wrap"><h1 class="h1">Корзина</h1>
{% if items %}<div class="two"><div class="box">{% for p,q,sub in items %}<div class="ci"><a href="/product/{{ p.id }}"><img src="{{ p|img }}" alt=""></a>
<div><a class="nm" href="/product/{{ p.id }}">{{ p.name }}</a><div class="sm">{% if p.price>0 %}{{ p.price|money }} сом · {{ sub|money }} сом{% else %}Цена по запросу{% endif %}</div></div>
<form class="ctl" action="/cart/update/{{ p.id }}" method="post"><div class="qty"><button name="delta" value="-1" aria-label="Меньше"><svg class="i"><use href="#i-minus"/></svg></button><span>{{ q }}</span><button name="delta" value="1" aria-label="Больше"><svg class="i"><use href="#i-plus"/></svg></button></div>
<button class="x" name="delta" value="-999" aria-label="Удалить"><svg class="i"><use href="#i-x"/></svg></button></form></div>{% endfor %}</div>
<aside class="box sum"><div class="hint">Товаров: {{ count }}</div><div class="tot"><span>Итого</span><b>{{ total|money }} сом</b></div><a class="btn blk" href="/checkout">Оформить предзаказ</a></aside></div>
{% else %}<div class="empty"><h2>В корзине пока пусто</h2><p>Добавьте товары из каталога.</p><a class="btn" href="/catalog">В каталог</a></div>{% endif %}</div>{% endblock %}'''

T['checkout.html'] = r'''{% extends 'base.html' %}{% from 'macros.html' import pay %}{% block body %}<div class="wrap"><h1 class="h1">Оформление предзаказа</h1>
<div class="two"><div><form class="box" method="post"><label class="f">Имя<input name="name" required autocomplete="name" placeholder="Как к вам обращаться"></label>
<label class="f">Телефон<input name="phone" required type="tel" autocomplete="tel" inputmode="tel" placeholder="+996 700 000 000"></label>
<label class="f">Комментарий <span class="hint">(необязательно)</span><textarea name="comment" placeholder="Например, удобное время звонка"></textarea></label>
<button class="btn blk">Отправить предзаказ</button></form>
{% if methods %}<h2 style="font-size:20px;margin:26px 0 12px">Реквизиты для оплаты</h2>{% for m in methods %}{{ pay(m) }}{% endfor %}<p class="hint">Реквизиты также будут на странице подтверждения.</p>{% endif %}</div>
<aside class="box sum"><h3 style="font-size:17px;margin-bottom:10px">Ваш заказ</h3>{% for p,q,sub in items %}<div class="ln"><span>{{ p.name|truncate(34) }} × {{ q }}</span><span>{% if sub>0 %}{{ sub|money }}{% else %}—{% endif %}</span></div>{% endfor %}<div class="tot"><span>Итого</span><b>{{ total|money }} сом</b></div></aside></div></div>{% endblock %}'''

T['order_done.html'] = r'''{% extends 'base.html' %}{% from 'macros.html' import pay %}{% block body %}<div class="wrap" style="max-width:760px"><div style="padding:36px 0 10px"><div class="ok-ic"><svg class="i"><use href="#i-check"/></svg></div>
<h1 style="font-size:32px">Предзаказ №{{ o.id }} принят</h1><p class="hint" style="font-size:16px;margin-top:8px">Мы свяжемся с вами по номеру {{ o.customer_phone }} и подтвердим заказ.</p></div>
<div class="box"><h3 style="font-size:17px;margin-bottom:8px">Состав</h3>{% for i in o.items %}<div class="ln" style="display:flex;justify-content:space-between;padding:4px 0"><span>{{ i.product.name if i.product else 'Товар' }} × {{ i.quantity }}</span><span>{{ (i.price*i.quantity)|money }}</span></div>{% endfor %}
<div class="tot" style="display:flex;justify-content:space-between;font-weight:700;margin-top:10px;padding-top:12px;border-top:1px solid var(--line)"><span>Итого</span><span>{{ o.total_price|money }} сом</span></div></div>
{% if methods %}<h2 style="font-size:20px;margin:26px 0 12px">Как оплатить</h2>{% for m in methods %}{{ pay(m) }}{% endfor %}{% endif %}
<p style="margin:22px 0"><a class="btn sec" href="/catalog">Вернуться в каталог</a></p></div>{% endblock %}'''

# ---------------- админка ----------------
T['admin_base.html'] = r'''{% extends 'base.html' %}{% block body %}<div class="wrap">
<nav class="an">{% for k,l in [('dashboard','Обзор'),('products','Товары'),('orders','Заказы'),('categories','Категории'),('payments','Оплата'),('contacts','Контакты')] %}<a class="{{ 'on' if active==k }}" href="/admin/{{ k }}">{{ l }}</a>{% endfor %}<a class="out" href="/admin/logout">Выйти</a></nav>
{% block content %}{% endblock %}</div>{% endblock %}'''

T['admin_login.html'] = r'''{% extends 'base.html' %}{% block body %}<div class="wrap" style="max-width:420px;padding-top:60px"><form class="box" method="post"><h1 style="font-size:26px;margin-bottom:6px">Вход для владельца</h1><p class="hint" style="margin-bottom:16px">Введите пароль администратора.</p>
<label class="f">Пароль<input type="password" name="password" required autofocus autocomplete="current-password"></label><button class="btn blk">Войти</button></form></div>{% endblock %}'''

T['admin_dashboard.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<h1 class="h1">Обзор</h1>
{% if default_pw %}<div class="note">Пароль администратора стандартный. Задайте свой в переменной <b>ADMIN_PASSWORD</b> на сервере.</div>{% endif %}
{% if not methods %}<div class="note">Реквизиты для оплаты не добавлены. <a href="/admin/payments"><b>Добавить</b></a></div>{% endif %}
<div class="stats"><div class="box stat"><b>{{ pc }}</b><span>Товаров</span></div><div class="box stat"><b>{{ oc }}</b><span>Заказов</span></div><div class="box stat"><b>{{ nc }}</b><span>Новых</span></div><div class="box stat"><b>{{ revenue|money }}</b><span>Сумма заказов, сом</span></div></div>
<h2 style="font-size:20px;margin-bottom:12px">Последние заказы</h2>{% include 'admin_orders_table.html' %}{% endblock %}'''

T['admin_orders_table.html'] = r'''<div class="scroll"><table class="tbl"><thead><tr><th>№</th><th>Клиент</th><th>Телефон</th><th>Сумма</th><th>Статус</th><th>Дата</th></tr></thead><tbody>
{% for o in orders %}<tr><td><a href="/admin/orders/{{ o.id }}"><b>#{{ o.id }}</b></a></td><td>{{ o.customer_name }}</td><td><a href="tel:{{ o.customer_phone|tel }}">{{ o.customer_phone }}</a></td><td>{{ o.total_price|money }} сом</td>
<td><span class="tag {{ 'new' if o.status=='Новый' else 'ok' if o.status in ('Оплачен','Готов','Выдан') else 'bad' if o.status=='Отменён' else '' }}">{{ o.status }}</span></td><td>{{ o.created_at.strftime('%d.%m %H:%M') }}</td></tr>
{% else %}<tr><td colspan="6" style="text-align:center;color:var(--mut);padding:30px">Заказов пока нет</td></tr>{% endfor %}</tbody></table></div>'''

T['admin_orders.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<h1 class="h1">Заказы</h1>
<div class="chips"><a class="chip {{ 'on' if not st }}" href="/admin/orders">Все</a>{% for s in statuses %}<a class="chip {{ 'on' if st==s }}" href="/admin/orders?status={{ s }}">{{ s }}</a>{% endfor %}</div>
{% include 'admin_orders_table.html' %}{% endblock %}'''

T['admin_order.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<p class="crumbs"><a href="/admin/orders">← Все заказы</a></p><h1 class="h1">Заказ №{{ o.id }}</h1>
<div class="two"><div class="box"><h3 style="font-size:17px;margin-bottom:8px">Состав</h3>{% for i in o.items %}<div style="display:flex;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid var(--line)"><span>{{ i.product.name if i.product else 'Товар удалён' }} × {{ i.quantity }}</span><b>{{ (i.price*i.quantity)|money }} сом</b></div>{% endfor %}
<div style="display:flex;justify-content:space-between;padding-top:12px;font:800 20px Manrope,sans-serif"><span>Итого</span><span>{{ o.total_price|money }} сом</span></div></div>
<div><div class="box" style="margin-bottom:14px"><div><span class="hint">Клиент</span><br><b>{{ o.customer_name }}</b></div><div style="margin-top:8px"><span class="hint">Телефон</span><br><a href="tel:{{ o.customer_phone|tel }}"><b>{{ o.customer_phone }}</b></a></div>
{% if o.comment %}<div style="margin-top:8px"><span class="hint">Комментарий</span><br>{{ o.comment }}</div>{% endif %}<div style="margin-top:8px"><span class="hint">Создан</span><br>{{ o.created_at.strftime('%d.%m.%Y %H:%M') }}</div></div>
<form class="box" method="post" action="/admin/orders/{{ o.id }}/status"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><label class="f">Статус<select name="status">{% for s in statuses %}<option {{ 'selected' if o.status==s }}>{{ s }}</option>{% endfor %}</select></label><button class="btn blk">Обновить статус</button></form>
<form method="post" action="/admin/orders/{{ o.id }}/delete" onsubmit="return confirm('Удалить заказ?')" style="margin-top:12px"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><button class="btn red blk">Удалить заказ</button></form></div></div>{% endblock %}'''

T['admin_products.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<div class="tools"><h1 class="h1" style="margin:0">Товары</h1><a class="btn" href="/admin/products/new">Добавить товар</a></div>
<form style="margin:16px 0"><div class="search" style="max-width:none"><svg class="i"><use href="#i-search"/></svg><input name="q" value="{{ q }}" placeholder="Найти товар" aria-label="Поиск"></div></form>
<div class="scroll"><table class="tbl"><thead><tr><th>Товар</th><th>Категория</th><th>Цена</th><th></th></tr></thead><tbody>
{% for p in products %}<tr><td><div class="cell"><img class="thumb" src="{{ p|img }}" alt=""><b>{{ p.name }}</b></div></td><td>{{ p.category.name if p.category else '—' }}</td><td>{{ p.price|money if p.price>0 else 'по запросу' }}</td>
<td><div class="acts"><a class="btn sec sm" href="/admin/products/{{ p.id }}">Изменить</a><form method="post" action="/admin/products/{{ p.id }}/delete" onsubmit="return confirm('Удалить товар?')"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><button class="btn red sm">Удалить</button></form></div></td></tr>
{% else %}<tr><td colspan="4" style="text-align:center;color:var(--mut);padding:30px">Товаров нет</td></tr>{% endfor %}</tbody></table></div>{% endblock %}'''

T['admin_product_form.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<p class="crumbs"><a href="/admin/products">← Товары</a></p><h1 class="h1">{{ 'Изменить товар' if p else 'Новый товар' }}</h1>
<form class="box" method="post" enctype="multipart/form-data" style="max-width:640px"><input type="hidden" name="_csrf" value="{{ csrf_token() }}">
<label class="f">Название<input name="name" required value="{{ p.name if p else '' }}"></label>
<label class="f">Цена, сом <span class="hint">(0 — «Цена по запросу»)</span><input name="price" type="number" min="0" step="1" value="{{ p.price|int if p else '' }}"></label>
<label class="f">Категория<select name="category_id"><option value="">Без категории</option>{% for c in categories %}<option value="{{ c.id }}" {{ 'selected' if p and p.category_id==c.id }}>{{ c.name }}</option>{% endfor %}</select></label>
<label class="f">Описание<textarea name="description">{{ p.description if p and p.description else '' }}</textarea></label>
<label class="f">Фото<input type="file" name="photo" accept="image/*" data-preview="#pv"></label><img id="pv" class="thumb" style="width:120px;height:120px;margin:-6px 0 16px" src="{{ p|img if p else '' }}" {% if not p %}hidden{% endif %} alt="">
<button class="btn">Сохранить</button></form>{% endblock %}'''

T['admin_categories.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<h1 class="h1">Категории</h1>
<form class="acts" method="post" style="margin:12px 0 18px"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><input class="chip" style="width:280px;max-width:100%;height:46px;font:400 16px Inter,sans-serif" name="name" required placeholder="Новая категория"><button class="btn">Добавить</button></form>
<div class="scroll"><table class="tbl"><tbody>{% for c in cats %}<tr><td><b>{{ c.name }}</b></td><td style="text-align:right"><form method="post" action="/admin/categories/{{ c.id }}/delete" onsubmit="return confirm('Удалить категорию? Товары останутся без категории.')"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><button class="btn red sm">Удалить</button></form></td></tr>
{% else %}<tr><td style="text-align:center;color:var(--mut);padding:30px">Категорий нет</td></tr>{% endfor %}</tbody></table></div>{% endblock %}'''

T['admin_payments.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<h1 class="h1">Реквизиты для оплаты</h1>
<p class="hint" style="margin-bottom:6px">Клиент увидит их при оформлении предзаказа и на странице подтверждения. Добавьте один или несколько способов: банк, кошелёк, QR-код.</p>
<div class="two eq"><div>{% for m in methods %}<div class="pay"><div><h4>{{ m.title }} {% if not m.active %}<span class="tag bad">скрыт</span>{% endif %}</h4><pre>{{ m.details }}</pre>
<div class="acts"><a class="btn sec sm" href="/admin/payments?edit={{ m.id }}">Изменить</a><form method="post" action="/admin/payments/{{ m.id }}/toggle"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><button class="btn sec sm">{{ 'Скрыть' if m.active else 'Показать' }}</button></form>
<form method="post" action="/admin/payments/{{ m.id }}/delete" onsubmit="return confirm('Удалить реквизиты?')"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><button class="btn red sm">Удалить</button></form></div></div>{% if m.qr_url %}<img class="qr" src="{{ m.qr_url }}" alt="QR">{% endif %}</div>
{% else %}<div class="box" style="color:var(--mut)">Пока нет ни одного способа оплаты. Заполните форму рядом.</div>{% endfor %}</div>
<form class="box" method="post" action="/admin/payments/save" enctype="multipart/form-data"><h3 style="font-size:17px;margin-bottom:14px">{{ 'Изменить способ оплаты' if edit else 'Новый способ оплаты' }}</h3>
<input type="hidden" name="_csrf" value="{{ csrf_token() }}"><input type="hidden" name="id" value="{{ edit.id if edit else '' }}">
<label class="f">Название<input name="title" required maxlength="80" placeholder="Например, Оптима Банк" value="{{ edit.title if edit else '' }}"></label>
<label class="f">Реквизиты<textarea name="details" placeholder="Номер карты или счёта&#10;Получатель&#10;Телефон кошелька">{{ edit.details if edit and edit.details else '' }}</textarea></label>
<label class="f">QR-код или фото <span class="hint">(необязательно)</span><input type="file" name="qr" accept="image/*" data-preview="#qv"></label>
<img id="qv" class="qr" style="width:120px;height:120px;object-fit:contain;margin:-6px 0 14px;border:1px solid var(--line);" src="{{ edit.qr_url if edit and edit.qr_url else '' }}" {% if not (edit and edit.qr_url) %}hidden{% endif %} alt="">
{% if edit and edit.qr_url %}<label class="ck"><input type="checkbox" name="remove_qr"> Удалить текущий QR</label>{% endif %}
<label class="ck"><input type="checkbox" name="active" {{ 'checked' if not edit or edit.active }}> Показывать клиентам</label>
<div class="acts"><button class="btn">Сохранить</button>{% if edit %}<a class="btn sec" href="/admin/payments">Отмена</a>{% endif %}</div></form></div>{% endblock %}'''

T['admin_contacts.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<h1 class="h1">Контакты</h1>
<form class="box" method="post" style="max-width:560px"><input type="hidden" name="_csrf" value="{{ csrf_token() }}">
<label class="f">Номера для связи <span class="hint">(каждый с новой строки)</span><textarea name="phones" placeholder="+996 700 123 456">{{ phones_raw }}</textarea></label>
<label class="f">WhatsApp <span class="hint">(номер, необязательно)</span><input name="whatsapp" value="{{ whatsapp }}" placeholder="+996700123456"></label><button class="btn">Сохранить</button></form>
{% if bot_on %}<form class="box" method="post" action="/admin/bot/webhook" style="max-width:560px;margin-top:16px"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><h3 style="font-size:17px;margin-bottom:6px">Telegram-бот</h3><p class="hint" style="margin-bottom:12px">Подключает бота к этому сайту. Нажмите после первого запуска или смены адреса.</p><button class="btn sec">Подключить webhook</button></form>{% endif %}{% endblock %}'''
