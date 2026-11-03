# -*- coding: utf-8 -*-
"""Темы оформления: сезоны и праздники. Меняются из админки (Оформление).

Тема = палитра + шрифты + иллюстрации (SVG) + частицы (снег, лепестки…) + тексты.
Чтобы добавить свою тему, скопируйте любой блок T(...) внизу файла и поменяйте цвета и тексты.
"""
import datetime
import math
import random

from markupsafe import Markup


# ============================ SVG-помощники ============================
def U(sym, x, y, w, h, fill=None, stroke=None, extra=''):
    a = f'<use href="#i-{sym}" x="{x}" y="{y}" width="{w}" height="{h}"'
    if fill:
        a += f' fill="{fill}"'
    if stroke:
        a += f' stroke="{stroke}"'
    return a + (' ' + extra if extra else '') + '/>'


def ROW(sym, xs, y, w, h, fills, extra=''):
    return ''.join(U(sym, x, y, w, h, fills[i % len(fills)], extra=extra) for i, x in enumerate(xs))


def _rays(cx, cy, r1, r2, n):
    d = ''
    for i in range(n):
        t, w = 2 * math.pi * i / n, math.pi / n * .55
        p = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))  # noqa
        a1, tip, a2 = p(r1, t - w), p(r2, t), p(r1, t + w)
        d += f'M{a1[0]:.1f} {a1[1]:.1f}L{tip[0]:.1f} {tip[1]:.1f}L{a2[0]:.1f} {a2[1]:.1f}Z'
    return d


def _web(size=200):
    angs, d = [0, 22.5, 45, 67.5, 90], ''
    for a in angs:
        r = math.radians(a)
        d += f'M0 0L{size * math.cos(r):.1f} {size * math.sin(r):.1f}'
    for R in [40, 80, 120, 160, 200]:
        pts = [(R * math.cos(math.radians(x)), R * math.sin(math.radians(x))) for x in angs]
        for i in range(4):
            m = math.radians((angs[i] + angs[i + 1]) / 2)
            d += f'M{pts[i][0]:.1f} {pts[i][1]:.1f}Q{R * .86 * math.cos(m):.1f} {R * .86 * math.sin(m):.1f} {pts[i + 1][0]:.1f} {pts[i + 1][1]:.1f}'
    return d


def _enc(s):
    return s.replace('#', '%23')


