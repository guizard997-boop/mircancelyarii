# -*- coding: utf-8 -*-
"""Шаблоны и стили сайта. Цвета, шрифты и иллюстрации берутся из темы (themes.py)."""
from themes import GRAIN

CSS = r'''
:root{--bg:#F5F6F8}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;background:var(--bg)}
body{margin:0;font:16px/1.55 var(--bf);color:var(--ink);background:var(--bgimg),radial-gradient(1200px 600px at 50% -10%,var(--bg2) 0,transparent 70%) var(--bg);background-attachment:fixed;min-height:100vh;display:flex;flex-direction:column}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:200;opacity:var(--grain);background-image:__GRAIN__}
main{flex:1}h1,h2,h3,h4{font-family:var(--hf);font-weight:var(--hw);letter-spacing:.01em;line-height:1.08;margin:0;text-transform:var(--hup)}
a{color:inherit;text-decoration:none}img{display:block;max-width:100%}button{font-family:inherit}
::selection{background:var(--ink);color:var(--bg)}::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--line)}
.wrap{width:100%;max-width:1200px;margin:0 auto;padding:0 20px}
svg.i{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;flex:none}
:focus-visible{outline:2px dashed var(--ink);outline-offset:3px}
.hdr{position:sticky;top:0;z-index:40;background:var(--hd);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.hdr .wrap{display:flex;align-items:center;gap:16px;height:68px}
.logo{display:flex;align-items:center;gap:12px;font:var(--hw) calc(var(--k)*24px) var(--hf);letter-spacing:var(--ls);text-transform:var(--up);white-space:nowrap}
.logo b{display:grid;place-items:center;width:36px;height:36px;border:1px solid var(--lgb);background:var(--lgbg);color:var(--lgfg);border-radius:var(--r);font-size:19px}
.search{flex:1;max-width:520px;position:relative}
.search input{width:100%;height:44px;border:1px solid var(--line);background:var(--sf);padding:0 16px 0 44px;font:400 15px var(--bf);color:var(--ink);border-radius:min(var(--r),22px)}
.search input::placeholder{color:var(--mut)}.search svg{position:absolute;left:15px;top:12px;color:var(--mut)}
.ibtn{position:relative;display:grid;place-items:center;width:44px;height:44px;border:1px solid var(--line);background:var(--sf);border-radius:min(var(--r),22px)}.ibtn:hover{border-color:var(--ink)}
.badge{position:absolute;top:-7px;right:-7px;min-width:20px;height:20px;padding:0 5px;border-radius:999px;background:var(--acc);color:var(--on-acc);font:800 11px/20px var(--bf);text-align:center}.badge[hidden]{display:none}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:48px;padding:0 26px;border:1px solid var(--pri);border-radius:var(--r);background:var(--pri);color:var(--on-pri);font:700 13px var(--bf);letter-spacing:var(--ls);text-transform:var(--up);cursor:pointer;transition:background .15s,color .15s,transform .1s}
.btn:hover{background:var(--bg);color:var(--pri)}.btn:active{transform:scale(.98)}.btn[disabled]{opacity:.5}
.btn.sec{background:transparent;color:var(--ink);border-color:var(--line)}.btn.sec:hover{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.btn.sm{height:34px;padding:0 14px;font-size:11px}.btn.red{background:transparent;color:var(--ink);border:1px dashed var(--mut)}.btn.red:hover{background:var(--ink);color:var(--bg)}.btn.blk{width:100%}
.chips{display:flex;gap:8px;overflow-x:auto;padding:16px 0;scrollbar-width:none}.chips::-webkit-scrollbar{display:none}
.chip{flex:none;height:38px;padding:0 16px;display:inline-flex;align-items:center;border:1px solid var(--line);background:var(--sf);border-radius:min(var(--r),19px);font-size:12px;font-weight:600;letter-spacing:var(--ls);text-transform:var(--up);color:var(--mut)}
.chip:hover{border-color:var(--ink);color:var(--ink)}.chip.on{background:var(--pri);color:var(--on-pri);border-color:var(--pri)}
.hero{position:relative;display:grid;grid-template-columns:1.05fr 1fr;gap:32px;align-items:center;padding:56px 0 28px}
.hero h1{font-size:calc(var(--k)*clamp(46px,7vw,96px));text-shadow:0 0 34px var(--glow)}.hero h1 em{font-style:var(--emst);color:var(--em);font-weight:inherit}
.hero p{color:var(--mut);font-size:18px;max-width:460px;margin:22px 0 32px}
.scene{width:100%;height:auto;display:block;overflow:visible}
.bat{transform-box:fill-box;transform-origin:center;animation:flap .45s ease-in-out infinite alternate}@keyframes flap{to{transform:scaleY(.72) translateY(2px)}}
.floaty{transform-box:fill-box;transform-origin:center;animation:flo 5s ease-in-out infinite}@keyframes flo{50%{transform:translateY(-12px) rotate(3deg)}}
.fog{position:absolute;left:-10%;right:-10%;bottom:-40px;height:180px;background:radial-gradient(ellipse at 50% 100%,var(--yg),transparent 70%);pointer-events:none}
main{overflow-x:clip}
.sec-h{display:flex;justify-content:space-between;align-items:end;margin:36px 0 18px;padding-bottom:10px;border-bottom:1px solid var(--line)}.sec-h h2{font-size:calc(var(--k)*38px)}
.sec-h a{color:var(--mut);font-weight:600;font-size:12px;letter-spacing:var(--ls);text-transform:var(--up)}.sec-h a:hover{color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px}
.pc{background:var(--sf);border:1px solid var(--line);border-radius:var(--rc);overflow:hidden;display:flex;flex-direction:column;transition:border-color .2s,transform .2s,box-shadow .2s}
@media(hover:hover){.pc:hover{border-color:var(--ink);transform:translateY(-3px);box-shadow:0 18px 40px -20px var(--hv)}}
.pc .im{position:relative;display:block;aspect-ratio:1;background:var(--sf2);overflow:hidden}
.pc .im img,.ci img{width:100%;height:100%;object-fit:cover;filter:var(--imgf);transition:filter .35s,transform .5s}
@media(hover:hover){.pc:hover .im img{filter:none;transform:scale(1.04)}}
.pc .bd{padding:14px;display:flex;flex-direction:column;gap:6px;flex:1}.pc .cat{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut)}
.pc h3{font:600 calc(var(--k)*23px)/1.12 var(--hf);letter-spacing:0;text-transform:none;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.25em}
.pc .row{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:8px}
.price{font:var(--hw) calc(var(--k)*28px) var(--hf);color:var(--price);text-transform:none}.price small{font:500 11px var(--bf);color:var(--mut);letter-spacing:.1em;text-transform:uppercase}
.add{width:42px;height:42px;border:1px solid var(--pri);border-radius:min(var(--r),21px);background:var(--pri);color:var(--on-pri);display:grid;place-items:center;cursor:pointer;transition:background .15s,color .15s}.add:hover{background:var(--bg);color:var(--pri)}
.tools{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}.tools select{height:40px;border:1px solid var(--line);border-radius:var(--r);padding:0 12px;background:var(--sf);color:var(--ink);font:500 14px var(--bf)}
.pager{display:flex;gap:6px;justify-content:center;margin:30px 0}.pager a{min-width:40px;height:40px;display:grid;place-items:center;border:1px solid var(--line);border-radius:var(--r);background:var(--sf);font-weight:600}.pager a.on{background:var(--pri);color:var(--on-pri);border-color:var(--pri)}
.empty{text-align:center;padding:64px 0;color:var(--mut)}.empty h2{color:var(--ink);margin-bottom:8px;font-size:calc(var(--k)*40px)}.empty .btn{margin-top:20px}
.ill{width:96px;height:auto;margin:0 auto 14px;display:block;fill:var(--mut);stroke:none}
.crumbs{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);padding-top:22px}.crumbs a:hover{color:var(--ink)}
.pd{display:grid;grid-template-columns:1fr 1fr;gap:44px;padding:22px 0 10px}
.pd .ph{aspect-ratio:1;overflow:hidden;background:var(--sf2);border:1px solid var(--line);border-radius:var(--rc)}.pd .ph img{width:100%;height:100%;object-fit:cover}
.pd h1{font-size:calc(var(--k)*clamp(34px,4.6vw,60px));margin:10px 0 16px}.pd .price{font-size:calc(var(--k)*42px);margin-bottom:18px}
.pd .desc{color:var(--mut);max-width:520px;white-space:pre-line}.buy{display:flex;gap:12px;margin-top:28px;flex-wrap:wrap}
.qty{display:inline-flex;align-items:center;border:1px solid var(--line);border-radius:var(--r);background:var(--sf);height:48px}
.qty button{width:42px;height:100%;border:0;background:none;cursor:pointer;color:var(--ink);display:grid;place-items:center;border-radius:var(--r)}.qty button:hover{background:var(--pri);color:var(--on-pri)}
.qty input{width:44px;border:0;text-align:center;font:600 15px var(--bf);background:none;color:var(--ink);height:100%;-moz-appearance:textfield}
.qty input::-webkit-outer-spin-button,.qty input::-webkit-inner-spin-button{-webkit-appearance:none}
.two{display:grid;grid-template-columns:1fr 360px;gap:24px;align-items:start;padding:20px 0 10px}.two.eq{grid-template-columns:1fr 1fr}
.box{background:var(--sf);border:1px solid var(--line);border-radius:var(--rc);padding:22px}
.h1{font-size:calc(var(--k)*46px);margin:28px 0 6px}
.ci{display:grid;grid-template-columns:72px 1fr auto;gap:14px;align-items:center;padding:14px 0;border-bottom:1px solid var(--line)}.ci:last-child{border:0}
.ci img{width:72px;height:72px;background:var(--sf2);border-radius:var(--r)}.ci .nm{font:600 calc(var(--k)*22px) var(--hf);text-transform:none}.ci .sm{color:var(--mut);font-size:14px}
.ctl{display:flex;align-items:center;gap:10px}.ctl .qty{height:38px}.ctl .qty button{width:34px}.ctl .qty span{min-width:26px;text-align:center;font-weight:600}
.ctl .x{border:0;background:none;color:var(--mut);cursor:pointer;display:grid;place-items:center;width:34px;height:34px}.ctl .x:hover{color:var(--ink)}
.sum{position:sticky;top:90px}.sum .tot{display:flex;justify-content:space-between;align-items:baseline;font-weight:600;margin:14px 0 18px}.sum .tot b{font:var(--hw) calc(var(--k)*34px) var(--hf)}
.sum .ln{display:flex;justify-content:space-between;gap:10px;font-size:14px;color:var(--mut);padding:3px 0}
label.f{display:block;font-weight:600;font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:14px}
label.f input,label.f select,label.f textarea{display:block;width:100%;margin-top:7px;height:48px;border:1px solid var(--line);border-radius:var(--r);padding:0 14px;font:400 16px var(--bf);background:var(--inp);color:var(--ink);text-transform:none;letter-spacing:0}
label.f textarea{height:auto;padding:12px 14px;min-height:110px;resize:vertical}label.f input[type=file]{padding:11px 12px;height:auto}
label.ck{display:flex;gap:10px;align-items:center;font-weight:500;margin-bottom:14px}label.ck input{accent-color:var(--pri)}
input:focus,select:focus,textarea:focus{outline:1px solid var(--pri);outline-offset:0;border-color:var(--pri)}
.hint{font-size:13px;color:var(--mut);font-weight:400;letter-spacing:0;text-transform:none}
.pay{border:1px solid var(--line);border-radius:var(--rc);padding:16px;background:var(--sf);display:grid;grid-template-columns:1fr auto;gap:14px;margin-bottom:12px}
.pay h4{margin:0 0 8px;font:var(--hw) calc(var(--k)*26px) var(--hf);text-transform:none}.pay pre{margin:0 0 12px;white-space:pre-wrap;font:500 14px/1.7 var(--bf);word-break:break-word}
.pay .qr{width:120px;height:120px;object-fit:contain;border:1px solid var(--line);background:#fff;padding:4px;border-radius:var(--r)}
.ok-ic{display:grid;place-items:center;width:72px;height:72px;border:1px solid var(--ink);border-radius:var(--r);margin-bottom:16px}.ok-ic svg{width:44px;height:44px;fill:var(--ink);stroke:none}.ok-ic svg.i{fill:none;stroke:var(--ink);stroke-width:2}
.an{display:flex;gap:6px;overflow-x:auto;padding:16px 0 4px;scrollbar-width:none}.an a{flex:none;padding:8px 16px;border:1px solid transparent;border-radius:min(var(--r),18px);font-weight:600;font-size:12px;letter-spacing:var(--ls);text-transform:var(--up);color:var(--mut)}.an a.on{border-color:var(--ink);color:var(--ink)}.an a:hover{color:var(--ink)}.an .out{margin-left:auto}
.scroll{overflow-x:auto}
.tbl{width:100%;border-collapse:collapse;background:var(--sf);border:1px solid var(--line);font-size:14px}
.tbl th{background:var(--sf2);text-align:left;color:var(--mut);font-weight:600;padding:10px 14px;white-space:nowrap;font-size:11px;letter-spacing:.12em;text-transform:uppercase}.tbl td{padding:12px 14px;border-top:1px solid var(--line);vertical-align:middle}
.tag{display:inline-block;padding:2px 10px;border:1px solid var(--mut);border-radius:999px;font:600 11px var(--bf);letter-spacing:.08em;text-transform:uppercase;color:var(--mut);white-space:nowrap}
.tag.new{background:var(--acc);color:var(--on-acc);border-color:var(--acc)}.tag.ok{border-color:var(--ink);color:var(--ink)}.tag.bad{border-style:dashed;color:var(--mut);text-decoration:line-through}.tag.warn{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:14px 0 22px}.stat{display:block}.stat b{display:block;font:var(--hw) calc(var(--k)*44px) var(--hf)}.stat span{color:var(--mut);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.thumb{width:44px;height:44px;object-fit:cover;background:var(--sf2);border-radius:var(--r)}.cell{display:flex;align-items:center;gap:12px}
.note{border:1px dashed var(--mut);border-radius:var(--r);padding:12px 14px;font-size:14px;margin:12px 0}
.acts{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.acts form{margin:0}
.tgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}
.tcard{border:1px solid var(--line);background:var(--sf);border-radius:var(--rc);overflow:hidden;display:flex;flex-direction:column}.tcard.cur{outline:2px solid var(--pri)}
.tcard .sw{display:flex;height:60px}.tcard .sw i{flex:1}.tcard .bd{padding:14px;display:flex;flex-direction:column;gap:6px;flex:1}.tcard h3{font-size:calc(var(--k)*26px);text-transform:none}
.pvbar{position:fixed;left:50%;transform:translateX(-50%);bottom:20px;z-index:300;background:var(--ink);color:var(--bg);padding:8px 10px 8px 18px;border-radius:999px;display:flex;gap:10px;align-items:center;font-size:14px;font-weight:600;box-shadow:0 12px 40px -8px rgba(0,0,0,.4);max-width:calc(100% - 24px)}
.pvbar form{margin:0}.pvbar .btn{height:34px;padding:0 14px;font-size:11px;background:var(--bg);color:var(--ink);border-color:var(--bg)}.pvbar .btn.sec{background:transparent;color:var(--bg);border-color:var(--bg)}
.ticker{overflow:hidden;background:var(--tkbg);color:var(--tkfg);position:relative;z-index:31}
.tk{display:flex;width:max-content;animation:tk 46s linear infinite}.tkg{display:flex;align-items:center;gap:30px;padding:9px 30px 9px 0}
.tkg span{font:600 11px var(--bf);letter-spacing:.2em;text-transform:uppercase;white-space:nowrap}.tkg svg{width:15px;height:15px;fill:currentColor;stroke:none;flex:none}@keyframes tk{to{transform:translateX(-50%)}}
.deco{position:relative;height:0;z-index:30;pointer-events:none}
.orn{display:flex;align-items:center;gap:16px;margin:34px 0 6px;color:var(--mut)}.orn i{flex:1;height:1px;background:linear-gradient(90deg,transparent,var(--line),transparent)}.orn svg{width:26px;height:26px;fill:currentColor;stroke:none}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:16px;margin:6px 0 10px}
.tile{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;padding:30px 14px 20px;border:1px solid var(--line);border-radius:var(--tile);background:var(--sf);transition:background .2s,color .2s,transform .2s}
.tile b{font:var(--hw) calc(var(--k)*24px)/1.1 var(--hf);text-transform:none}.tile span{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.tile-i{width:26px;height:26px;color:var(--mut)}.tile-i.fill{fill:currentColor;stroke:none}.tile-i.stroke{fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round}
@media(hover:hover){.tile:hover{background:var(--pri);color:var(--on-pri);transform:translateY(-4px)}.tile:hover .tile-i,.tile:hover span{color:var(--on-pri)}}
.yard{position:relative;height:130px;margin-top:70px;background:linear-gradient(to top,var(--yg),transparent 80%);pointer-events:none}
.yard svg.bg{position:absolute;inset:0;width:100%;height:100%;display:block}.yard *{pointer-events:auto}
.ft{position:relative;background:var(--sf);border-top:1px solid var(--line);padding:42px 0 8px}
.ft .wrap{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:28px}.ft h4{font-size:calc(var(--k)*24px);margin-bottom:10px;text-transform:none}.ft a{display:block;color:var(--mut);font-size:14px;padding:3px 0}.ft a:hover{color:var(--ink)}
.copy{color:var(--mut);font-size:12px;letter-spacing:.08em;padding-top:26px;padding-bottom:22px}
.nav-b{display:none;position:fixed;left:0;right:0;bottom:0;z-index:40;background:var(--hd);backdrop-filter:blur(12px);border-top:1px solid var(--line);grid-template-columns:repeat(3,1fr);padding-bottom:env(safe-area-inset-bottom)}
.nav-b a{display:flex;flex-direction:column;align-items:center;gap:2px;padding:9px 0 8px;font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);position:relative}.nav-b a.on{color:var(--ink)}.nav-b .badge{top:3px;right:calc(50% - 24px)}
#toasts{position:fixed;left:50%;transform:translateX(-50%);bottom:24px;z-index:300;display:flex;flex-direction:column;gap:8px;align-items:center;pointer-events:none;width:calc(100% - 24px);max-width:420px}
.toast{background:var(--ink);color:var(--bg);padding:12px 18px;border-radius:min(var(--r),14px);font-size:14px;font-weight:600;box-shadow:0 12px 40px -8px var(--hv);animation:tin .2s ease both}.toast.bad{outline:1px dashed var(--bg);outline-offset:-5px}.toast.out{animation:tout .2s ease both}
@keyframes tin{from{opacity:0;transform:translateY(10px)}}@keyframes tout{to{opacity:0;transform:translateY(6px)}}
.err{text-align:center;padding:70px 0 20px}.err .ill{width:120px}.err .code{font:var(--hw) calc(var(--k)*clamp(90px,18vw,180px))/1 var(--hf);text-shadow:0 0 40px var(--glow)}.err h1{font-size:calc(var(--k)*38px);margin:6px 0 10px}.err p{color:var(--mut);margin-bottom:24px}
.fxl{position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:34}.fxp{position:absolute;top:-30px;color:var(--fx)}.fxp svg{width:100%;height:100%;display:block}
.fxp.stroke svg{fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round}.fxp.fill svg{fill:currentColor;stroke:none}
.fall{animation:fall linear infinite}@keyframes fall{from{transform:translate3d(0,-5vh,0) rotate(0)}to{transform:translate3d(var(--dx),110vh,0) rotate(var(--rot))}}
.rise{top:auto;bottom:-30px;animation:rise linear infinite}@keyframes rise{from{transform:translate3d(0,0,0) rotate(0)}to{transform:translate3d(var(--dx),-115vh,0) rotate(var(--rot))}}
.twk{animation:twk ease-in-out infinite alternate}@keyframes twk{from{opacity:.1;transform:scale(.6)}to{opacity:.9;transform:scale(1.1)}}
[data-boo]{cursor:pointer}
@media(max-width:860px){.hero,.pd,.two,.two.eq{grid-template-columns:1fr}.sum{position:static}.ft .wrap{grid-template-columns:1fr 1fr}.hero{padding-top:44px}.scene{max-width:420px;margin:0 auto}}
@media(max-width:600px){.wrap{padding:0 14px}.grid{grid-template-columns:repeat(2,1fr);gap:10px}.logo span{display:none}.cart-h{display:none}.pc .bd{padding:10px}.pc h3{font-size:calc(var(--k)*19px)}.nav-b{display:grid}body{padding-bottom:64px}#toasts,.pvbar{bottom:78px}.pay{grid-template-columns:1fr}.ci{grid-template-columns:64px 1fr}.ci .ctl{grid-column:1/-1}.ft .wrap{grid-template-columns:1fr}.h1{font-size:calc(var(--k)*38px)}.dang.d2{display:none}.yard{height:96px;margin-top:50px}.tile{padding:22px 10px 14px}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}html{scroll-behavior:auto}.fxl{display:none}}
'''
CSS = CSS.replace('__GRAIN__', GRAIN)

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
var boo=['Бу!','Тсс, они слушают','Не бойтесь, он декоративный','С Хэллоуином','Свечи не тушить'];
document.addEventListener('click',function(e){if(e.target.closest('[data-boo]')){toast(boo[Math.floor(Math.random()*boo.length)])}});
})();

