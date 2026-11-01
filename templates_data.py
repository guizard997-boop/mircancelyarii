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
.hero{position:relative;display:grid;grid-template-columns:1.05fr 1fr;gap:32px;align-items:center;padding:56px 0 28px}main{overflow-x:clip}
.hero h1{font-size:clamp(46px,7vw,96px);text-shadow:0 0 34px rgba(255,255,255,.22)}.hero h1 em{font-style:italic;font-weight:600;color:var(--mut)}
.hero p{color:var(--mut);font-size:18px;max-width:460px;margin:22px 0 32px}
.scene{width:100%;height:auto;display:block;overflow:visible}.web{position:absolute;left:-8px;top:-8px;width:210px;opacity:.5;pointer-events:none}
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

body{background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='600'><circle cx='195' cy='137' r='0.6' fill='white' opacity='0.6'/><circle cx='223' cy='305' r='0.6' fill='white' opacity='0.4'/><circle cx='133' cy='18' r='1' fill='white' opacity='0.25'/><circle cx='90' cy='272' r='1.3' fill='white' opacity='0.6'/><circle cx='451' cy='146' r='1' fill='white' opacity='0.4'/><circle cx='243' cy='502' r='1.3' fill='white' opacity='0.6'/><circle cx='376' cy='444' r='1' fill='white' opacity='0.6'/><circle cx='124' cy='358' r='1' fill='white' opacity='0.6'/><circle cx='463' cy='571' r='0.8' fill='white' opacity='0.4'/><circle cx='458' cy='552' r='0.8' fill='white' opacity='0.4'/><circle cx='211' cy='187' r='1' fill='white' opacity='0.4'/><circle cx='384' cy='474' r='1' fill='white' opacity='0.6'/><circle cx='290' cy='409' r='0.8' fill='white' opacity='0.6'/><circle cx='506' cy='567' r='0.8' fill='white' opacity='0.6'/><circle cx='245' cy='203' r='1' fill='white' opacity='0.25'/><circle cx='79' cy='444' r='1.3' fill='white' opacity='0.4'/><circle cx='6' cy='438' r='0.6' fill='white' opacity='0.25'/><circle cx='149' cy='513' r='1.3' fill='white' opacity='0.6'/><circle cx='263' cy='167' r='1.3' fill='white' opacity='0.6'/><circle cx='261' cy='363' r='0.8' fill='white' opacity='0.6'/><circle cx='387' cy='536' r='0.8' fill='white' opacity='0.6'/><circle cx='247' cy='512' r='0.8' fill='white' opacity='0.6'/><circle cx='47' cy='43' r='1' fill='white' opacity='0.6'/><circle cx='587' cy='353' r='0.8' fill='white' opacity='0.4'/><circle cx='201' cy='172' r='0.6' fill='white' opacity='0.25'/><circle cx='175' cy='74' r='1.3' fill='white' opacity='0.6'/><circle cx='573' cy='560' r='0.6' fill='white' opacity='0.4'/><circle cx='355' cy='98' r='0.6' fill='white' opacity='0.25'/><circle cx='322' cy='128' r='1.3' fill='white' opacity='0.4'/><circle cx='279' cy='582' r='0.6' fill='white' opacity='0.4'/><circle cx='538' cy='379' r='0.6' fill='white' opacity='0.25'/><circle cx='331' cy='346' r='0.8' fill='white' opacity='0.4'/><circle cx='577' cy='549' r='1.3' fill='white' opacity='0.25'/><circle cx='216' cy='307' r='0.6' fill='white' opacity='0.4'/><circle cx='517' cy='164' r='0.8' fill='white' opacity='0.4'/><circle cx='439' cy='224' r='1' fill='white' opacity='0.4'/><circle cx='245' cy='368' r='0.8' fill='white' opacity='0.6'/><circle cx='298' cy='442' r='0.8' fill='white' opacity='0.6'/><circle cx='363' cy='439' r='0.6' fill='white' opacity='0.4'/><circle cx='411' cy='475' r='0.6' fill='white' opacity='0.25'/><circle cx='50' cy='8' r='1' fill='white' opacity='0.25'/><circle cx='464' cy='496' r='1.3' fill='white' opacity='0.4'/><circle cx='66' cy='300' r='1.3' fill='white' opacity='0.25'/><circle cx='155' cy='57' r='0.6' fill='white' opacity='0.4'/><circle cx='164' cy='227' r='1' fill='white' opacity='0.4'/><circle cx='401' cy='301' r='0.6' fill='white' opacity='0.4'/><circle cx='135' cy='106' r='1' fill='white' opacity='0.4'/><circle cx='456' cy='448' r='0.6' fill='white' opacity='0.4'/><circle cx='551' cy='306' r='0.8' fill='white' opacity='0.25'/><circle cx='334' cy='174' r='0.8' fill='white' opacity='0.25'/><circle cx='258' cy='157' r='0.6' fill='white' opacity='0.4'/><circle cx='384' cy='76' r='1' fill='white' opacity='0.4'/><circle cx='222' cy='52' r='0.8' fill='white' opacity='0.6'/><circle cx='248' cy='536' r='1.3' fill='white' opacity='0.25'/><circle cx='591' cy='406' r='0.6' fill='white' opacity='0.6'/></svg>"),radial-gradient(1200px 600px at 50% -10%,#1d1d1d 0,transparent 70%) var(--bg);background-attachment:fixed}
.sky{position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:35}
.fb{position:absolute;left:0;width:44px;height:22px;opacity:.8;animation:fly 28s linear infinite}
.fb.b1{top:16%}.fb.b2{top:38%;width:30px;height:15px;animation-duration:38s;animation-delay:-14s;opacity:.55}.fb.b3{top:62%;width:52px;height:26px;animation-duration:46s;animation-delay:-30s;opacity:.65}
@keyframes fly{0%{transform:translate(-12vw,0)}25%{transform:translate(24vw,-34px)}50%{transform:translate(54vw,22px)}75%{transform:translate(84vw,-28px)}100%{transform:translate(116vw,8px)}}
.ticker{overflow:hidden;background:var(--ink);color:var(--bg);position:relative;z-index:31}
.tk{display:flex;width:max-content;animation:tk 46s linear infinite}.tkg{display:flex;align-items:center;gap:30px;padding:9px 30px 9px 0}
.tkg span{font:600 11px Inter,sans-serif;letter-spacing:.2em;text-transform:uppercase;white-space:nowrap}.tkg svg{width:15px;height:15px;fill:currentColor;stroke:none;flex:none}
@keyframes tk{to{transform:translateX(-50%)}}
.deco{position:relative;height:0;z-index:30;pointer-events:none}
.drips{position:absolute;left:0;right:0;top:-1px;height:50px;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='488' height='50' viewBox='0 0 488 50'><path fill='%23F4F4F4' d='M6 0H15V16A4.5 4.5 0 0 1 6 16ZM44 0H53V34A4.5 4.5 0 0 1 44 34ZM82 0H91V20A4.5 4.5 0 0 1 82 20ZM128 0H137V44A4.5 4.5 0 0 1 128 44ZM174 0H183V14A4.5 4.5 0 0 1 174 14ZM204 0H213V28A4.5 4.5 0 0 1 204 28ZM250 0H259V38A4.5 4.5 0 0 1 250 38ZM280 0H289V18A4.5 4.5 0 0 1 280 18ZM326 0H335V30A4.5 4.5 0 0 1 326 30ZM356 0H365V12A4.5 4.5 0 0 1 356 12ZM386 0H395V40A4.5 4.5 0 0 1 386 40ZM432 0H441V22A4.5 4.5 0 0 1 432 22Z'/></svg>") repeat-x}
.dang{position:absolute;top:0;pointer-events:auto;cursor:pointer;transform-origin:top center;animation:sw 4.5s ease-in-out infinite;display:flex;flex-direction:column;align-items:center}
.dang .th{display:block;width:1px;background:#8a8a8a}.dang svg{width:38px;height:38px;display:block}
@keyframes sw{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}
[data-boo]{cursor:pointer}
.orn{display:flex;align-items:center;gap:16px;margin:34px 0 6px;color:var(--mut)}.orn i{flex:1;height:1px;background:linear-gradient(90deg,transparent,#555,transparent)}.orn svg{width:26px;height:26px;fill:currentColor;stroke:none}
.tombs{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:16px;margin:6px 0 10px}
.tomb{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;padding:34px 14px 20px;border:1px solid var(--line);border-radius:90px 90px 0 0;background:linear-gradient(#171717,#0a0a0a);transition:background .2s,color .2s,transform .2s}
.tomb svg{width:22px;height:22px;color:var(--mut)}.tomb b{font:700 22px/1.1 Cormorant,Georgia,serif}.tomb span{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
@media(hover:hover){.tomb:hover{background:var(--ink);color:var(--bg);transform:translateY(-4px)}.tomb:hover svg,.tomb:hover span{color:var(--bg)}}
.pc .im{position:relative}.pc .im::after{content:"";position:absolute;right:0;top:0;width:70px;height:70px;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200' fill='none' stroke='white' stroke-width='1.2'><path d='M0 0L200.0 0.0M0 0L184.8 76.5M0 0L141.4 141.4M0 0L76.5 184.8M0 0L0.0 200.0M40.0 0.0Q33.7 6.7 37.0 15.3M37.0 15.3Q28.6 19.1 28.3 28.3M28.3 28.3Q19.1 28.6 15.3 37.0M15.3 37.0Q6.7 33.7 0.0 40.0M80.0 0.0Q67.5 13.4 73.9 30.6M73.9 30.6Q57.2 38.2 56.6 56.6M56.6 56.6Q38.2 57.2 30.6 73.9M30.6 73.9Q13.4 67.5 0.0 80.0M120.0 0.0Q101.2 20.1 110.9 45.9M110.9 45.9Q85.8 57.3 84.9 84.9M84.9 84.9Q57.3 85.8 45.9 110.9M45.9 110.9Q20.1 101.2 0.0 120.0M160.0 0.0Q135.0 26.8 147.8 61.2M147.8 61.2Q114.4 76.4 113.1 113.1M113.1 113.1Q76.4 114.4 61.2 147.8M61.2 147.8Q26.8 135.0 0.0 160.0M200.0 0.0Q168.7 33.6 184.8 76.5M184.8 76.5Q143.0 95.6 141.4 141.4M141.4 141.4Q95.6 143.0 76.5 184.8M76.5 184.8Q33.6 168.7 0.0 200.0'/></svg>") no-repeat 0 0/contain;transform:scaleX(-1);opacity:.5;pointer-events:none}
.floaty{transform-box:fill-box;transform-origin:center;animation:flo 5s ease-in-out infinite}@keyframes flo{50%{transform:translateY(-12px) rotate(3deg)}}
.fl{transform-box:fill-box;transform-origin:50% 100%;animation:fl .16s ease-in-out infinite alternate}@keyframes fl{to{transform:scale(.88,1.1)}}
.hero h1 em{animation:glow 5s infinite}@keyframes glow{0%,90%,100%{opacity:1}93%{opacity:.55}96%{opacity:.9}}
.yard{position:relative;height:130px;margin-top:70px;background:linear-gradient(to top,rgba(255,255,255,.09),transparent 80%);pointer-events:none}
.yard svg.bg{position:absolute;inset:0;width:100%;height:100%;display:block}.yard *{pointer-events:auto}
.eyes{position:absolute;width:34px;height:12px;animation:blink 6s infinite;transform-box:fill-box;transform-origin:center}
@keyframes blink{0%,94%,100%{transform:scaleY(1)}97%{transform:scaleY(.08)}}
.ft{margin-top:0}.ft::before{display:none}
.ill{width:96px;height:auto;margin:0 auto 14px;display:block;fill:var(--ink);stroke:none}
.candles{display:flex;justify-content:center;align-items:flex-end;gap:14px;margin-bottom:18px}.candles .c{position:relative;width:26px}.candles svg{width:100%;display:block;fill:#e9e9e9;stroke:none}.candles .f{position:absolute;left:0;top:-22px;width:26px;height:26px;fill:#fff;filter:drop-shadow(0 0 8px #fff)}
.ok-ic{width:72px;height:72px}.ok-ic svg{width:44px;height:44px;fill:var(--ink);stroke:none}
.err{text-align:center;padding:70px 0 20px}.err .code{font:700 clamp(90px,18vw,180px)/1 Cormorant,Georgia,serif;text-shadow:0 0 40px rgba(255,255,255,.3)}.err h1{font-size:38px;margin:6px 0 10px}.err p{color:var(--mut);margin-bottom:24px}
@media(max-width:600px){.dang.d2{display:none}.tomb{padding:26px 10px 16px}.yard{height:96px;margin-top:50px}}
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
var boo=['Бу!','Тсс, они слушают','Не бойтесь, он декоративный','С Хэллоуином','Свечи не тушить'];
document.addEventListener('click',function(e){if(e.target.closest('[data-boo]')){toast(boo[Math.floor(Math.random()*boo.length)])}});
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
<symbol id="i-cross" viewBox="0 0 24 24"><path d="M12 3v18M6 9h12"/></symbol>
<symbol id="i-pumpkin" viewBox="0 0 100 90"><path fill-rule="evenodd" d="M50 16C38 8 20 10 12 28C4 46 10 74 34 82C42 85 58 85 66 82C90 74 96 46 88 28C80 10 62 8 50 16Z M28 36L40 36L34 48Z M60 36L72 36L66 48Z M46 52L54 52L50 60Z M26 62L34 66L40 60L46 68L54 68L60 60L66 66L74 62C70 76 60 80 50 80C40 80 30 76 26 62Z"/><path d="M45 16C45 8 50 3 58 1L61 6C57 8 55 12 55 17Z"/><path fill="none" stroke="#050505" stroke-width="2" opacity=".55" d="M38 12C26 34 28 64 40 83M62 12C74 34 72 64 60 83"/></symbol>
<symbol id="i-skull" viewBox="0 0 64 72"><path fill-rule="evenodd" d="M32 2C16 2 6 14 6 28C6 38 11 44 16 48L16 60L24 60L24 66L28 66L28 60L36 60L36 66L40 66L40 60L48 60L48 48C53 44 58 38 58 28C58 14 48 2 32 2Z M13 28A9 10 0 1 0 31 28A9 10 0 1 0 13 28Z M33 28A9 10 0 1 0 51 28A9 10 0 1 0 33 28Z M32 38L27 48L37 48Z"/><path fill="none" stroke="#050505" stroke-width="2" d="M24 52V60M32 52V60M40 52V60"/></symbol>
<symbol id="i-ghost" viewBox="0 0 64 80"><path fill-rule="evenodd" d="M32 4C16 4 8 16 8 32L8 74L16 66L24 74L32 66L40 74L48 66L56 74L56 32C56 16 48 4 32 4Z M20 30A5 7 0 1 0 30 30A5 7 0 1 0 20 30Z M34 30A5 7 0 1 0 44 30A5 7 0 1 0 34 30Z M27 46A5 6 0 1 0 37 46A5 6 0 1 0 27 46Z"/></symbol>
<symbol id="i-spider" viewBox="0 0 60 60"><path d="M30 26A10 12 0 1 0 30 50A10 12 0 1 0 30 26Z M30 18A6 6 0 1 0 30 30A6 6 0 1 0 30 18Z"/><path fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M22 34L8 24L2 32M21 38L4 40L2 50M22 43L8 52L6 58M24 30L14 16L8 14M38 34L52 24L58 32M39 38L56 40L58 50M38 43L52 52L54 58M36 30L46 16L52 14"/></symbol>
<symbol id="i-tomb" viewBox="0 0 48 64"><path fill-rule="evenodd" d="M4 64V22C4 10 12 2 24 2C36 2 44 10 44 22V64Z M22 14H26V22H34V27H26V46H22V27H14V22H22Z"/></symbol>
<symbol id="i-tree" viewBox="0 0 120 140"><path fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="7" d="M60 140C58 112 62 92 60 70"/><path fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M60 104C48 94 36 86 22 72M60 92C74 82 88 78 104 64M60 70C54 56 44 46 36 28M60 70C66 54 76 44 84 24M22 72L10 68M22 72L16 56M104 64L114 66M104 64L108 50M36 28L28 22M36 28L40 14M84 24L92 18M84 24L82 10M48 82L38 86"/></symbol>
<symbol id="i-candle" viewBox="0 0 30 72"><path d="M8 30H22V70H8Z M22 36C27 36 27 46 22 46Z"/></symbol>
<symbol id="i-flame" viewBox="0 0 30 30"><path d="M15 2C10 10 8 15 12 21C14 24 16 24 18 21C22 15 20 10 15 2Z"/></symbol>
<symbol id="i-eyes" viewBox="0 0 40 14"><path fill-rule="evenodd" d="M2 7C8 0 14 0 18 7C14 14 8 14 2 7Z M7 7A2.5 5 0 1 0 12 7A2.5 5 0 1 0 7 7Z M22 7C26 0 32 0 38 7C32 14 26 14 22 7Z M28 7A2.5 5 0 1 0 33 7A2.5 5 0 1 0 28 7Z"/></symbol>
<symbol id="i-cauldron" viewBox="0 0 80 66"><path d="M8 20C5 24 4 30 4 38C4 54 18 62 40 62C62 62 76 54 76 38C76 30 75 24 72 20Z M18 58L12 66H24Z M62 58L56 66H68Z"/><path d="M6 16A34 7 0 1 0 74 16A34 7 0 1 0 6 16Z"/><path fill="#050505" d="M12 16A28 4 0 1 0 68 16A28 4 0 1 0 12 16Z"/><circle cx="28" cy="10" r="4" fill="#F4F4F4"/><circle cx="44" cy="5" r="5" fill="#F4F4F4"/><circle cx="56" cy="11" r="3" fill="#F4F4F4"/></symbol>
</svg>'''

T = {}

T['base.html'] = r'''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#050505"><link rel="icon" href="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='-8 -8 116 106'><rect x='-8' y='-8' width='116' height='106' fill='black'/><path fill='white' fill-rule='evenodd' d='M50 16C38 8 20 10 12 28C4 46 10 74 34 82C42 85 58 85 66 82C90 74 96 46 88 28C80 10 62 8 50 16Z M28 36L40 36L34 48Z M60 36L72 36L66 48Z M46 52L54 52L50 60Z M26 62L34 66L40 60L46 68L54 68L60 60L66 66L74 62C70 76 60 80 50 80C40 80 30 76 26 62Z'/></svg>">
<title>{{ title }} — Мир канцелярии</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,600;0,700;1,600&family=Inter:wght@400;500;600&display=swap&subset=cyrillic" rel="stylesheet">
<style>{% raw %}''' + CSS + r'''{% endraw %}</style></head><body>
''' + SPRITE + r'''
{% block sky %}<div class="sky" aria-hidden="true"><svg class="fb b1" viewBox="0 0 64 32"><use class="bat" href="#i-bat" fill="#F4F4F4"/></svg><svg class="fb b2" viewBox="0 0 64 32"><use class="bat" href="#i-bat" fill="#F4F4F4"/></svg><svg class="fb b3" viewBox="0 0 64 32"><use class="bat" href="#i-bat" fill="#F4F4F4"/></svg></div>{% endblock %}
<header class="hdr"><div class="wrap">
<a class="logo" href="/" aria-label="Мир канцелярии"><b><svg class="i"><use href="#i-moon"/></svg></b><span>Мир канцелярии</span></a>
<form class="search" action="/catalog" role="search"><svg class="i"><use href="#i-search"/></svg><input id="q" type="search" name="q" value="{{ request.args.get('q','') }}" placeholder="Поиск по каталогу" autocomplete="off" aria-label="Поиск"></form>
<a class="ibtn cart-h" href="/cart" aria-label="Корзина"><svg class="i"><use href="#i-bag"/></svg><span class="badge" data-badge {% if not cart_count %}hidden{% endif %}>{{ cart_count }}</span></a>
</div></header>
{% block deco %}<div class="ticker" aria-hidden="true"><div class="tk"><div class="tkg"><span>Ручки, которые не боятся темноты</span><svg viewBox="0 0 100 90"><use href="#i-pumpkin"/></svg><span>Тетради с секретами</span><svg viewBox="0 0 64 72"><use href="#i-skull"/></svg><span>Краски для ночных кошмаров</span><svg viewBox="0 0 100 90"><use href="#i-pumpkin"/></svg><span>Предзаказ до первых петухов</span><svg viewBox="0 0 64 72"><use href="#i-skull"/></svg><span>Пишите осторожно</span><svg viewBox="0 0 100 90"><use href="#i-pumpkin"/></svg></div><div class="tkg"><span>Ручки, которые не боятся темноты</span><svg viewBox="0 0 100 90"><use href="#i-pumpkin"/></svg><span>Тетради с секретами</span><svg viewBox="0 0 64 72"><use href="#i-skull"/></svg><span>Краски для ночных кошмаров</span><svg viewBox="0 0 100 90"><use href="#i-pumpkin"/></svg><span>Предзаказ до первых петухов</span><svg viewBox="0 0 64 72"><use href="#i-skull"/></svg><span>Пишите осторожно</span><svg viewBox="0 0 100 90"><use href="#i-pumpkin"/></svg></div></div></div>
<div class="deco"><div class="drips"></div>
<div class="dang" data-boo style="right:8%"><i class="th" style="height:80px"></i><svg viewBox="0 0 60 60"><use href="#i-spider" fill="#F4F4F4" stroke="#F4F4F4"/></svg></div>
<div class="dang d2" data-boo style="right:27%;animation-delay:-2s"><i class="th" style="height:46px"></i><svg viewBox="0 0 60 60" style="width:28px;height:28px"><use href="#i-spider" fill="#F4F4F4" stroke="#F4F4F4"/></svg></div></div>{% endblock %}
{% with m=get_flashed_messages(with_categories=true) %}{% if m %}<div id="flash" hidden>{% for c,t in m %}<i data-c="{{ c }}">{{ t }}</i>{% endfor %}</div>{% endif %}{% endwith %}
<main>{% block body %}{% endblock %}</main>
{% block yard %}<div class="yard" aria-hidden="true"><svg class="bg" viewBox="0 0 1200 130" preserveAspectRatio="xMidYMax slice">
<use href="#i-tree" x="150" y="2" width="120" height="140" stroke="#0D0D0D" fill="none"/><use href="#i-tree" x="860" y="14" width="96" height="112" stroke="#0D0D0D" fill="none"/>
<use href="#i-tomb" x="40" y="62" width="40" height="53" fill="#0D0D0D" stroke="#3a3a3a" stroke-width="1.5"/><use href="#i-tomb" x="380" y="58" width="46" height="61" fill="#0D0D0D" stroke="#3a3a3a" stroke-width="1.5"/>
<use href="#i-tomb" x="520" y="76" width="32" height="42" fill="#0D0D0D" stroke="#3a3a3a" stroke-width="1.5"/><use href="#i-tomb" x="740" y="64" width="42" height="56" fill="#0D0D0D" stroke="#3a3a3a" stroke-width="1.5"/>
<use href="#i-tomb" x="1050" y="60" width="44" height="58" fill="#0D0D0D" stroke="#3a3a3a" stroke-width="1.5"/>
<path d="M0 130V100Q150 80 300 98T600 96T900 100T1200 92V130Z" fill="#0D0D0D" stroke="#3a3a3a" stroke-width="1.2"/>
<use href="#i-pumpkin" x="300" y="82" width="56" height="50" fill="#F4F4F4"/><use href="#i-pumpkin" x="640" y="92" width="38" height="34" fill="#F4F4F4"/><use href="#i-pumpkin" x="970" y="80" width="64" height="58" fill="#F4F4F4"/>
<use class="floaty" data-boo href="#i-ghost" x="1130" y="14" width="38" height="48" fill="#F4F4F4" opacity=".9"/>
<use class="bat" href="#i-bat" x="460" y="14" width="46" height="23" fill="#F4F4F4"/><use class="bat" href="#i-bat" x="570" y="30" width="30" height="15" fill="#F4F4F4" style="animation-delay:-.2s"/>
</svg>
<svg class="eyes" style="left:14%;bottom:62px" viewBox="0 0 40 14"><use href="#i-eyes" fill="#F4F4F4"/></svg><svg class="eyes" style="left:76%;bottom:58px;animation-delay:-3s" viewBox="0 0 40 14"><use href="#i-eyes" fill="#F4F4F4"/></svg></div>{% endblock %}
<footer class="ft"><div class="wrap">
<div><div class="logo"><b><svg class="i"><use href="#i-moon"/></svg></b><span>Мир канцелярии</span></div></div>
<div><h4>Каталог</h4>{% for c in categories[:8] %}<a href="/catalog?category={{ c.id }}">{{ c.name }}</a>{% endfor %}<a href="/catalog">Все товары</a></div>
<div><h4>Связаться</h4>{% for p in phones %}<a href="tel:{{ p|tel }}">{{ p }}</a>{% endfor %}{% if whatsapp %}<a href="https://wa.me/{{ whatsapp|tel|replace('+','') }}" rel="noopener">WhatsApp</a>{% endif %}{% if not phones and not whatsapp %}<a href="/cart">Оформить предзаказ</a>{% endif %}</div>
</div><div class="wrap copy">© 2026 Мир канцелярии &nbsp;·&nbsp; Пишите осторожно</div></footer>
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
<section class="hero"><svg class="web" viewBox="0 0 200 200" fill="none" stroke="#fff" stroke-width="1" aria-hidden="true"><path d="M0 0L200.0 0.0M0 0L184.8 76.5M0 0L141.4 141.4M0 0L76.5 184.8M0 0L0.0 200.0M40.0 0.0Q33.7 6.7 37.0 15.3M37.0 15.3Q28.6 19.1 28.3 28.3M28.3 28.3Q19.1 28.6 15.3 37.0M15.3 37.0Q6.7 33.7 0.0 40.0M80.0 0.0Q67.5 13.4 73.9 30.6M73.9 30.6Q57.2 38.2 56.6 56.6M56.6 56.6Q38.2 57.2 30.6 73.9M30.6 73.9Q13.4 67.5 0.0 80.0M120.0 0.0Q101.2 20.1 110.9 45.9M110.9 45.9Q85.8 57.3 84.9 84.9M84.9 84.9Q57.3 85.8 45.9 110.9M45.9 110.9Q20.1 101.2 0.0 120.0M160.0 0.0Q135.0 26.8 147.8 61.2M147.8 61.2Q114.4 76.4 113.1 113.1M113.1 113.1Q76.4 114.4 61.2 147.8M61.2 147.8Q26.8 135.0 0.0 160.0M200.0 0.0Q168.7 33.6 184.8 76.5M184.8 76.5Q143.0 95.6 141.4 141.4M141.4 141.4Q95.6 143.0 76.5 184.8M76.5 184.8Q33.6 168.7 0.0 200.0"/></svg><div style="position:relative"><h1>Канцелярия для <em>долгих ночей</em></h1><p>Ручки, тетради, краски и всё для тех, кто пишет, рисует и учится допоздна. Выберите нужное и оставьте предзаказ.</p><a class="btn" href="/catalog">Открыть каталог</a></div><div><svg class="scene" viewBox="0 0 520 460" role="img" aria-label="Луна, летучие мыши, привидение и тыквы"><defs><radialGradient id="mg" cx="38%" cy="32%" r="78%"><stop offset="0" stop-color="#FAFAFA"/><stop offset="1" stop-color="#8E8E8E"/></radialGradient><radialGradient id="gl"><stop offset="0" stop-color="#fff" stop-opacity=".3"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient><linearGradient id="gv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d1d1d"/><stop offset="1" stop-color="#050505" stop-opacity="0"/></linearGradient><linearGradient id="gh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/><stop offset=".14" stop-color="#fff"/><stop offset=".86" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient><mask id="gm"><rect x="0" y="350" width="520" height="110" fill="url(#gh)"/></mask></defs>
<circle cx="300" cy="205" r="215" fill="url(#gl)"/><circle cx="300" cy="205" r="150" fill="url(#mg)"/><g fill="#000" opacity=".16"><circle cx="250" cy="150" r="24"/><circle cx="350" cy="235" r="32"/><circle cx="285" cy="285" r="15"/><circle cx="375" cy="150" r="13"/><circle cx="225" cy="235" r="11"/></g>
<use href="#i-tree" x="305" y="185" width="200" height="233" stroke="#050505" fill="none"/>
<use href="#i-tomb" x="205" y="352" width="48" height="64" fill="#050505" stroke="#555" stroke-width="2"/><use href="#i-tomb" x="120" y="368" width="34" height="45" fill="#050505" stroke="#555" stroke-width="2"/><use href="#i-tomb" x="455" y="368" width="36" height="48" fill="#050505" stroke="#555" stroke-width="2"/>
<g mask="url(#gm)"><path d="M0 412Q120 388 250 406T520 396V460H0Z" fill="url(#gv)" stroke="#555" stroke-width="1.5"/></g>
<use href="#i-pumpkin" x="30" y="352" width="104" height="94" fill="#F4F4F4" data-boo/><use href="#i-pumpkin" x="150" y="396" width="58" height="52" fill="#F4F4F4" data-boo/><use href="#i-pumpkin" x="390" y="398" width="68" height="62" fill="#F4F4F4" data-boo/>
<use class="floaty" data-boo href="#i-ghost" x="55" y="62" width="88" height="110" fill="#F4F4F4" opacity=".92"/>
<use class="bat" href="#i-bat" x="205" y="150" width="150" height="75" fill="#050505"/><use class="bat" href="#i-bat" x="338" y="82" width="72" height="36" fill="#050505" style="animation-delay:-.2s"/>
<use class="bat" href="#i-bat" x="170" y="40" width="80" height="40" fill="#F4F4F4" style="animation-delay:-.1s"/><use class="bat" href="#i-bat" x="430" y="20" width="64" height="32" fill="#F4F4F4" style="animation-delay:-.3s"/><use class="bat" href="#i-bat" x="20" y="250" width="56" height="28" fill="#F4F4F4" style="animation-delay:-.25s"/><use class="bat" href="#i-bat" x="440" y="300" width="70" height="35" fill="#F4F4F4"/></svg></div><div class="fog"></div></section>
{% if categories %}<div class="orn" aria-hidden="true"><i></i><svg viewBox="0 0 64 72"><use href="#i-skull"/></svg><i></i></div><div class="sec-h" style="margin-top:8px"><h2>Разделы</h2></div><div class="tombs">{% for c in categories %}<a class="tomb" href="/catalog?category={{ c.id }}"><svg class="i"><use href="#i-cross"/></svg><b>{{ c.name }}</b><span>{{ c.products|length }} шт.</span></a>{% endfor %}</div>{% endif %}
<div class="orn" aria-hidden="true"><i></i><svg viewBox="0 0 64 72"><use href="#i-skull"/></svg><i></i></div><div class="sec-h" style="margin-top:8px"><h2>Новинки</h2><a href="/catalog">Весь каталог</a></div>
{% if products %}<div class="grid">{% for p in products %}{{ card(p) }}{% endfor %}</div>{% else %}<div class="empty"><svg class="ill" viewBox="0 0 64 72"><use href="#i-skull"/></svg><h2>Здесь пока пусто</h2><p>Каталог скоро наполнится.</p></div>{% endif %}
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
{% else %}<div class="empty"><svg class="ill" viewBox="0 0 64 80"><use href="#i-ghost"/></svg><h2>Ничего не найдено</h2><p>Измените запрос или выберите другую категорию.</p><a class="btn" href="/catalog">Сбросить фильтры</a></div>{% endif %}
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
{% else %}<div class="empty"><svg class="ill" viewBox="0 0 80 66"><use href="#i-cauldron"/></svg><h2>В котле пусто</h2><p>Добавьте товары из каталога.</p><a class="btn" href="/catalog">В каталог</a></div>{% endif %}</div>{% endblock %}'''

T['checkout.html'] = r'''{% extends 'base.html' %}{% from 'macros.html' import pay %}{% block body %}<div class="wrap"><h1 class="h1">Оформление предзаказа</h1>
<div class="two"><div><form class="box" method="post"><label class="f">Имя<input name="name" required autocomplete="name" placeholder="Как к вам обращаться"></label>
<label class="f">Телефон<input name="phone" required type="tel" autocomplete="tel" inputmode="tel" placeholder="+996 700 000 000"></label>
<label class="f">Комментарий <span class="hint">(необязательно)</span><textarea name="comment" placeholder="Например, удобное время звонка"></textarea></label>
<button class="btn blk">Отправить предзаказ</button></form>
{% if methods %}<h2 style="font-size:20px;margin:26px 0 12px">Реквизиты для оплаты</h2>{% for m in methods %}{{ pay(m) }}{% endfor %}<p class="hint">Реквизиты также будут на странице подтверждения.</p>{% endif %}</div>
<aside class="box sum"><h3 style="font-size:17px;margin-bottom:10px">Ваш заказ</h3>{% for p,q,sub in items %}<div class="ln"><span>{{ p.name|truncate(34) }} × {{ q }}</span><span>{% if sub>0 %}{{ sub|money }}{% else %}—{% endif %}</span></div>{% endfor %}<div class="tot"><span>Итого</span><b>{{ total|money }} сом</b></div></aside></div></div>{% endblock %}'''

T['order_done.html'] = r'''{% extends 'base.html' %}{% from 'macros.html' import pay %}{% block body %}<div class="wrap" style="max-width:760px"><div style="padding:36px 0 10px"><div class="ok-ic"><svg viewBox="0 0 100 90"><use href="#i-pumpkin"/></svg></div>
<h1 style="font-size:32px">Предзаказ №{{ o.id }} принят</h1><p class="hint" style="font-size:16px;margin-top:8px">Мы свяжемся с вами по номеру {{ o.customer_phone }} и подтвердим заказ.</p></div>
<div class="box"><h3 style="font-size:17px;margin-bottom:8px">Состав</h3>{% for i in o.items %}<div class="ln" style="display:flex;justify-content:space-between;padding:4px 0"><span>{{ i.product.name if i.product else 'Товар' }} × {{ i.quantity }}</span><span>{{ (i.price*i.quantity)|money }}</span></div>{% endfor %}
<div class="tot" style="display:flex;justify-content:space-between;font-weight:700;margin-top:10px;padding-top:12px;border-top:1px solid var(--line)"><span>Итого</span><span>{{ o.total_price|money }} сом</span></div></div>
{% if methods %}<h2 style="font-size:20px;margin:26px 0 12px">Как оплатить</h2>{% for m in methods %}{{ pay(m) }}{% endfor %}{% endif %}
<p style="margin:22px 0"><a class="btn sec" href="/catalog">Вернуться в каталог</a></p></div>{% endblock %}'''

# ---------------- админка ----------------
T['admin_base.html'] = r'''{% extends 'base.html' %}{% block sky %}{% endblock %}{% block deco %}{% endblock %}{% block yard %}{% endblock %}{% block body %}<div class="wrap">
<nav class="an">{% for k,l in [('dashboard','Обзор'),('products','Товары'),('orders','Заказы'),('categories','Категории'),('payments','Оплата'),('contacts','Контакты')] %}<a class="{{ 'on' if active==k }}" href="/admin/{{ k }}">{{ l }}</a>{% endfor %}<a class="out" href="/admin/logout">Выйти</a></nav>
{% block content %}{% endblock %}</div>{% endblock %}'''

T['admin_login.html'] = r'''{% extends 'base.html' %}{% block body %}<div class="wrap" style="max-width:420px;padding-top:60px"><div class="candles" aria-hidden="true"><div class="c" style="width:22px"><svg class="f fl" viewBox="0 0 30 30" style="top:-18px;width:22px;height:22px;animation-delay:-0.05s"><use href="#i-flame"/></svg><svg viewBox="0 0 30 72" style="height:70px"><use href="#i-candle"/></svg></div><div class="c" style="width:28px"><svg class="f fl" viewBox="0 0 30 30" style="top:-24px;width:28px;height:28px;animation-delay:-0.1s"><use href="#i-flame"/></svg><svg viewBox="0 0 30 72" style="height:110px"><use href="#i-candle"/></svg></div><div class="c" style="width:20px"><svg class="f fl" viewBox="0 0 30 30" style="top:-16px;width:20px;height:20px;animation-delay:-0.08s"><use href="#i-flame"/></svg><svg viewBox="0 0 30 72" style="height:56px"><use href="#i-candle"/></svg></div></div><form class="box" method="post"><h1 style="font-size:32px;margin-bottom:6px">Вход для владельца</h1><p class="hint" style="margin-bottom:16px">Введите пароль администратора.</p>
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

T['error.html'] = r'''{% extends 'base.html' %}{% block body %}<div class="wrap err"><svg class="ill" style="width:120px" viewBox="0 0 64 72"><use href="#i-skull"/></svg><div class="code">{{ code }}</div><h1>{{ msg }}</h1><p>{{ sub }}</p><a class="btn" href="/">На главную</a></div>{% endblock %}'''