WEB_PATH = _web()
WEB_URI = _enc(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200' fill='none' stroke='white' stroke-width='1.2'><path d='{WEB_PATH}'/></svg>")
random.seed(13)
_dr, _x = '', 6
for _L in [16, 34, 20, 44, 14, 28, 38, 18, 30, 12, 40, 22]:
    _dr += f"M{_x} 0H{_x + 9}V{_L}A4.5 4.5 0 0 1 {_x} {_L}Z"
    _x += random.choice([30, 38, 46])
DRIP_URI = _enc(f"<svg xmlns='http://www.w3.org/2000/svg' width='{_x + 10}' height='50' viewBox='0 0 {_x + 10} 50'><path fill='#F4F4F4' d='{_dr}'/></svg>")
_st = ''.join(f"<circle cx='{random.randint(4, 596)}' cy='{random.randint(4, 596)}' r='{random.choice([.6, .8, 1, 1.3])}' fill='white' opacity='{random.choice([.25, .4, .6])}'/>" for _ in range(55))
STAR_URI = _enc(f"<svg xmlns='http://www.w3.org/2000/svg' width='600' height='600'>{_st}</svg>")
PUMP = "M50 16C38 8 20 10 12 28C4 46 10 74 34 82C42 85 58 85 66 82C90 74 96 46 88 28C80 10 62 8 50 16Z M28 36L40 36L34 48Z M60 36L72 36L66 48Z M46 52L54 52L50 60Z M26 62L34 66L40 60L46 68L54 68L60 60L66 66L74 62C70 76 60 80 50 80C40 80 30 76 26 62Z"
GRAIN = "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>\")"

# ============================ Библиотека фигур ============================
MOTIFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-cross" viewBox="0 0 24 24"><path d="M12 3v18M6 9h12"/></symbol>
<symbol id="i-flake" viewBox="0 0 24 24"><path d="M12 2v20M3.3 7l17.4 10M20.7 7 3.3 17M9 3.5l3 2.5 3-2.5M9 20.5l3-2.5 3 2.5"/></symbol>
<symbol id="i-bub" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M8 9a5 5 0 0 1 4-3"/></symbol>
<symbol id="i-heart" viewBox="0 0 24 24"><path d="M12 21C5 15 2 11 2 7.5A5.2 5.2 0 0 1 12 5.5 5.2 5.2 0 0 1 22 7.5C22 11 19 15 12 21Z"/></symbol>
<symbol id="i-petal" viewBox="0 0 24 24"><path d="M12 2C17 7 18 14 12 22C6 14 7 7 12 2Z"/></symbol>
<symbol id="i-leaf" viewBox="0 0 24 24"><path d="M12 2l2.5 5 4-2-1 5 5 .5-3.5 4 2 5-5-1.5L12 22l-1-5.5-5 1.5 2-5L4 9.5 9 10 8 5l4 2Z"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path d="M12 2l3 6.5 7 1-5 5 1.2 7L12 18l-6.2 3.5L7 14.5l-5-5 7-1Z"/></symbol>
<symbol id="i-sparkle" viewBox="0 0 24 24"><path d="M12 0C13 8 16 11 24 12C16 13 13 16 12 24C11 16 8 13 0 12C8 11 11 8 12 0Z"/></symbol>
<symbol id="i-rect" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="1"/></symbol>
<symbol id="i-crescent" viewBox="0 0 100 100"><path d="M60 6A46 46 0 1 0 94 62A38 38 0 0 1 60 6Z"/></symbol>
<symbol id="i-sun" viewBox="0 0 100 100"><path stroke="none" d="M72 50A22 22 0 1 0 28 50A22 22 0 1 0 72 50Z{_rays(50, 50, 28, 48, 12)}"/></symbol>
<symbol id="i-flagsun" viewBox="0 0 100 100"><path stroke="none" fill-rule="evenodd" d="M74 50A24 24 0 1 0 26 50A24 24 0 1 0 74 50Z M67 50A17 17 0 1 1 33 50A17 17 0 1 1 67 50Z"/><path stroke="none" d="{_rays(50, 50, 27, 48, 40)}"/><path fill="none" stroke-width="1.6" d="M50 33Q42 50 50 67M50 33Q58 50 50 67M33 50Q50 42 67 50M33 50Q50 58 67 50"/></symbol>
<symbol id="i-cloud" viewBox="0 0 100 50"><path stroke="none" d="M24 46A16 16 0 0 1 20 14A22 22 0 0 1 62 8A18 18 0 0 1 82 46Z"/></symbol>
<symbol id="i-mount" viewBox="0 0 200 80" preserveAspectRatio="none"><path stroke="none" d="M0 80L48 22L74 50L112 4L162 62L200 36V80Z"/></symbol>
<symbol id="i-wave" viewBox="0 0 200 30" preserveAspectRatio="none"><path stroke="none" d="M0 14Q25 0 50 14T100 14T150 14T200 14V30H0Z"/></symbol>
<symbol id="i-fir" viewBox="0 0 60 80"><path stroke="none" d="M30 2L46 26H38L52 48H42L56 70H4L18 48H8L22 26H14Z"/><path stroke="none" fill="#6B4A2E" d="M26 70H34V80H26Z"/></symbol>
<symbol id="i-treeR" viewBox="0 0 80 110"><path stroke="none" fill="#6B4A2E" d="M36 110V66H44V110Z"/><g stroke="none"><circle cx="40" cy="34" r="30"/><circle cx="18" cy="52" r="18"/><circle cx="62" cy="52" r="18"/><circle cx="40" cy="56" r="20"/></g></symbol>
<symbol id="i-flower" viewBox="0 0 40 40"><g stroke="none"><circle cx="20" cy="9" r="7"/><circle cx="31" cy="17" r="7"/><circle cx="27" cy="30" r="7"/><circle cx="13" cy="30" r="7"/><circle cx="9" cy="17" r="7"/><circle cx="20" cy="20" r="5" fill="#FFD84D"/></g></symbol>
<symbol id="i-tulip" viewBox="0 0 30 60"><path stroke="none" d="M15 3C8 3 5 11 6 19C8 28 22 28 24 19C25 11 22 3 15 3Z"/><path stroke="none" fill="#3E9B4F" d="M14 27H16V58H14Z M15 52C6 50 4 42 4 38C10 40 14 46 15 52Z M15 48C24 46 26 38 26 34C20 36 16 42 15 48Z"/></symbol>
<symbol id="i-mimosa" viewBox="0 0 40 60"><path stroke="none" fill="#3E9B4F" d="M19 26H21V60H19Z"/><g stroke="none"><circle cx="20" cy="8" r="5"/><circle cx="11" cy="14" r="5"/><circle cx="29" cy="14" r="5"/><circle cx="7" cy="23" r="5"/><circle cx="20" cy="19" r="5"/><circle cx="33" cy="23" r="5"/><circle cx="14" cy="28" r="4"/><circle cx="26" cy="28" r="4"/></g></symbol>
<symbol id="i-gift" viewBox="0 0 50 50"><path stroke="none" fill-rule="evenodd" d="M6 22H44V47H6Z M22 22H28V47H22Z"/><path stroke="none" fill-rule="evenodd" d="M3 14H47V22H3Z M22 14H28V22H22Z"/><path stroke="none" d="M25 14C16 3 7 8 12 13C14 15 20 14 25 14Z M25 14C34 3 43 8 38 13C36 15 30 14 25 14Z"/></symbol>
<symbol id="i-ball" viewBox="0 0 30 40"><path stroke="none" d="M13 0H17V5H13Z M15 6A12 12 0 1 0 15.1 6Z"/></symbol>
<symbol id="i-balloon" viewBox="0 0 40 70"><path stroke="none" d="M20 2C8 2 4 14 8 24C11 31 17 36 20 38C23 36 29 31 32 24C36 14 32 2 20 2Z M18 38L22 38L20 43Z"/><path fill="none" stroke="#8a8a8a" stroke-width="1.4" d="M20 43C16 52 24 58 20 68"/></symbol>
<symbol id="i-pencil" viewBox="0 0 100 24"><path stroke="none" d="M18 3H88V21H18Z M2 12L18 3V21Z"/><path stroke="none" fill="#F2A0B3" d="M88 3H98V21H88Z"/><path stroke="none" fill="#BBB" d="M84 3H88V21H84Z"/><path stroke="none" fill="#333" d="M2 12L7 9.5V14.5Z"/></symbol>
<symbol id="i-book" viewBox="0 0 60 50"><path d="M28 10C20 5 9 5 3 8V43C9 40 20 40 28 45Z"/><path d="M32 10C40 5 51 5 57 8V43C51 40 40 40 32 45Z"/></symbol>
<symbol id="i-yurt" viewBox="0 0 120 80"><path fill-rule="evenodd" d="M12 78V46C12 40 28 34 60 34S108 40 108 46V78Z M50 78V56C50 50 70 50 70 56V78Z"/><path d="M0 48C10 22 40 8 60 8S110 22 120 48C100 40 80 35 60 35S20 40 0 48Z"/><path d="M54 8C54 2 66 2 66 8Z"/></symbol>
<symbol id="i-lantern" viewBox="0 0 40 70"><path stroke="none" fill-rule="evenodd" d="M18 0H22V8H18Z M8 10H32L36 22V42L32 52H8L4 42V22Z M14 20H26V42H14Z M16 52H24V62L20 70L16 62Z"/></symbol>
<symbol id="i-mosque" viewBox="0 0 120 100"><path d="M0 100V58H12V30L16 20L20 30V58H32V68C32 48 44 36 60 18C76 36 88 48 88 68V58H100V30L104 20L108 30V58H120V100Z"/></symbol>
<symbol id="i-flag" viewBox="0 0 40 56"><path stroke="none" d="M4 2H7V56H4Z M7 4H36L28 14L36 24H7Z"/></symbol>
<symbol id="i-tag" viewBox="0 0 60 40"><path stroke="none" fill-rule="evenodd" d="M2 20L18 2H58V38H18Z M14 20A4 4 0 1 0 22 20A4 4 0 1 0 14 20Z"/></symbol>
<symbol id="i-snowman" viewBox="0 0 60 90"><circle cx="30" cy="68" r="20" stroke-width="2"/><circle cx="30" cy="40" r="14" stroke-width="2"/><circle cx="30" cy="19" r="10" stroke-width="2"/><path stroke="none" fill="#1c1c1c" d="M20 6H40V10H20Z M24 0H36V7H24Z"/><circle stroke="none" fill="#1c1c1c" cx="27" cy="17" r="1.5"/><circle stroke="none" fill="#1c1c1c" cx="33" cy="17" r="1.5"/><path stroke="none" fill="#F08A24" d="M30 20L40 23L30 25Z"/><path stroke="none" fill="#D6334C" d="M19 29H41V33H19Z"/><circle stroke="none" fill="#1c1c1c" cx="30" cy="44" r="1.6"/><circle stroke="none" fill="#1c1c1c" cx="30" cy="52" r="1.6"/></symbol>
<symbol id="i-pumpkin" viewBox="0 0 100 90"><path fill-rule="evenodd" d="{PUMP}"/><path d="M45 16C45 8 50 3 58 1L61 6C57 8 55 12 55 17Z"/><path fill="none" stroke="#050505" stroke-width="2" opacity=".55" d="M38 12C26 34 28 64 40 83M62 12C74 34 72 64 60 83"/></symbol>
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


# ============================ Сцены (главная) ============================
def SC(inner, defs=''):
    return ('<svg class="scene" viewBox="0 0 520 460" role="img" aria-label="Тематическая иллюстрация"><defs>'
            + defs + '</defs>' + inner + '</svg>')


def MG(c1, c2, i='mg'):
    return f'<radialGradient id="{i}" cx="38%" cy="32%" r="78%"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient>'


def GL(c, op=.3, i='gl'):
    return f'<radialGradient id="{i}"><stop offset="0" stop-color="{c}" stop-opacity="{op}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'


def GR(top, stroke):
    d = (f'<linearGradient id="gv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{top}" stop-opacity="0"/></linearGradient>'
         '<linearGradient id="gh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/><stop offset=".14" stop-color="#fff"/><stop offset=".86" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
         '<mask id="gm"><rect x="0" y="350" width="520" height="110" fill="url(#gh)"/></mask>')
    g = f'<g mask="url(#gm)"><path d="M0 412Q120 388 250 406T520 396V460H0Z" fill="url(#gv)" stroke="{stroke}" stroke-width="1.5"/></g>'
    return d, g


def sc_classic():
    d, g = GR('#DADFE8', '#C2C9D6')
    return SC('<circle cx="300" cy="215" r="150" fill="#2B4BFF"/>'
              '<g transform="rotate(-18 300 150)">' + U('pencil', 150, 110, 300, 72, '#FFE14D') + '</g>'
              '<g transform="rotate(14 300 330)">' + U('pencil', 170, 300, 280, 67, '#fff') + '</g>'
              + U('book', 120, 190, 240, 200, '#fff', '#12141A', 'stroke-width="2.5"') + g
              + U('sparkle', 60, 90, 36, 36, '#2B4BFF') + U('sparkle', 440, 60, 26, 26, '#FFC83D') + U('sparkle', 452, 300, 30, 30, '#2B4BFF'), d)


def sc_midnight():
    d, g = GR('#1A1D2B', '#343A52')
    st = ''.join(U('sparkle', x, y, s, s, '#cfd6ff', extra=f'opacity="{o}"') for x, y, s, o in [(60, 70, 18, .8), (130, 160, 12, .6), (430, 50, 22, .9), (470, 180, 14, .6), (90, 300, 14, .5), (410, 290, 12, .5), (210, 40, 14, .7)])
    return SC('<circle cx="290" cy="200" r="230" fill="url(#gl)"/>' + U('crescent', 160, 40, 270, 270, '#E8EBFF') + st
              + U('mount', 0, 300, 330, 120, '#14172A') + U('mount', 220, 330, 300, 100, '#1B1F35') + g
              + U('book', 200, 345, 130, 108, '#6C7BFF'), GL('#8d9bff', .3) + d)


def sc_winter():
    d, g = GR('#FFFFFF', '#BBD3EA')
    fl = ''.join(U('flake', x, y, s, s, stroke='#7FB2E5', extra='fill="none" stroke-width="1.6"') for x, y, s in [(60, 70, 30), (440, 70, 26), (120, 190, 20), (470, 220, 24), (330, 40, 18)])
    return SC('<circle cx="390" cy="120" r="70" fill="url(#gl)"/><circle cx="390" cy="120" r="40" fill="#FFF1BE"/>'
              + U('cloud', 60, 140, 130, 65, '#fff') + U('cloud', 300, 200, 110, 55, '#fff')
              + U('mount', 0, 210, 340, 135, '#BFD7EE') + U('mount', 200, 240, 330, 130, '#9EC1E4')
              + U('fir', 40, 290, 78, 104, '#2F6B58') + U('fir', 120, 330, 52, 70, '#2F6B58') + U('fir', 440, 300, 66, 88, '#2F6B58') + g
              + U('snowman', 300, 300, 110, 165, '#fff', '#2A4A6B') + fl, GL('#FFE9A0', .6) + d)


def sc_spring():
    d, g = GR('#9AD18B', '#6FB063')
    return SC('<circle cx="410" cy="95" r="80" fill="url(#gl)"/>' + U('sun', 345, 30, 130, 130, '#FFD24A')
              + U('cloud', 60, 80, 130, 65, '#fff') + U('cloud', 250, 150, 100, 50, '#fff')
              + U('treeR', 70, 215, 160, 220, '#FFB3C7') + U('treeR', 350, 250, 120, 165, '#7CCB7E') + g
              + U('tulip', 250, 345, 44, 88, '#E8467C') + U('tulip', 300, 360, 36, 72, '#FF9E43') + U('tulip', 336, 372, 30, 60, '#fff')
              + U('flower', 20, 395, 44, 44, '#FF8FB1') + U('flower', 440, 385, 50, 50, '#fff') + U('flower', 110, 420, 34, 34, '#FFD84D'), GL('#FFF0A8', .7) + d)


def sc_summer():
    d, g = GR('#F6DFA4', '#E8C97A')
    return SC('<circle cx="270" cy="190" r="190" fill="url(#gl)"/>' + U('sun', 140, 60, 260, 260, '#FFC83D')
              + U('cloud', 40, 70, 130, 65, '#fff') + U('cloud', 360, 120, 120, 60, '#fff')
              + U('balloon', 50, 150, 60, 105, '#FF5C7A') + U('balloon', 430, 200, 50, 88, '#4D7CFF')
              + U('wave', 0, 330, 520, 56, '#7FD8EA') + g + U('wave', 0, 365, 520, 58, '#16B5D4')
              + U('wave', 0, 405, 520, 55, '#0E9FBD'), GL('#FFE27A', .6) + d)


def sc_autumn():
    d, g = GR('#C9955B', '#A97A45')
    lv = ''.join(U('leaf', x, y, s, s, c) for x, y, s, c in [(70, 120, 34, '#E07A1F'), (440, 90, 30, '#B5482A'), (130, 220, 24, '#E8B02D'), (460, 230, 28, '#E07A1F'), (250, 70, 22, '#C4581C')])
    return SC('<circle cx="300" cy="250" r="150" fill="url(#gl)"/><circle cx="300" cy="250" r="105" fill="#F6C985" opacity=".7"/>'
              + U('treeR', 40, 190, 170, 235, '#E07A1F') + U('treeR', 300, 215, 150, 205, '#B5482A') + U('treeR', 410, 250, 100, 140, '#E8B02D') + g
              + U('pumpkin', 220, 365, 84, 76, '#E67E22') + U('pumpkin', 330, 395, 52, 47, '#F0A04B') + lv, GL('#FFD08A', .6) + d)


def sc_halloween():
    d, g = GR('#1d1d1d', '#555')
    cr = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(250, 150, 24), (350, 235, 32), (285, 285, 15), (375, 150, 13), (225, 235, 11)])
    ts = 'fill="#050505" stroke="#555" stroke-width="2"'
    return SC('<circle cx="300" cy="205" r="215" fill="url(#gl)"/><circle cx="300" cy="205" r="150" fill="url(#mg)"/><g fill="#000" opacity=".16">' + cr + '</g>'
              + U('tree', 305, 185, 200, 233, stroke='#050505', extra='fill="none"')
              + f'<use href="#i-tomb" x="205" y="352" width="48" height="64" {ts}/><use href="#i-tomb" x="120" y="368" width="34" height="45" {ts}/><use href="#i-tomb" x="455" y="368" width="36" height="48" {ts}/>'
              + g + U('pumpkin', 30, 352, 104, 94, '#F4F4F4', extra='data-boo') + U('pumpkin', 150, 396, 58, 52, '#F4F4F4', extra='data-boo') + U('pumpkin', 390, 398, 68, 62, '#F4F4F4', extra='data-boo')
              + U('ghost', 55, 62, 88, 110, '#F4F4F4', extra='class="floaty" data-boo opacity=".92"')
              + U('bat', 205, 150, 150, 75, '#050505', extra='class="bat"') + U('bat', 338, 82, 72, 36, '#050505', extra='class="bat" style="animation-delay:-.2s"')
              + U('bat', 170, 40, 80, 40, '#F4F4F4', extra='class="bat" style="animation-delay:-.1s"') + U('bat', 430, 20, 64, 32, '#F4F4F4', extra='class="bat" style="animation-delay:-.3s"')
              + U('bat', 20, 250, 56, 28, '#F4F4F4', extra='class="bat" style="animation-delay:-.25s"') + U('bat', 440, 300, 70, 35, '#F4F4F4', extra='class="bat"'),
              GL('#fff', .3) + MG('#FAFAFA', '#8E8E8E') + d)