(function(){var h=document.documentElement,fx=h.dataset.fx;if(!fx||fx==='none'||(window.matchMedia&&matchMedia('(prefers-reduced-motion:reduce)').matches))return;
var n=+h.dataset.fxn||30,cols=(h.dataset.fxc||'').split(',').filter(Boolean),L=document.createElement('div');L.className='fxl';L.setAttribute('aria-hidden','true');
var map={snow:['flake','stroke','fall'],petals:['petal','fill','fall'],leaves:['leaf','fill','fall'],hearts:['heart','fill','rise'],bubbles:['bub','stroke','rise'],stars:['sparkle','fill','twk'],confetti:['rect','fill','fall']};
var m=map[fx]||map.snow;
for(var i=0;i<n;i++){var e=document.createElement('i'),tw=m[2]==='twk',s=tw?6+Math.random()*10:8+Math.random()*16;e.className='fxp '+m[1]+' '+m[2];
e.style.cssText='left:'+Math.random()*100+'%;width:'+s+'px;height:'+s+'px;animation-duration:'+(tw?2+Math.random()*4:9+Math.random()*14)+'s;animation-delay:-'+Math.random()*20+'s;--dx:'+(Math.random()*120-60)+'px;--rot:'+(Math.random()*540-270)+'deg;'+(tw?'top:'+Math.random()*100+'%;':'opacity:'+(.4+Math.random()*.5)+';')+(cols.length?'color:'+cols[i%cols.length]+';':'');
e.innerHTML='<svg viewBox="0 0 24 24"><use href="#i-'+m[0]+'"/></svg>';L.appendChild(e)}
document.body.appendChild(L)})();
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