def sc_newyear():
    d, g = GR('#EAF2FF', '#9DB6E0')
    orn = ''.join(U('ball', x, y, 20, 27, c) for x, y, c in [(215, 170, '#E5484D'), (270, 150, '#F2C14E'), (180, 250, '#F2C14E'), (300, 240, '#E5484D'), (240, 300, '#4D7CFF'), (160, 330, '#E5484D'), (320, 320, '#F2C14E')])
    st = ''.join(U('sparkle', x, y, s, s, '#F2C14E') for x, y, s in [(70, 90, 24), (440, 70, 30), (90, 240, 16), (450, 230, 20), (400, 140, 14)])
    return SC('<circle cx="260" cy="200" r="210" fill="url(#gl)"/>' + U('fir', 120, 50, 280, 373, '#1F7A4D') + orn + U('star', 232, 6, 56, 56, '#F2C14E') + g
              + U('gift', 40, 372, 78, 78, '#E5484D') + U('gift', 400, 378, 70, 70, '#4D7CFF') + U('gift', 120, 400, 52, 52, '#F2C14E') + U('gift', 350, 410, 44, 44, '#E5484D') + st, GL('#F2C14E', .25) + d)


def sc_valentine():
    d, g = GR('#FFD6E2', '#F4A9C0')
    sm = ''.join(U('heart', x, y, s, s, c, extra=f'opacity="{o}"') for x, y, s, c, o in [(60, 90, 50, '#FF8FAB', .9), (420, 70, 44, '#FFB3C7', .9), (70, 260, 30, '#FFB3C7', .8), (440, 250, 36, '#FF8FAB', .9), (360, 30, 24, '#D6336C', .8)])
    return SC('<circle cx="270" cy="210" r="210" fill="url(#gl)"/>' + U('heart', 130, 70, 270, 270, '#D6336C') + U('sparkle', 200, 120, 40, 40, '#fff', extra='opacity=".7"') + sm
              + U('balloon', 40, 330, 50, 88, '#FF8FAB') + g + U('gift', 380, 345, 90, 90, '#D6336C') + U('gift', 300, 395, 50, 50, '#FF8FAB'), GL('#FF8FAB', .35) + d)


def sc_women8():
    d, g = GR('#E7D2F7', '#CBA6E6')
    fl = ''.join(U('flower', x, y, s, s, c) for x, y, s, c in [(60, 70, 54, '#FF8FB1'), (420, 60, 60, '#FFD23F'), (40, 250, 46, '#fff'), (440, 240, 50, '#FF8FB1'), (120, 360, 40, '#FFD23F')])
    return SC('<circle cx="260" cy="210" r="205" fill="url(#gl)"/><circle cx="260" cy="145" r="60" fill="none" stroke="#9B4DCA" stroke-width="28"/><circle cx="260" cy="268" r="76" fill="none" stroke="#9B4DCA" stroke-width="28"/>'
              + fl + g + U('mimosa', 360, 330, 60, 90, '#FFD23F') + U('mimosa', 110, 345, 52, 78, '#FFD23F') + U('tulip', 200, 355, 40, 80, '#E8467C') + U('tulip', 300, 370, 34, 68, '#9B4DCA'), GL('#C48CF0', .4) + d)


def sc_defender():
    d, g = GR('#5E7B5F', '#3E5A40')
    return SC('<circle cx="270" cy="210" r="210" fill="url(#gl)"/><circle cx="270" cy="210" r="145" fill="#2F5D3A"/>' + U('star', 160, 100, 220, 220, '#E2C066')
              + U('mount', 0, 270, 300, 130, '#9AAA9B') + U('mount', 230, 290, 290, 110, '#7F917F') + g
              + U('flag', 50, 290, 70, 98, '#C0392B') + U('flag', 420, 300, 66, 92, '#C0392B') + U('star', 60, 80, 30, 30, '#C8A24A') + U('star', 430, 90, 26, 26, '#C8A24A'), GL('#8FB58F', .45) + d)


def sc_nooruz():
    d, g = GR('#8FD08C', '#62AE62')
    tl = ''.join(U('tulip', x, y, w, h, c) for x, y, w, h, c in [(40, 350, 40, 80, '#E8467C'), (90, 370, 34, 68, '#FFC93C'), (350, 360, 40, 80, '#fff'), (400, 350, 44, 88, '#E8467C'), (450, 378, 32, 64, '#FFC93C')])
    return SC('<circle cx="400" cy="100" r="90" fill="url(#gl)"/>' + U('sun', 335, 35, 130, 130, '#FFC93C') + U('cloud', 60, 90, 130, 65, '#fff')
              + U('mount', 0, 200, 320, 140, '#BFD8C4') + U('mount', 200, 230, 330, 130, '#A5C8AE') + g
              + U('yurt', 150, 310, 200, 133, '#fff', '#1F8A4C', 'stroke-width="3"') + tl, GL('#FFE9A0', .6) + d)


def sc_school():
    d, g = GR('#E8DDC0', '#CDBE95')
    pen = ''.join(f'<g transform="rotate({r} {cx} {cy})">' + U('pencil', cx - 130, cy - 28, 260, 62, c) + '</g>' for r, cx, cy, c in [(-24, 280, 120, '#FFD84D'), (18, 300, 330, '#FF6B6B'), (-8, 260, 410, '#4D9BFF')])
    return SC('<path d="M60 90Q200 60 300 95T470 80" fill="none" stroke="#FFD84D" stroke-width="16" stroke-linecap="round" opacity=".75"/>' + pen
              + U('book', 100, 150, 320, 267, '#fff', '#1B2A5C', 'stroke-width="3.5"') + g + U('star', 40, 250, 40, 40, '#FFD84D') + U('sparkle', 450, 200, 34, 34, '#2B4BFF') + U('star', 440, 330, 28, 28, '#FF6B6B'), d)


def sc_eid():
    d, g = GR('#0A271F', '#D9B44A')
    th = ''.join(f'<line x1="{x + w / 2}" y1="0" x2="{x + w / 2}" y2="{y}" stroke="#D9B44A" stroke-width="1.5"/>' + U('lantern', x, y, w, h, '#D9B44A') for x, y, w, h in [(70, 40, 50, 88), (440, 20, 42, 74), (370, 70, 30, 52)])
    st = ''.join(U('sparkle', x, y, s, s, '#F4E4A6', extra='opacity=".85"') for x, y, s in [(150, 90, 18), (460, 190, 22), (60, 210, 14), (230, 40, 14), (420, 300, 14)])
    return SC('<circle cx="290" cy="190" r="215" fill="url(#gl)"/>' + U('crescent', 170, 40, 250, 250, '#D9B44A') + U('star', 390, 120, 54, 54, '#D9B44A') + th + st
              + U('mosque', 135, 262, 255, 191, '#0F3A2E', '#D9B44A', 'stroke-width="2"') + g, GL('#D9B44A', .25) + d)


def sc_independence():
    d, g = GR('#E9D8B8', '#CDB78A')
    return SC('<circle cx="270" cy="200" r="215" fill="url(#gl)"/><circle cx="270" cy="205" r="150" fill="#E8112D"/>' + U('flagsun', 130, 65, 280, 280, '#FFEF00', '#E8112D')
              + U('mount', 0, 280, 300, 120, '#D9C39B') + U('mount', 220, 300, 300, 100, '#C9B084') + g
              + U('flag', 40, 300, 66, 92, '#E8112D') + U('flag', 440, 310, 60, 84, '#E8112D') + U('yurt', 340, 345, 120, 80, '#fff', '#E8112D', 'stroke-width="3"'), GL('#FFEF00', .35) + d)


def sc_sale():
    d, g = GR('#111111', '#FFE600')
    tg = ''.join(U('tag', x, y, w, w * .66, c, extra=f'transform="rotate({r} {x + w / 2} {y + w / 3})"') for x, y, w, c, r in [(40, 80, 100, '#E3262F', -14), (400, 60, 90, '#111', 12), (60, 300, 84, '#111', 10), (410, 290, 100, '#E3262F', -10)])
    return SC('<circle cx="270" cy="205" r="150" fill="#111"/><circle cx="215" cy="150" r="34" fill="none" stroke="#FFE600" stroke-width="26"/><circle cx="325" cy="262" r="34" fill="none" stroke="#FFE600" stroke-width="26"/>'
              '<path d="M335 110L205 300" stroke="#FFE600" stroke-width="26" stroke-linecap="round"/>' + tg + g + U('sparkle', 90, 200, 30, 30, '#E3262F') + U('sparkle', 440, 190, 24, 24, '#111'), d)


# ============================ Подвал-пейзаж ============================
def Y(back, gfill, gstroke, front='', glow='rgba(255,255,255,.09)', extra=''):
    return ('<div class="yard" aria-hidden="true" style="--yg:' + glow + '"><svg class="bg" viewBox="0 0 1200 130" preserveAspectRatio="xMidYMax slice">' + back
            + f'<path d="M0 130V100Q150 80 300 98T600 96T900 100T1200 92V130Z" fill="{gfill}" stroke="{gstroke}" stroke-width="1.2"/>' + front + '</svg>' + extra + '</div>')


def yd_midnight():
    return Y(ROW('sparkle', [90, 260, 470, 700, 930, 1110], 12, 14, 14, ['#cfd6ff']) + U('mount', 0, 56, 520, 60, '#14172A') + U('mount', 640, 60, 560, 56, '#14172A'), '#14172A', '#343A52', glow='rgba(120,140,255,.10)')


def yd_winter():
    return Y(ROW('fir', [60, 250, 520, 910, 1090], 14, 70, 93, ['#2F6B58']) + ROW('fir', [150, 700, 990], 44, 46, 61, ['#2F6B58']), '#FFFFFF', '#BBD3EA',
             U('snowman', 600, 52, 52, 78, '#fff', '#2A4A6B') + ROW('flake', [140, 380, 820, 1030], 20, 22, 22, ['#7FB2E5'], 'fill="none" stroke="#7FB2E5" stroke-width="1.6"'), glow='rgba(120,170,230,.18)')


def yd_spring():
    return Y(ROW('treeR', [80, 430, 800, 1090], 8, 76, 105, ['#FFB3C7', '#7CCB7E', '#FFB3C7', '#7CCB7E']), '#9AD18B', '#6FB063',
             ROW('tulip', [200, 330, 560, 700, 960], 70, 28, 56, ['#E8467C', '#FF9E43', '#fff']) + ROW('flower', [150, 270, 480, 640, 880, 1030], 84, 30, 30, ['#FF8FB1', '#fff', '#FFD84D']), glow='rgba(150,210,140,.22)')


def yd_summer():
    return Y(ROW('balloon', [220, 940], 6, 38, 66, ['#FF5C7A', '#4D7CFF']) + ROW('cloud', [90, 560], 12, 90, 45, ['#fff']), '#F6DFA4', '#E8C97A',
             U('wave', 0, 82, 1200, 30, '#7FD8EA') + U('wave', 0, 100, 1200, 34, '#16B5D4'), glow='rgba(255,210,100,.25)')


def yd_autumn():
    return Y(ROW('treeR', [100, 380, 700, 1000], 8, 76, 105, ['#E07A1F', '#B5482A', '#E8B02D']), '#C9955B', '#A97A45',
             ROW('pumpkin', [240, 560, 880], 80, 44, 40, ['#E67E22']) + ROW('leaf', [160, 340, 480, 680, 820, 1060], 90, 20, 20, ['#C4581C', '#E8B02D', '#B5482A']), glow='rgba(230,150,70,.2)')


def yd_halloween():
    ts = 'fill="#0D0D0D" stroke="#3a3a3a" stroke-width="1.5"'
    back = (U('tree', 150, 2, 120, 140, stroke='#0D0D0D', extra='fill="none"') + U('tree', 860, 14, 96, 112, stroke='#0D0D0D', extra='fill="none"')
            + ''.join(f'<use href="#i-tomb" x="{x}" y="{y}" width="{w}" height="{h}" {ts}/>' for x, y, w, h in [(40, 62, 40, 53), (380, 58, 46, 61), (520, 76, 32, 42), (740, 64, 42, 56), (1050, 60, 44, 58)]))
    front = (U('pumpkin', 300, 82, 56, 50, '#F4F4F4') + U('pumpkin', 640, 92, 38, 34, '#F4F4F4') + U('pumpkin', 970, 80, 64, 58, '#F4F4F4')
             + U('ghost', 1130, 14, 38, 48, '#F4F4F4', extra='class="floaty" data-boo opacity=".9"')
             + U('bat', 460, 14, 46, 23, '#F4F4F4', extra='class="bat"') + U('bat', 570, 30, 30, 15, '#F4F4F4', extra='class="bat" style="animation-delay:-.2s"'))
    eyes = ('<svg class="eyes" style="left:14%;bottom:62px" viewBox="0 0 40 14"><use href="#i-eyes" fill="#F4F4F4"/></svg>'
            '<svg class="eyes" style="left:76%;bottom:58px;animation-delay:-3s" viewBox="0 0 40 14"><use href="#i-eyes" fill="#F4F4F4"/></svg>')
    return Y(back, '#0D0D0D', '#3a3a3a', front, extra=eyes)


def yd_newyear():
    return Y(ROW('fir', [50, 280, 620, 960, 1100], 8, 80, 106, ['#1F7A4D']) + ROW('sparkle', [180, 430, 800, 1040], 18, 16, 16, ['#F2C14E']), '#EAF2FF', '#9DB6E0',
             ROW('gift', [140, 380, 560, 760, 900], 82, 36, 36, ['#E5484D', '#4D7CFF', '#F2C14E']), glow='rgba(120,160,255,.2)')


def yd_valentine():
    return Y(ROW('heart', [100, 360, 640, 900, 1120], 20, 40, 37, ['#FFB3C7'], 'opacity=".75"'), '#FFD6E2', '#F4A9C0',
             ROW('heart', list(range(60, 1200, 110)), 88, 30, 28, ['#D6336C', '#FF8FAB']), glow='rgba(255,140,170,.2)')


def yd_women8():
    return Y(ROW('mimosa', [120, 480, 840, 1100], 40, 42, 63, ['#FFD23F']) + ROW('tulip', [260, 620, 980], 54, 30, 60, ['#E8467C', '#9B4DCA']), '#E7D2F7', '#CBA6E6',
             ROW('flower', list(range(60, 1200, 120)), 86, 30, 30, ['#FF8FB1', '#fff', '#FFD23F']), glow='rgba(190,140,240,.2)')


def yd_defender():
    return Y(U('mount', 0, 36, 420, 86, '#9AAA9B') + U('mount', 330, 46, 460, 76, '#7F917F') + U('mount', 760, 30, 440, 92, '#9AAA9B'), '#5E7B5F', '#3E5A40',
             ROW('flag', [160, 520, 900, 1100], 46, 32, 46, ['#C0392B']) + ROW('star', [340, 700], 90, 22, 22, ['#C8A24A']), glow='rgba(120,160,120,.2)')


def yd_nooruz():
    return Y(U('mount', 0, 34, 520, 88, '#BFD8C4') + U('mount', 640, 40, 560, 82, '#BFD8C4') + ROW('yurt', [260, 860], 48, 110, 73, ['#fff'], 'stroke="#1F8A4C" stroke-width="2.5"'), '#8FD08C', '#62AE62',
             ROW('tulip', list(range(40, 1200, 100)), 74, 26, 52, ['#E8467C', '#FFC93C', '#fff']), glow='rgba(255,220,120,.22)')


def yd_school():
    cols = ['#FFD84D', '#FF6B6B', '#4D9BFF', '#7ED957', '#B58CFF']
    pens = ''.join(f'<use href="#i-pencil" x="{x - 50}" y="{50 + (i % 3) * 4 - 12}" width="100" height="24" fill="{cols[i % 5]}" transform="rotate(90 {x} {50 + (i % 3) * 4})"/>' for i, x in enumerate(range(40, 1200, 56)))
    return Y(pens, '#E8DDC0', '#CDBE95', glow='rgba(43,75,255,.10)')