T['base.html'] = r'''<!doctype html><html lang="ru" {{ thx.fx_attrs }}><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="{{ thx.theme_color }}">
<link rel="icon" href="data:image/svg+xml;utf8,{{ thx.favicon }}">
<title>{{ title }} — Мир канцелярии</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{{ thx.fonts }}" rel="stylesheet">
<style>{% raw %}''' + CSS + r'''{% endraw %}</style><style>{{ thx.css }}</style></head><body>
''' + SPRITE + r'''{{ motifs }}
{% block sky %}{{ thx.sky }}{% endblock %}
<header class="hdr"><div class="wrap">
<a class="logo" href="/" aria-label="Мир канцелярии">{{ thx.logo }}<span>Мир канцелярии</span></a>
<form class="search" action="/catalog" role="search"><svg class="i"><use href="#i-search"/></svg><input id="q" type="search" name="q" value="{{ request.args.get('q','') }}" placeholder="Поиск по каталогу" autocomplete="off" aria-label="Поиск"></form>
<a class="ibtn cart-h" href="/cart" aria-label="Корзина"><svg class="i"><use href="#i-bag"/></svg><span class="badge" data-badge {% if not cart_count %}hidden{% endif %}>{{ cart_count }}</span></a>
</div></header>
{% block deco %}{{ thx.deco }}{% endblock %}
{% with m=get_flashed_messages(with_categories=true) %}{% if m %}<div id="flash" hidden>{% for c,t in m %}<i data-c="{{ c }}">{{ t }}</i>{% endfor %}</div>{% endif %}{% endwith %}
<main>{% block body %}{% endblock %}</main>
{% block yard %}{{ thx.yard }}{% endblock %}
<footer class="ft"><div class="wrap">
<div><div class="logo">{{ thx.logo }}<span>Мир канцелярии</span></div></div>
<div><h4>Каталог</h4>{% for c in categories[:8] %}<a href="/catalog?category={{ c.id }}">{{ c.name }}</a>{% endfor %}<a href="/catalog">Все товары</a></div>
<div><h4>Связаться</h4>{% for p in phones %}<a href="tel:{{ p|tel }}">{{ p }}</a>{% endfor %}{% if whatsapp %}<a href="https://wa.me/{{ whatsapp|tel|replace('+','') }}" rel="noopener">WhatsApp</a>{% endif %}{% if not phones and not whatsapp %}<a href="/cart">Оформить предзаказ</a>{% endif %}</div>
</div><div class="wrap copy">© 2026 Мир канцелярии &nbsp;·&nbsp; {{ th.tag }}</div></footer>
<nav class="nav-b" aria-label="Навигация">
<a href="/" class="{{ 'on' if request.path=='/' }}"><svg class="i"><use href="#i-home"/></svg>Главная</a>
<a href="/catalog" class="{{ 'on' if request.path.startswith('/catalog') }}"><svg class="i"><use href="#i-grid"/></svg>Каталог</a>
<a href="/cart" class="{{ 'on' if request.path.startswith('/cart') }}"><svg class="i"><use href="#i-bag"/></svg>Корзина<span class="badge" data-badge {% if not cart_count %}hidden{% endif %}>{{ cart_count }}</span></a>
</nav>
{% if preview %}<div class="pvbar"><span>Предпросмотр: {{ th.name }}</span><form method="post" action="/admin/theme/set"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><input type="hidden" name="id" value="{{ th.id }}"><button class="btn">Применить</button></form><a class="btn sec" href="/admin/theme/preview/stop">Закрыть</a></div>{% endif %}
<div id="toasts" aria-live="polite"></div>
<script>{% raw %}''' + JS + r'''{% endraw %}</script></body></html>'''

T['macros.html'] = r'''{% macro card(p) %}<article class="pc"><a class="im" href="/product/{{ p.id }}"><img src="{{ p|img }}" alt="{{ p.name }}" loading="lazy" decoding="async"></a>
<div class="bd">{% if p.category %}<span class="cat">{{ p.category.name }}</span>{% endif %}<a href="/product/{{ p.id }}"><h3>{{ p.name }}</h3></a>
<div class="row">{% if p.price and p.price>0 %}<span class="price">{{ p.price|money }} <small>сом</small></span>{% else %}<span class="price"><small>Цена по запросу</small></span>{% endif %}
<form action="/cart/add/{{ p.id }}" method="post" data-add><button class="add" aria-label="В корзину: {{ p.name }}"><svg class="i"><use href="#i-plus"/></svg></button></form></div></div></article>{% endmacro %}
{% macro pay(m) %}<div class="pay"><div><h4>{{ m.title }}</h4>{% if m.details %}<pre>{{ m.details }}</pre><button type="button" class="btn sec sm" data-copy="{{ m.details }}"><svg class="i" style="width:16px;height:16px"><use href="#i-copy"/></svg>Копировать</button>{% endif %}</div>{% if m.qr_url %}<img class="qr" src="{{ m.qr_url }}" alt="QR: {{ m.title }}">{% endif %}</div>{% endmacro %}'''