def yd_eid():
    return Y(ROW('mosque', [80, 400, 780, 1060], 14, 110, 92, ['#0F3A2E'], 'stroke="#D9B44A" stroke-width="1.4"') + ROW('sparkle', [260, 600, 940], 20, 14, 14, ['#F4E4A6']), '#0A271F', '#D9B44A',
             ROW('lantern', [200, 560, 900], 4, 20, 36, ['#D9B44A']), glow='rgba(217,180,74,.18)')


def yd_independence():
    return Y(U('mount', 0, 36, 440, 86, '#D9C39B') + U('mount', 760, 30, 440, 92, '#D9C39B') + ROW('yurt', [300, 640], 50, 110, 73, ['#fff'], 'stroke="#E8112D" stroke-width="2.5"'), '#E9D8B8', '#CDB78A',
             ROW('flag', [140, 520, 860, 1090], 46, 32, 46, ['#E8112D']), glow='rgba(232,17,45,.12)')


def yd_sale():
    return Y('', '#111111', '#FFE600', ROW('tag', list(range(70, 1200, 130)), 74, 62, 41, ['#E3262F', '#FFE600']), glow='rgba(255,230,0,.2)')


# ============================ Бегущая строка / украшения ============================
def ticker(phrases, sym, vb):
    grp = ''.join(f'<span>{t}</span><svg viewBox="{vb}"><use href="#i-{sym}"/></svg>' for t in phrases)
    return f'<div class="ticker" aria-hidden="true"><div class="tk"><div class="tkg">{grp}</div><div class="tkg">{grp}</div></div></div>'


def bunting(colors, n=26):
    flags, w = '', 1200 / n
    for i in range(n):
        x = i * w
        y = 4 + 14 * math.sin(math.pi * (i + .5) / n * 1) * 1.0
        flags += f'<path d="M{x + 3:.1f} {y:.1f}L{x + w - 3:.1f} {y:.1f}L{x + w / 2:.1f} {y + 34:.1f}Z" fill="{colors[i % len(colors)]}"/>'
    return f'<svg class="bunt" viewBox="0 0 1200 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 4Q600 40 1200 4" fill="none" stroke="#888" stroke-width="1.5" opacity=".6"/>{flags}</svg>'


def garland(n=18):
    cols, out = ['#E5484D', '#F2C14E', '#3DDC84', '#4D7CFF'], ''
    for i in range(n):
        x = (i + .5) * 1200 / n
        y = 6 + 22 * math.sin(math.pi * (i + .5) / n)
        out += f'<circle class="bulb" style="animation-delay:-{(i % 4) * .4}s" cx="{x:.1f}" cy="{y + 10:.1f}" r="6" fill="{cols[i % 4]}"/>'
    return f'<svg class="garland" viewBox="0 0 1200 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 4Q600 36 1200 4" fill="none" stroke="#7a8aa8" stroke-width="1.5"/>{out}</svg>'


def halloween_deco():
    sp = ('<div class="dang" data-boo style="right:8%"><i class="th" style="height:80px"></i><svg viewBox="0 0 60 60"><use href="#i-spider" fill="#F4F4F4" stroke="#F4F4F4"/></svg></div>'
          '<div class="dang d2" data-boo style="right:27%;animation-delay:-2s"><i class="th" style="height:46px"></i><svg viewBox="0 0 60 60" style="width:28px;height:28px"><use href="#i-spider" fill="#F4F4F4" stroke="#F4F4F4"/></svg></div>')
    return '<div class="deco"><div class="drips"></div>' + sp + '</div>'


HALLOWEEN_SKY = ('<div class="sky" aria-hidden="true">' + ''.join(
    f'<svg class="fb b{i}" viewBox="0 0 64 32"><use class="bat" href="#i-bat" fill="#F4F4F4"/></svg>' for i in (1, 2, 3)) + '</div>')

CANDLES = ('<div class="candles" aria-hidden="true">' + ''.join(
    f'<div class="c" style="width:{w}px"><svg class="f fl" viewBox="0 0 30 30" style="top:-{w - 4}px;width:{w}px;height:{w}px;animation-delay:-{d}s"><use href="#i-flame"/></svg><svg viewBox="0 0 30 72" style="height:{h}px"><use href="#i-candle"/></svg></div>'
    for w, h, d in [(22, 70, .05), (28, 110, .1), (20, 56, .08)]) + '</div>')

# ============================ Описание тем ============================
DEF = dict(bg='#F5F6F8', bg2='#FFFFFF', sf='#FFFFFF', sf2='#F0F1F4', ink='#12141A', mut='#697082', line='#E3E6EC', pri='#2B4BFF', onpri='#FFFFFF',
           acc='#FFE14D', onacc='#12141A', hd='rgba(255,255,255,.92)', glow='transparent', fx='#8aa', inp='#FFFFFF', price='var(--ink)', tkbg='var(--ink)',
           tkfg='var(--bg)', imgf='none', hv='rgba(18,20,26,.18)', grain='0', bgimg='linear-gradient(transparent,transparent)', r='10px', rc='16px', up='none',
           ls='0', hup='none', hw='800', k='.72', tile='16px', em='var(--mut)', emst='normal', lgbg='var(--pri)', lgfg='var(--onpri)', lgb='var(--pri)', yg='rgba(0,0,0,.05)')


def T(id, name, group, desc, fonts, hf, bf, vars, hero, ticker_, tsym, fx, fxn, scene, yard, icon, orn, tile_kind, tags, ill, **kw):
    v = dict(DEF)
    v.update(vars)
    v['hf'], v['bf'] = hf, bf
    return dict(id=id, name=name, group=group, desc=desc, fonts=fonts, vars=v, hero=hero, ticker=ticker_, tsym=tsym, fx=fx, fxn=fxn, scene=scene,
                yard=yard, icon=icon, orn=orn, tile_kind=tile_kind, tags=tags, ill=ill, **kw)


GEN_T = {'cart': 'Корзина пуста', 'search': 'Ничего не найдено', 'empty': 'Здесь пока пусто', 'err404': 'Страница не найдена', 'err404p': 'Возможно, адрес набран неверно.'}
INTER = 'Inter:wght@400;500;600'

THEMES_LIST = [
    T('classic', 'Классика', 'Базовые', 'Светлый, чистый, чернильно-синий акцент', [INTER, 'Manrope:wght@700;800'], 'Manrope,Inter,sans-serif', 'Inter,system-ui,sans-serif', {},
      ('Всё для учёбы,', 'работы и творчества', 'Выберите товары и оставьте предзаказ. Мы свяжемся с вами и подтвердим наличие.'),
      ['Ручки и маркеры', 'Тетради и блокноты', 'Краски и кисти', 'Всё для офиса', 'Предзаказ за минуту'], ('star', '0 0 24 24'), 'none', 0, sc_classic(), None, 'star', 'sparkle', 'fill',
      GEN_T, ('book', '0 0 60 50'), tag='Спасибо, что вы с нами'),
    T('midnight', 'Полночь', 'Базовые', 'Тёмный минимализм со звёздами', [INTER, 'Manrope:wght@700;800'], 'Manrope,Inter,sans-serif', 'Inter,system-ui,sans-serif',
      dict(bg='#0B0C10', bg2='#1B1E2E', sf='#13151B', sf2='#1A1D27', ink='#ECEEF4', mut='#8D93A8', line='#262A38', pri='#6C7BFF', acc='#6C7BFF', onacc='#fff', hd='rgba(11,12,16,.9)',
           inp='#0B0C10', fx='#cfd6ff', tkbg='#13151B', tkfg='#ECEEF4', hv='rgba(108,123,255,.35)', glow='rgba(108,123,255,.25)', yg='rgba(120,140,255,.10)', em='#8D93A8'),
      ('Канцелярия', 'для тихих вечеров', 'Тетради, ручки и краски для тех, кто работает, когда город засыпает.'),
      ['Тихие вечера', 'Ручки для ночных идей', 'Тетради с хорошей бумагой', 'Предзаказ без спешки'], ('sparkle', '0 0 24 24'), 'stars', 40, sc_midnight(), yd_midnight(), 'sparkle', 'crescent', 'fill', GEN_T, ('crescent', '0 0 100 100'), tag='Доброй ночи'),
    T('winter', 'Зима', 'Сезоны', 'Снегопад, ёлки и голубой лёд', ['Nunito:wght@400;600;700;800', 'Comfortaa:wght@600;700'], 'Comfortaa,Nunito,sans-serif', 'Nunito,system-ui,sans-serif',
      dict(bg='#EAF3FB', bg2='#FFFFFF', sf='#FFFFFF', sf2='#E4EFFA', ink='#10294A', mut='#5B7595', line='#CFE1F3', pri='#2477D6', acc='#A8D8FF', onacc='#10294A', hd='rgba(255,255,255,.9)', fx='#8DB9E8',
           tkbg='#2477D6', tkfg='#fff', hv='rgba(36,119,214,.25)', r='14px', rc='22px', tile='22px', hw='700', k='.7', em='#2477D6', yg='rgba(120,170,230,.18)'),
      ('Зимние вечера —', 'время новых тетрадей', 'Тёплый свет лампы, горячий чай и красивая канцелярия. Оставьте предзаказ, мы всё подготовим.'),
      ['Снежные вечера', 'Тетради для зимних планов', 'Тёплые идеи', 'Ручки, которые не замерзают', 'Предзаказ у камина'], ('flake', '0 0 24 24'), 'snow', 70, sc_winter(), yd_winter(), 'flake', 'sparkle', 'stroke', GEN_T, ('snowman', '0 0 60 90'), tag='Тепла и уюта'),
    T('spring', 'Весна', 'Сезоны', 'Цветущие деревья, лепестки и тюльпаны', ['Nunito:wght@400;600;700;800'], 'Nunito,sans-serif', 'Nunito,system-ui,sans-serif',
      dict(bg='#F3FAF0', bg2='#FFFFFF', sf='#FFFFFF', sf2='#E9F5E4', ink='#1D3B2A', mut='#5F8069', line='#D5EACD', pri='#2F8F46', acc='#FFB3C7', onacc='#4A1730', hd='rgba(255,255,255,.9)', fx='#FF9DB8',
           tkbg='#2F8F46', tkfg='#fff', hv='rgba(47,143,70,.25)', r='14px', rc='22px', tile='22px', hw='800', k='.68', em='#E8467C', yg='rgba(150,210,140,.22)'),
      ('Весна пришла —', 'пора начинать новое', 'Свежие тетради, яркие краски и ручки для новых планов. Выберите и оставьте предзаказ.'),
      ['Весеннее настроение', 'Краски цвета тюльпанов', 'Новые тетради для новых планов', 'Цветущие идеи', 'Предзаказ с улыбкой'], ('flower', '0 0 40 40'), 'petals', 26, sc_spring(), yd_spring(), 'flower', 'flower', 'fill', GEN_T, ('flower', '0 0 40 40'), tag='С первым теплом'),
    T('summer', 'Лето', 'Сезоны', 'Солнце, море и яркие цвета', ['Rubik:wght@400;500;600;800', 'Rubik:wght@800'], 'Rubik,sans-serif', 'Rubik,system-ui,sans-serif',
      dict(bg='#FFFBEA', bg2='#FFFFFF', sf='#FFFFFF', sf2='#FFF3C9', ink='#0E3B43', mut='#4F7F86', line='#FBE7A8', pri='#0891B2', acc='#FFC83D', onacc='#0E3B43', hd='rgba(255,251,234,.92)', fx='#38C6E4',
           tkbg='#0891B2', tkfg='#fff', hv='rgba(8,145,178,.25)', r='14px', rc='22px', tile='22px', hw='800', k='.66', em='#E8590C', yg='rgba(255,210,100,.25)'),
      ('Лето — время', 'ярких красок', 'Скетчбуки, маркеры и всё для творчества на каникулах. Выбирайте и оставляйте предзаказ.'),
      ['Лето, солнце, краски', 'Скетчбуки для каникул', 'Яркие маркеры', 'Творчество на свежем воздухе', 'Предзаказ на пляже'], ('sun', '0 0 100 100'), 'bubbles', 22, sc_summer(), yd_summer(), 'sun', 'sun', 'fill', GEN_T, ('sun', '0 0 100 100'), tag='Отличного лета'),
    T('autumn', 'Осень', 'Сезоны', 'Золотые листья, тыквы и тёплые тона', ['Lora:wght@500;600;700', INTER], 'Lora,Georgia,serif', 'Inter,system-ui,sans-serif',
      dict(bg='#FBF3E9', bg2='#FFFAF2', sf='#FFFAF4', sf2='#F6E8D6', ink='#3B2417', mut='#85624A', line='#EBD6BF', pri='#C4581C', acc='#E8A33D', onacc='#3B2417', hd='rgba(251,243,233,.92)', fx='#E07A1F',
           tkbg='#3B2417', tkfg='#F6DDB8', hv='rgba(196,88,28,.28)', r='8px', rc='14px', tile='14px', hw='700', k='.78', em='#C4581C', yg='rgba(230,150,70,.2)'),
      ('Осень — время', 'тёплых тетрадей', 'Золотые листья, свежие учебные планы и красивая канцелярия. Оставьте предзаказ.'),
      ['Золотая осень', 'Тетради для новых планов', 'Тёплые оттенки', 'Ручки под шуршание листьев', 'Предзаказ с чаем'], ('leaf', '0 0 24 24'), 'leaves', 26, sc_autumn(), yd_autumn(), 'leaf', 'leaf', 'fill', GEN_T, ('leaf', '0 0 24 24'), tag='Тёплой осени'),
    T('halloween', 'Хэллоуин', 'Праздники', 'Мрачный чёрно-белый: луна, мыши, тыквы, кладбище', ['Cormorant:ital,wght@0,600;0,700;1,600', INTER], 'Cormorant,Georgia,serif', 'Inter,system-ui,sans-serif',
      dict(bg='#050505', bg2='#1d1d1d', sf='#0D0D0D', sf2='#161616', ink='#F4F4F4', mut='#8F8F8F', line='#2A2A2A', pri='#F4F4F4', onpri='#050505', acc='#F4F4F4', onacc='#050505', hd='rgba(5,5,5,.9)',
           glow='rgba(255,255,255,.22)', inp='#050505', imgf='grayscale(1) contrast(1.08) brightness(.92)', hv='rgba(255,255,255,.3)', grain='.06', bgimg=f'url("data:image/svg+xml;utf8,{STAR_URI}")',
           r='2px', rc='2px', up='uppercase', ls='.14em', hw='700', k='1', tile='90px 90px 0 0', lgbg='transparent', lgfg='var(--ink)', lgb='var(--ink)', yg='rgba(255,255,255,.09)', fx='#F4F4F4', emst='italic'),
      ('Канцелярия для', 'долгих ночей', 'Ручки, тетради, краски и всё для тех, кто пишет, рисует и учится допоздна. Выберите нужное и оставьте предзаказ.'),
      ['Ручки, которые не боятся темноты', 'Тетради с секретами', 'Краски для ночных кошмаров', 'Предзаказ до первых петухов', 'Пишите осторожно'], ('pumpkin', '0 0 100 90'), 'none', 0, sc_halloween(), yd_halloween(), 'cross', 'skull', 'stroke',
      {'cart': 'В котле пусто', 'search': 'Ничего не найдено', 'empty': 'Здесь пока пусто', 'err404': 'Эта страница ушла в мир иной', 'err404p': 'Её здесь больше нет. Вернитесь к живым.'},
      ('ghost', '0 0 64 80'), tag='Пишите осторожно', logo='<b><svg class="i"><use href="#i-moon"/></svg></b>', sky=HALLOWEEN_SKY, deco=halloween_deco(), login=CANDLES, css_key='halloween',
      ill_cart=('cauldron', '0 0 80 66'), ill_empty=('skull', '0 0 64 72'), ok=('pumpkin', '0 0 100 90')),
    T('newyear', 'Новый год', 'Праздники', 'Ночное небо, ёлка, гирлянда и подарки', ['Playfair Display:wght@600;700;800', INTER], 'Playfair Display,Georgia,serif', 'Inter,system-ui,sans-serif',
      dict(bg='#0A1630', bg2='#1B2E63', sf='#11204A', sf2='#162A5E', ink='#F6F1E6', mut='#9FB0D6', line='#25396E', pri='#F2C14E', onpri='#1A1200', acc='#E5484D', onacc='#fff', hd='rgba(10,22,48,.9)',
           inp='#0A1630', fx='#FFFFFF', tkbg='#E5484D', tkfg='#fff', hv='rgba(242,193,78,.35)', glow='rgba(242,193,78,.3)', r='12px', rc='18px', tile='18px', hw='700', k='.8', em='#F2C14E', yg='rgba(120,160,255,.2)'),
      ('С Новым годом!', 'Пусть всё сбудется', 'Красивая канцелярия для планов на новый год и подарков близким. Выберите нужное и оставьте предзаказ.'),
      ['С Новым годом', 'Планы на год в новой тетради', 'Подарки с заботой', 'Волшебство рядом', 'Предзаказ к празднику'], ('star', '0 0 24 24'), 'snow', 60, sc_newyear(), yd_newyear(), 'star', 'star', 'fill', GEN_T,
      ('gift', '0 0 50 50'), tag='С Новым годом', deco_extra=garland(), css_key='newyear'),
    T('valentine', 'День влюблённых', 'Праздники', '14 февраля: сердечки и нежно-розовый', ['Pacifico', 'Nunito:wght@400;600;700;800'], 'Pacifico,cursive', 'Nunito,system-ui,sans-serif',
      dict(bg='#FFF1F4', bg2='#FFFFFF', sf='#FFFFFF', sf2='#FFE3EA', ink='#4A1730', mut='#9A5670', line='#FAD3DE', pri='#D6336C', acc='#FF8FAB', onacc='#4A1730', hd='rgba(255,241,244,.92)', fx='#F06292',
           tkbg='#D6336C', tkfg='#fff', hv='rgba(214,51,108,.3)', r='999px', rc='24px', tile='24px', hw='400', k='.62', em='#D6336C', yg='rgba(255,140,170,.2)'),
      ('Для тех,', 'кого любишь', 'Открытки, блокноты и милые мелочи в подарок. Выберите нужное и оставьте предзаказ.'),
      ['Сделано с любовью', 'Милые блокноты', 'Подарок для любимого человека', 'Сердечные мелочи', 'Предзаказ с нежностью'], ('heart', '0 0 24 24'), 'hearts', 24, sc_valentine(), yd_valentine(), 'heart', 'heart', 'fill', GEN_T, ('heart', '0 0 24 24'), tag='С любовью'),
    T('women8', '8 Марта', 'Праздники', 'Мимоза, цветы и сиреневый', ['Marck Script', 'Nunito:wght@400;600;700;800'], 'Marck Script,cursive', 'Nunito,system-ui,sans-serif',
      dict(bg='#FBF4FF', bg2='#FFFFFF', sf='#FFFFFF', sf2='#F3E6FB', ink='#3A1F4D', mut='#8A6AA0', line='#E8D5F5', pri='#9B4DCA', acc='#FFD23F', onacc='#3A1F4D', hd='rgba(251,244,255,.92)', fx='#FFC933',
           tkbg='#9B4DCA', tkfg='#fff', hv='rgba(155,77,202,.3)', r='999px', rc='24px', tile='24px', hw='400', k='.82', em='#9B4DCA', yg='rgba(190,140,240,.2)'),
      ('С 8 Марта,', 'дорогие женщины!', 'Подарки, блокноты и красивые мелочи для самых любимых. Выберите и оставьте предзаказ.'),
      ['С праздником весны', 'Цветы и мимоза', 'Блокноты для особенных людей', 'Подарок с душой', 'Предзаказ к 8 Марта'], ('flower', '0 0 40 40'), 'petals', 28, sc_women8(), yd_women8(), 'flower', 'flower', 'fill', GEN_T, ('mimosa', '0 0 40 60'), tag='С 8 Марта'),
    T('defender', '23 Февраля', 'Праздники', 'День защитника Отечества: хаки и золото', ['Oswald:wght@500;600;700', INTER], 'Oswald,sans-serif', 'Inter,system-ui,sans-serif',
      dict(bg='#EEF1EC', bg2='#FFFFFF', sf='#FFFFFF', sf2='#E4EAE2', ink='#1E2A22', mut='#5E6F62', line='#D3DBD0', pri='#2F5D3A', acc='#C8A24A', onacc='#1E2A22', hd='rgba(238,241,236,.94)', fx='#C8A24A',
           tkbg='#2F5D3A', tkfg='#F1E3B5', hv='rgba(47,93,58,.28)', r='4px', rc='6px', up='uppercase', ls='.1em', hup='uppercase', tile='6px', hw='700', k='.7', em='#2F5D3A', yg='rgba(120,160,120,.2)'),
      ('С Днём', 'защитника Отечества', 'Подарки для настоящих защитников: блокноты, ручки и многое другое. Выберите и оставьте предзаказ.'),
      ['С 23 Февраля', 'Подарки для защитников', 'Надёжные ручки', 'Блокноты для настоящих мужчин', 'Предзаказ к празднику'], ('star', '0 0 24 24'), 'confetti', 14, sc_defender(), yd_defender(), 'star', 'star', 'fill', GEN_T, ('star', '0 0 24 24'), tag='С Днём защитника'),
    T('nooruz', 'Нооруз', 'Праздники', '21 марта: юрты, тюльпаны и солнце', ['Philosopher:wght@400;700', 'Nunito:wght@400;600;700;800'], 'Philosopher,Georgia,serif', 'Nunito,system-ui,sans-serif',
      dict(bg='#F4FBF1', bg2='#FFFFFF', sf='#FFFFFF', sf2='#E8F5E1', ink='#173F2B', mut='#5C7F69', line='#D3EACB', pri='#1F8A4C', acc='#FFC93C', onacc='#173F2B', hd='rgba(244,251,241,.92)', fx='#E8467C',
           tkbg='#1F8A4C', tkfg='#fff', hv='rgba(31,138,76,.28)', r='12px', rc='20px', tile='20px', hw='700', k='.85', em='#E8467C', yg='rgba(255,220,120,.22)'),
      ('Нооруз майрамыңыз', 'менен!', 'Весна, солнце и обновление. Красивая канцелярия к празднику: выберите и оставьте предзаказ.'),
      ['Нооруз майрамы', 'Весна идёт', 'Тюльпаны и солнце', 'Новые планы с новым годом', 'Предзаказ к празднику'], ('flower', '0 0 40 40'), 'petals', 24, sc_nooruz(), yd_nooruz(), 'flower', 'sun', 'fill', GEN_T, ('yurt', '0 0 120 80'), tag='Нооруз майрамы менен'),
    T('school', 'День знаний', 'Праздники', '1 сентября: тетрадка в клетку, карандаши, маркер', ['Caveat:wght@600;700', 'Nunito:wght@400;600;700;800'], 'Caveat,cursive', 'Nunito,system-ui,sans-serif',
      dict(bg='#F6F2E7', bg2='#FFFFFF', sf='#FFFFFF', sf2='#F0EAD7', ink='#1B2A5C', mut='#5F6B94', line='#DCE3F0', pri='#2740C9', acc='#FFD84D', onacc='#1B2A5C', hd='rgba(246,242,231,.94)', fx='#FF6B6B',
           bgimg='linear-gradient(#DCE6F2 1px,transparent 1px),linear-gradient(90deg,#DCE6F2 1px,transparent 1px)', tkbg='#FFD84D', tkfg='#1B2A5C', hv='rgba(39,64,201,.25)', r='10px', rc='12px', tile='12px', hw='700', k='1.05', em='#2740C9', yg='rgba(43,75,255,.08)'),
      ('Снова в школу!', 'Всё к 1 сентября', 'Тетради, ручки, пеналы и краски. Соберите всё к 1 сентября и оставьте предзаказ.'),
      ['С Днём знаний', 'Тетради в клетку и линейку', 'Карандаши на любой вкус', 'Всё к первому звонку', 'Предзаказ к 1 сентября'], ('star', '0 0 24 24'), 'confetti', 18, sc_school(), yd_school(), 'star', 'star', 'fill', GEN_T, ('book', '0 0 60 50'), tag='Удачного учебного года', css_key='school'),
    T('eid', 'Айт', 'Праздники', 'Ураза и Курман айт: изумруд, золото, полумесяц', ['Cormorant:wght@600;700', INTER], 'Cormorant,Georgia,serif', 'Inter,system-ui,sans-serif',
      dict(bg='#06231C', bg2='#0F4A39', sf='#0C3328', sf2='#124034', ink='#F4EBD0', mut='#A9C4B6', line='#1B5844', pri='#D9B44A', onpri='#1B1500', acc='#D9B44A', onacc='#1B1500', hd='rgba(6,35,28,.9)',
           inp='#06231C', fx='#F4E4A6', tkbg='#D9B44A', tkfg='#1B1500', hv='rgba(217,180,74,.35)', glow='rgba(217,180,74,.25)', r='6px', rc='10px', tile='10px', hw='700', k='.95', em='#D9B44A', yg='rgba(217,180,74,.18)'),
      ('Ийд мубарак!', 'Светлого праздника', 'Тёплых встреч и добрых подарков. Красивая канцелярия для близких: выберите и оставьте предзаказ.'),
      ['Светлого праздника', 'Добрых встреч', 'Подарки близким', 'Мир и благополучие', 'Предзаказ к празднику'], ('star', '0 0 24 24'), 'stars', 34, sc_eid(), yd_eid(), 'star', 'crescent', 'fill', GEN_T, ('lantern', '0 0 40 70'), tag='Ийд мубарак'),
    T('independence', 'День независимости', 'Праздники', '31 августа: красный и жёлтый, солнце-тундук', ['Oswald:wght@500;600;700', INTER], 'Oswald,sans-serif', 'Inter,system-ui,sans-serif',
      dict(bg='#FFF6E6', bg2='#FFFFFF', sf='#FFFFFF', sf2='#FBEAC8', ink='#3A0A10', mut='#8A5A4A', line='#F2DDB4', pri='#D3202F', acc='#FFD500', onacc='#3A0A10', hd='rgba(255,246,230,.94)', fx='#E8112D',
           tkbg='#E8112D', tkfg='#FFEF00', hv='rgba(211,32,47,.3)', r='4px', rc='6px', up='uppercase', ls='.1em', hup='uppercase', tile='6px', hw='700', k='.7', em='#D3202F', yg='rgba(232,17,45,.12)'),
      ('С Днём', 'независимости!', 'С праздником, Кыргызстан! Красивая канцелярия к торжеству: выберите и оставьте предзаказ.'),
      ['С Днём независимости', 'Ала-Тоо и солнце', 'Мирного неба', 'Гордость и единство', 'Предзаказ к празднику'], ('star', '0 0 24 24'), 'confetti', 26, sc_independence(), yd_independence(), 'star', 'flagsun', 'fill', GEN_T, ('flagsun', '0 0 100 100'),
      tag='С Днём независимости', deco_extra=bunting(['#E8112D', '#FFD500']), css_key='bunting'),
    T('sale', 'Распродажа', 'Праздники', 'Яркий жёлто-чёрный стиль для акций', ['Oswald:wght@500;600;700', INTER], 'Oswald,sans-serif', 'Inter,system-ui,sans-serif',
      dict(bg='#FFFBD6', bg2='#FFF39A', sf='#FFFFFF', sf2='#FFF3A8', ink='#111111', mut='#5A5A3A', line='#E8DB6A', pri='#111111', onpri='#FFE600', acc='#E3262F', onacc='#fff', hd='rgba(255,251,214,.94)', fx='#E3262F',
           tkbg='#111111', tkfg='#FFE600', hv='rgba(0,0,0,.3)', r='2px', rc='4px', up='uppercase', ls='.08em', hup='uppercase', tile='4px', hw='700', k='.72', em='#E3262F', yg='rgba(255,230,0,.2)'),
      ('Время', 'выгодных покупок', 'Подборка товаров по хорошим ценам. Выберите нужное и оставьте предзаказ.'),
      ['Выгодные предложения', 'Успейте оформить предзаказ', 'Хиты недели', 'Лучшие цены', 'Предзаказ сейчас'], ('tag', '0 0 60 40'), 'confetti', 40, sc_sale(), yd_sale(), 'tag', 'tag', 'fill', GEN_T, ('tag', '0 0 60 40'), tag='Выгодных покупок'),
]
THEMES = {t['id']: t for t in THEMES_LIST}
GROUPS = ['Базовые', 'Сезоны', 'Праздники']