T['home.html'] = r'''{% extends 'base.html' %}{% from 'macros.html' import card %}{% block body %}<div class="wrap">
<section class="hero"><div style="position:relative"><h1>{{ th.hero[0] }} <em>{{ th.hero[1] }}</em></h1><p>{{ th.hero[2] }}</p><a class="btn" href="/catalog">Открыть каталог</a></div><div>{{ thx.scene }}</div><div class="fog"></div></section>
{% if categories %}<div class="orn" aria-hidden="true"><i></i>{{ thx.orn }}<i></i></div><div class="sec-h" style="margin-top:8px"><h2>Разделы</h2></div><div class="tiles">{% for c in categories %}<a class="tile" href="/catalog?category={{ c.id }}">{{ thx.tile }}<b>{{ c.name }}</b><span>{{ c.products|length }} шт.</span></a>{% endfor %}</div>{% endif %}
<div class="orn" aria-hidden="true"><i></i>{{ thx.orn }}<i></i></div><div class="sec-h" style="margin-top:8px"><h2>Новинки</h2><a href="/catalog">Весь каталог</a></div>
{% if products %}<div class="grid">{% for p in products %}{{ card(p) }}{% endfor %}</div>{% else %}<div class="empty">{{ thx.ill_empty }}<h2>{{ th.tags.empty }}</h2><p>Каталог скоро наполнится.</p></div>{% endif %}
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
{% else %}<div class="empty">{{ thx.ill_search }}<h2>{{ th.tags.search }}</h2><p>Измените запрос или выберите другую категорию.</p><a class="btn" href="/catalog">Сбросить фильтры</a></div>{% endif %}
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
{% else %}<div class="empty">{{ thx.ill_cart }}<h2>{{ th.tags.cart }}</h2><p>Добавьте товары из каталога.</p><a class="btn" href="/catalog">В каталог</a></div>{% endif %}</div>{% endblock %}'''

T['checkout.html'] = r'''{% extends 'base.html' %}{% from 'macros.html' import pay %}{% block body %}<div class="wrap"><h1 class="h1">Оформление предзаказа</h1>
<div class="two"><div><form class="box" method="post"><label class="f">Имя<input name="name" required autocomplete="name" placeholder="Как к вам обращаться"></label>
<label class="f">Телефон<input name="phone" required type="tel" autocomplete="tel" inputmode="tel" placeholder="+996 700 000 000"></label>
<label class="f">Комментарий <span class="hint">(необязательно)</span><textarea name="comment" placeholder="Например, удобное время звонка"></textarea></label>
<button class="btn blk">Отправить предзаказ</button></form>
{% if methods %}<h2 style="font-size:20px;margin:26px 0 12px">Реквизиты для оплаты</h2>{% for m in methods %}{{ pay(m) }}{% endfor %}<p class="hint">Реквизиты также будут на странице подтверждения.</p>{% endif %}</div>
<aside class="box sum"><h3 style="font-size:17px;margin-bottom:10px">Ваш заказ</h3>{% for p,q,sub in items %}<div class="ln"><span>{{ p.name|truncate(34) }} × {{ q }}</span><span>{% if sub>0 %}{{ sub|money }}{% else %}—{% endif %}</span></div>{% endfor %}<div class="tot"><span>Итого</span><b>{{ total|money }} сом</b></div></aside></div></div>{% endblock %}'''

T['order_done.html'] = r'''{% extends 'base.html' %}{% from 'macros.html' import pay %}{% block body %}<div class="wrap" style="max-width:760px"><div style="padding:36px 0 10px"><div class="ok-ic">{{ thx.ok }}</div>
<h1 style="font-size:32px">Предзаказ №{{ o.id }} принят</h1><p class="hint" style="font-size:16px;margin-top:8px">Мы свяжемся с вами по номеру {{ o.customer_phone }} и подтвердим заказ.</p></div>
<div class="box"><h3 style="font-size:17px;margin-bottom:8px">Состав</h3>{% for i in o.items %}<div class="ln" style="display:flex;justify-content:space-between;padding:4px 0"><span>{{ i.product.name if i.product else 'Товар' }} × {{ i.quantity }}</span><span>{{ (i.price*i.quantity)|money }}</span></div>{% endfor %}
<div class="tot" style="display:flex;justify-content:space-between;font-weight:700;margin-top:10px;padding-top:12px;border-top:1px solid var(--line)"><span>Итого</span><span>{{ o.total_price|money }} сом</span></div></div>
{% if methods %}<h2 style="font-size:20px;margin:26px 0 12px">Как оплатить</h2>{% for m in methods %}{{ pay(m) }}{% endfor %}{% endif %}
<p style="margin:22px 0"><a class="btn sec" href="/catalog">Вернуться в каталог</a></p></div>{% endblock %}'''

T['admin_base.html'] = r'''{% extends 'base.html' %}{% block sky %}{% endblock %}{% block deco %}{% endblock %}{% block yard %}{% endblock %}{% block body %}<div class="wrap">
<nav class="an">{% for k,l in [('dashboard','Обзор'),('products','Товары'),('orders','Заказы'),('debts','Долги'),('categories','Категории'),('payments','Оплата'),('theme','Оформление'),('contacts','Контакты')] %}<a class="{{ 'on' if active==k }}" href="/admin/{{ k }}">{{ l }}</a>{% endfor %}<a class="out" href="/admin/logout">Выйти</a></nav>
{% block content %}{% endblock %}</div>{% endblock %}'''

T['admin_login.html'] = r'''{% extends 'base.html' %}{% block body %}<div class="wrap" style="max-width:420px;padding-top:60px">{{ thx.login }}<form class="box" method="post"><h1 style="font-size:32px;margin-bottom:6px">Вход для владельца</h1><p class="hint" style="margin-bottom:16px">Введите пароль администратора.</p>
<label class="f">Пароль<input type="password" name="password" required autofocus autocomplete="current-password"></label><button class="btn blk">Войти</button></form></div>{% endblock %}'''