# ============================ Дополнительный CSS тем ============================
CSS_EXTRA = {
    'halloween': '''
.sky{position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:35}
.fb{position:absolute;left:0;width:44px;height:22px;opacity:.8;animation:fly 28s linear infinite}
.fb.b1{top:16%}.fb.b2{top:38%;width:30px;height:15px;animation-duration:38s;animation-delay:-14s;opacity:.55}.fb.b3{top:62%;width:52px;height:26px;animation-duration:46s;animation-delay:-30s;opacity:.65}
@keyframes fly{0%{transform:translate(-12vw,0)}25%{transform:translate(24vw,-34px)}50%{transform:translate(54vw,22px)}75%{transform:translate(84vw,-28px)}100%{transform:translate(116vw,8px)}}
.deco{position:relative;height:0;z-index:30;pointer-events:none}
.drips{position:absolute;left:0;right:0;top:-1px;height:50px;background:url("data:image/svg+xml;utf8,__DRIP__") repeat-x}
.dang{position:absolute;top:0;pointer-events:auto;cursor:pointer;transform-origin:top center;animation:sw 4.5s ease-in-out infinite;display:flex;flex-direction:column;align-items:center}
.dang .th{display:block;width:1px;background:#8a8a8a}.dang svg{width:38px;height:38px;display:block}
@keyframes sw{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}
.pc .im::after{content:"";position:absolute;right:0;top:0;width:70px;height:70px;background:url("data:image/svg+xml;utf8,__WEB__") no-repeat 0 0/contain;transform:scaleX(-1);opacity:.5;pointer-events:none}
.hero h1 em{animation:glow 5s infinite}@keyframes glow{0%,90%,100%{opacity:1}93%{opacity:.55}96%{opacity:.9}}
.logo{animation:flick 7s infinite}@keyframes flick{0%,93%,100%{opacity:1}94%{opacity:.5}95%{opacity:1}97%{opacity:.35}98%{opacity:1}}
.eyes{position:absolute;width:34px;height:12px;animation:blink 6s infinite;transform-box:fill-box;transform-origin:center}
@keyframes blink{0%,94%,100%{transform:scaleY(1)}97%{transform:scaleY(.08)}}
.candles{display:flex;justify-content:center;align-items:flex-end;gap:14px;margin-bottom:18px}.candles .c{position:relative;width:26px}.candles svg{width:100%;display:block;fill:#e9e9e9;stroke:none}
.candles .f{position:absolute;left:0;top:-22px;width:26px;height:26px;fill:#fff;filter:drop-shadow(0 0 8px #fff)}
.fl{transform-box:fill-box;transform-origin:50% 100%;animation:fl .16s ease-in-out infinite alternate}@keyframes fl{to{transform:scale(.88,1.1)}}
.tile{border-bottom:0}
''',
    'newyear': '''
.deco{position:relative;height:0;z-index:30;pointer-events:none}
.garland{position:absolute;left:0;width:100%;top:0;height:54px}
.bulb{animation:bulb 1.6s ease-in-out infinite alternate;filter:drop-shadow(0 0 6px currentColor)}@keyframes bulb{from{opacity:.35}to{opacity:1}}
''',
    'bunting': '''
.deco{position:relative;height:0;z-index:30;pointer-events:none}
.bunt{position:absolute;left:0;width:100%;top:0;height:50px}
''',
    'school': '''
body{background-size:24px 24px,24px 24px,auto}
.hero h1{transform:rotate(-1.2deg)}
.hero h1 em{background:linear-gradient(transparent 58%,var(--acc) 58%,var(--acc) 90%,transparent 90%);padding:0 .12em}
''',
}