T['admin_dashboard.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<h1 class="h1">Обзор</h1>
{% if default_pw %}<div class="note">Пароль администратора стандартный. Задайте свой в переменной <b>ADMIN_PASSWORD</b> на сервере.</div>{% endif %}
{% if not methods %}<div class="note">Реквизиты для оплаты не добавлены. <a href="/admin/payments"><b>Добавить</b></a></div>{% endif %}
<div class="stats"><div class="box stat"><b>{{ pc }}</b><span>Товаров</span></div><div class="box stat"><b>{{ oc }}</b><span>Заказов</span></div><div class="box stat"><b>{{ nc }}</b><span>Новых</span></div><div class="box stat"><b>{{ revenue|money }}</b><span>Сумма заказов, сом</span></div><a class="box stat" href="/admin/debts"><b>{{ debt_total|money }}</b><span>Долги клиентов, сом</span></a></div>
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
<form method="post" action="/admin/orders/{{ o.id }}/to-debt" style="margin-top:12px" onsubmit="return confirm('Записать сумму заказа в долги клиента?')"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><button class="btn sec blk">Записать в долг</button></form>
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

T['error.html'] = r'''{% extends 'base.html' %}{% block body %}<div class="wrap err">{{ thx.ill_err }}<div class="code">{{ code }}</div><h1>{{ msg }}</h1><p>{{ sub }}</p><a class="btn" href="/">На главную</a></div>{% endblock %}'''

T['admin_theme.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<h1 class="h1">Оформление</h1>
<p class="hint" style="margin-bottom:14px">Выберите тему сайта: сезон или праздник. Изменения видят все посетители сразу. Кнопка «Предпросмотр» показывает тему только вам.</p>
<form class="box" method="post" action="/admin/theme/mode" style="margin-bottom:8px"><input type="hidden" name="_csrf" value="{{ csrf_token() }}">
<label class="ck"><input type="checkbox" name="auto" {{ 'checked' if auto }}> Менять тему автоматически по дате (сезоны и праздники)</label>
<p class="hint" style="margin:-6px 0 14px 28px">Сейчас по календарю подходит: <b>{{ auto_name }}</b>. Праздники с плавающей датой (Айт) и «Распродажа» включаются только вручную.</p>
<label class="ck"><input type="checkbox" name="fx" {{ 'checked' if fx_on }}> Анимации и падающие частицы (снег, листья, лепестки)</label>
<label class="f">Свои фразы для бегущей ленты <span class="hint">(каждая с новой строки; пусто — стандартные фразы темы)</span><textarea name="ticker" placeholder="Например: Скидка 10% до пятницы">{{ ticker_custom }}</textarea></label>
<button class="btn">Сохранить</button></form>
{% for g in groups %}<h2 style="font-size:calc(var(--k)*32px);margin:26px 0 12px">{{ g }}</h2><div class="tgrid">{% for t in by_group[g] %}
<div class="tcard {{ 'cur' if t.id==shown }}"><div class="sw"><i style="background:{{ t.vars.bg }}"></i><i style="background:{{ t.vars.sf }}"></i><i style="background:{{ t.vars.pri }}"></i><i style="background:{{ t.vars.acc }}"></i><i style="background:{{ t.vars.ink }}"></i></div>
<div class="bd"><h3>{{ t.name }}</h3><p class="hint">{{ t.desc }}</p>{% if t.id==shown %}<span class="tag ok" style="align-self:flex-start">Сейчас на сайте</span>{% endif %}
<div class="acts" style="margin-top:auto;padding-top:8px"><form method="post" action="/admin/theme/set"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><input type="hidden" name="id" value="{{ t.id }}"><button class="btn sm">{{ 'Выбрана' if t.id==chosen else 'Применить' }}</button></form><a class="btn sec sm" href="/admin/theme/preview/{{ t.id }}">Предпросмотр</a></div></div></div>{% endfor %}</div>{% endfor %}{% endblock %}'''

T['admin_debts.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<h1 class="h1">Долги</h1>
<div class="stats"><div class="box stat"><b>{{ total|money }}</b><span>Общий долг, сом</span></div><div class="box stat"><b>{{ n_debtors }}</b><span>Должников</span></div><div class="box stat"><b>{{ n_over }}</b><span>Просрочено</span></div></div>
<div class="two"><div>
<form style="margin-bottom:6px"><div class="search" style="max-width:none"><svg class="i"><use href="#i-search"/></svg><input name="q" value="{{ q }}" placeholder="Найти по имени или телефону" aria-label="Поиск"></div><input type="hidden" name="f" value="{{ f }}"></form>
<div class="chips"><a class="chip {{ 'on' if f=='debt' }}" href="/admin/debts?f=debt&q={{ q }}">Должны</a><a class="chip {{ 'on' if f=='over' }}" href="/admin/debts?f=over&q={{ q }}">Просрочены</a><a class="chip {{ 'on' if f=='paid' }}" href="/admin/debts?f=paid&q={{ q }}">Погашены</a><a class="chip {{ 'on' if f=='all' }}" href="/admin/debts?f=all&q={{ q }}">Все</a>
<a class="chip" href="/admin/debts/export.csv">Скачать CSV</a></div>
<div class="scroll"><table class="tbl"><thead><tr><th>Клиент</th><th>Долг</th><th>Срок</th><th></th></tr></thead><tbody>
{% for d in debtors %}{% set b=d.balance %}<tr><td><a href="/admin/debts/{{ d.id }}"><b>{{ d.name }}</b></a>{% if d.phone %}<div class="hint">{{ d.phone }}</div>{% endif %}</td>
<td><b>{{ b|money }}</b> сом</td><td>{% if b>0 and d.due %}{{ d.due.strftime('%d.%m.%Y') }}{% if d.overdue %} <span class="tag warn">просрочен</span>{% endif %}{% elif b<=0 %}<span class="tag ok">погашен</span>{% else %}—{% endif %}</td>
<td style="text-align:right"><a class="btn sec sm" href="/admin/debts/{{ d.id }}">Открыть</a></td></tr>
{% else %}<tr><td colspan="4" style="text-align:center;color:var(--mut);padding:30px">Записей нет</td></tr>{% endfor %}</tbody></table></div></div>
<form class="box" method="post" action="/admin/debts/add" id="new"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><h3 style="font-size:calc(var(--k)*26px);margin-bottom:14px;text-transform:none">Записать долг</h3>
<label class="f">Имя клиента<input name="name" required list="names" autocomplete="off" placeholder="Имя"></label><datalist id="names">{% for d in all_debtors %}<option value="{{ d.name }}">{% endfor %}</datalist>
<label class="f">Телефон<input name="phone" type="tel" placeholder="+996 700 000 000"></label>
<label class="f">Сумма, сом<input name="amount" required inputmode="decimal" placeholder="1500"></label>
<label class="f">За что <span class="hint">(необязательно)</span><input name="note" placeholder="Тетради, ручки"></label>
<label class="f">Вернуть до <span class="hint">(необязательно)</span><input name="due" type="date"></label>
<button class="btn blk">Записать</button><p class="hint" style="margin-top:10px">Если клиент с таким телефоном или именем уже есть, долг добавится к нему.</p></form></div>{% endblock %}'''

T['admin_debtor.html'] = r'''{% extends 'admin_base.html' %}{% block content %}<p class="crumbs"><a href="/admin/debts">← Все долги</a></p>
<div class="tools"><div><h1 class="h1" style="margin:8px 0 2px">{{ d.name }}</h1><div class="hint">{{ d.phone or 'телефон не указан' }}{% if d.note %} · {{ d.note }}{% endif %}</div></div>
<div class="acts">{% if d.phone %}<a class="btn sec sm" href="tel:{{ d.phone|tel }}">Позвонить</a><a class="btn sec sm" href="{{ wa }}" rel="noopener">Напомнить в WhatsApp</a>{% endif %}</div></div>
<div class="stats"><div class="box stat"><b>{{ bal|money }}</b><span>Сейчас должен, сом</span></div><div class="box stat"><b>{{ debt_sum|money }}</b><span>Всего в долг</span></div><div class="box stat"><b>{{ paid_sum|money }}</b><span>Уже вернул</span></div>
<div class="box stat"><b style="font-size:calc(var(--k)*28px)">{{ d.due.strftime('%d.%m.%Y') if d.due and bal>0 else '—' }}</b><span>Срок возврата{% if d.overdue %} · просрочен{% endif %}</span></div></div>
<div class="two eq"><form class="box" method="post" action="/admin/debts/{{ d.id }}/entry"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><input type="hidden" name="kind" value="debt"><h3 style="font-size:calc(var(--k)*24px);margin-bottom:12px;text-transform:none">Записать долг</h3>
<label class="f">Сумма, сом<input name="amount" required inputmode="decimal"></label><label class="f">За что<input name="note"></label><label class="f">Вернуть до<input name="due" type="date" value="{{ d.due.strftime('%Y-%m-%d') if d.due else '' }}"></label><label class="f">Дата записи <span class="hint">(пусто — сегодня)</span><input name="date" type="date"></label><button class="btn blk">Добавить долг</button></form>
<div><form class="box" method="post" action="/admin/debts/{{ d.id }}/entry"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><input type="hidden" name="kind" value="payment"><h3 style="font-size:calc(var(--k)*24px);margin-bottom:12px;text-transform:none">Принять оплату</h3>
<label class="f">Сумма, сом<input name="amount" required inputmode="decimal"></label><label class="f">Комментарий<input name="note" placeholder="Наличными, переводом"></label><label class="f">Дата <span class="hint">(пусто — сегодня)</span><input name="date" type="date"></label><button class="btn blk">Записать оплату</button></form>
{% if bal>0 %}<form method="post" action="/admin/debts/{{ d.id }}/settle" style="margin-top:12px" onsubmit="return confirm('Отметить долг полностью погашенным?')"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><button class="btn sec blk">Погасить полностью ({{ bal|money }} сом)</button></form>{% endif %}</div></div>
<h2 style="font-size:calc(var(--k)*30px);margin:28px 0 12px">История</h2>
<div class="scroll"><table class="tbl"><thead><tr><th>Дата</th><th>Операция</th><th>Сумма</th><th>Комментарий</th><th></th></tr></thead><tbody>
{% for e in entries %}<tr><td>{{ e.created_at.strftime('%d.%m.%Y') }}</td><td><span class="tag {{ 'warn' if e.kind=='debt' else 'ok' }}">{{ 'Долг' if e.kind=='debt' else 'Оплата' }}</span></td><td><b>{{ '+' if e.kind=='debt' else '−' }}{{ e.amount|money }}</b> сом</td><td>{{ e.note or '' }}{% if e.order_id %} <a href="/admin/orders/{{ e.order_id }}" class="hint">заказ №{{ e.order_id }}</a>{% endif %}</td>
<td style="text-align:right"><form method="post" action="/admin/debts/entry/{{ e.id }}/delete" onsubmit="return confirm('Удалить запись?')"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><button class="btn red sm">Удалить</button></form></td></tr>
{% else %}<tr><td colspan="5" style="text-align:center;color:var(--mut);padding:26px">Записей пока нет</td></tr>{% endfor %}</tbody></table></div>
<details class="box" style="margin-top:22px"><summary style="cursor:pointer;font-weight:600">Изменить данные клиента или удалить</summary>
<form method="post" action="/admin/debts/{{ d.id }}/edit" style="margin-top:14px"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><label class="f">Имя<input name="name" required value="{{ d.name }}"></label><label class="f">Телефон<input name="phone" value="{{ d.phone or '' }}"></label><label class="f">Заметка<textarea name="note">{{ d.note or '' }}</textarea></label><button class="btn">Сохранить</button></form>
<form method="post" action="/admin/debts/{{ d.id }}/delete" style="margin-top:12px" onsubmit="return confirm('Удалить клиента вместе со всей историей?')"><input type="hidden" name="_csrf" value="{{ csrf_token() }}"><button class="btn red">Удалить клиента</button></form></details>{% endblock %}'''