def theme_css(t):
    v = t['vars']
    names = {'onpri': 'on-pri', 'onacc': 'on-acc'}
    body = ';'.join(f'--{names.get(k, k)}:{val}' for k, val in v.items())
    ex = CSS_EXTRA.get(t.get('css_key', ''), '').replace('__DRIP__', DRIP_URI).replace('__WEB__', WEB_URI)
    return ':root{' + body + '}' + ex


def fonts_url(t):
    fams = []
    for f in t['fonts']:
        n, _, w = f.partition(':')
        fams.append('family=' + n.replace(' ', '+') + (':' + w if w else ''))
    return 'https://fonts.googleapis.com/css2?' + '&'.join(fams) + '&display=swap'


# ============================ Выбор темы ============================
RULES = [('newyear', (12, 20), (1, 10)), ('valentine', (2, 8), (2, 14)), ('defender', (2, 18), (2, 23)), ('women8', (3, 1), (3, 8)),
         ('nooruz', (3, 16), (3, 22)), ('independence', (8, 24), (8, 31)), ('school', (9, 1), (9, 10)), ('halloween', (10, 24), (11, 1))]


def today_kg():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=6)


def auto_theme(now=None):
    now = now or today_kg()
    md = (now.month, now.day)
    for tid, a, b in RULES:
        if (a <= b and a <= md <= b) or (a > b and (md >= a or md <= b)):
            return tid
    return {12: 'winter', 1: 'winter', 2: 'winter', 3: 'spring', 4: 'spring', 5: 'spring', 6: 'summer', 7: 'summer', 8: 'summer'}.get(now.month, 'autumn')


def resolve(chosen, auto, preview=None):
    if preview in THEMES:
        return THEMES[preview]
    if auto:
        return THEMES[auto_theme()]
    return THEMES.get(chosen) or THEMES['halloween']


_cache = {}


def pieces(t, custom_ticker='', fx_on=True):
    """Готовые куски HTML для шаблонов (кэшируются)."""
    key = (t['id'], custom_ticker, fx_on)
    if key in _cache:
        return _cache[key]
    phrases = [p.strip() for p in custom_ticker.splitlines() if p.strip()] or t['ticker']
    sym, vb = t['tsym']
    deco = ticker(phrases, sym, vb) + (t.get('deco') or '')
    if t.get('deco_extra'):
        deco += '<div class="deco">' + t['deco_extra'] + '</div>'
    ill = t['ill']
    ic = t.get('ill_cart', ill)
    ie = t.get('ill_empty', ill)

    def svg(pair):
        return Markup(f'<svg class="ill" viewBox="{pair[1]}"><use href="#i-{pair[0]}"/></svg>')

    okp = t.get('ok')
    ok = Markup(f'<svg viewBox="{okp[1]}"><use href="#i-{okp[0]}"/></svg>') if okp else Markup('<svg class="i" viewBox="0 0 24 24"><use href="#i-check"/></svg>')
    tile_icon = Markup(f'<svg class="tile-i {t["tile_kind"]}" viewBox="0 0 {"24 24" if t["icon"] in ("cross", "flake", "star", "heart", "leaf", "sparkle", "petal") else ("40 40" if t["icon"] == "flower" else ("100 100" if t["icon"] in ("sun", "crescent") else "60 40"))}"><use href="#i-{t["icon"]}"/></svg>')
    orn_vb = {'skull': '0 0 64 72', 'crescent': '0 0 100 100', 'sun': '0 0 100 100', 'flagsun': '0 0 100 100', 'tag': '0 0 60 40', 'flower': '0 0 40 40'}.get(t['orn'], '0 0 24 24')
    out = dict(
        fonts=fonts_url(t), css=Markup(theme_css(t)), sky=Markup(t.get('sky', '')), deco=Markup(deco), yard=Markup(t['yard'] or ''), scene=Markup(t['scene']),
        login=Markup(t.get('login') or f'<svg class="ill" style="width:84px" viewBox="{ill[1]}"><use href="#i-{ill[0]}"/></svg>'),
        ill_cart=svg(ic), ill_search=svg(ill), ill_empty=svg(ie), ill_err=svg(ie), ok=ok, tile=tile_icon,
        orn=Markup(f'<svg viewBox="{orn_vb}"><use href="#i-{t["orn"]}"/></svg>'), logo=Markup(t.get('logo') or '<b>М</b>'),
        favicon=_enc(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='{t['vars']['pri'] if t['vars']['pri'].startswith('#') else '#111'}'/><text x='16' y='23' font-size='20' font-weight='700' text-anchor='middle' fill='{t['vars']['onpri']}' font-family='sans-serif'>М</text></svg>"),
        fx_attrs=Markup(f'data-fx="{t["fx"] if fx_on else "none"}" data-fxn="{t["fxn"]}" data-fxc="{",".join(t.get("fxc", []))}"'),
        theme_color=t['vars']['bg'])
    _cache[key] = out
    return out


# палитры конфетти / лепестков
for _id, _c in {'defender': ['#C8A24A', '#2F5D3A', '#8FA58F'], 'independence': ['#E8112D', '#FFD500', '#D3202F'], 'school': ['#FF6B6B', '#E0A800', '#4D9BFF', '#58B947'],
                'sale': ['#E3262F', '#111111', '#E0C400'], 'valentine': ['#F06292', '#D6336C', '#FF8FAB'], 'women8': ['#E0A800', '#B07CE0', '#FF8FB1'],
                'spring': ['#FF9DB8', '#FFB3C7', '#F06292'], 'nooruz': ['#E8467C', '#E0A800', '#F48FB1'], 'autumn': ['#E07A1F', '#B5482A', '#E8B02D']}.items():
    THEMES[_id]['fxc'] = _c
