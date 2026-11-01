#!/usr/bin/env python3
"""Студийная обработка фото товаров.

Запуск:
    pip install pillow numpy opencv-python-headless          # обязательно
    pip install "rembg[cpu]"                                 # желательно: точнее вырезает фон
    python tools/studio.py photos_raw catalog                # розовый фон под сайт
    python tools/studio.py photos_raw catalog --bg white     # белый «каталожный» фон

Что делает с каждым фото:
  1. Поворот по EXIF, уменьшение до 1600 px.
  2. Вырезает товар (rembg, если установлен, иначе OpenCV GrabCut).
  3. Ставит на мягкий фон 1000x1000 с контактной тенью.
  4. Лёгкая коррекция света, цвета и резкости.
  5. Пишет catalog/catalog.csv, где нужно вписать названия и цены.

Если вырезка не удалась (товар слился с фоном), фото НЕ портится:
оно просто кадрируется в квадрат и улучшается, а в CSV ставится пометка «проверить».
"""
import argparse, csv, re, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageChops

try:
    import cv2
except ImportError:
    cv2 = None
try:
    from rembg import remove as rembg_remove
except Exception:
    rembg_remove = None

EXT = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
SIZE = 1000
PINK_CENTER, PINK_EDGE = (255, 247, 251), (255, 214, 231)


def load(path, long_side=1600):
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    im.thumbnail((long_side, long_side), Image.LANCZOS)
    return im


def cut_rembg(im):
    return rembg_remove(im).convert('RGBA')


def cut_grabcut(im):
    """Вырезка через GrabCut: рамка по краям считается фоном."""
    small = im.copy()
    small.thumbnail((700, 700))
    arr = cv2.cvtColor(np.array(small), cv2.COLOR_RGB2BGR)
    h, w = arr.shape[:2]
    mx, my = max(4, int(w * .03)), max(4, int(h * .03))
    mask = np.zeros((h, w), np.uint8)
    bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(arr, mask, (mx, my, w - 2 * mx, h - 2 * my), bgd, fgd, 6, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
    # оставляем самый крупный объект и закрываем дыры
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        m = np.where(lab == keep, 255, 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    alpha = Image.fromarray(m).resize(im.size, Image.LANCZOS)
    out = im.convert('RGBA')
    out.putalpha(alpha)
    return out


def refine_alpha(rgba):
    a = rgba.getchannel('A')
    a = a.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))  # убирает ореол по краю
    rgba.putalpha(a)
    return rgba


def cutout_ok(rgba):
    a = np.array(rgba.getchannel('A')) > 128
    frac = a.mean()
    return 0.03 < frac < 0.93


def backdrop(kind):
    if kind == 'white':
        return Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
    y, x = np.mgrid[0:SIZE, 0:SIZE].astype(np.float32)
    d = np.sqrt(((x - SIZE / 2) / (SIZE * .75)) ** 2 + ((y - SIZE * .45) / (SIZE * .75)) ** 2)
    d = np.clip(d, 0, 1)[..., None]
    c0, c1 = np.array(PINK_CENTER, np.float32), np.array(PINK_EDGE, np.float32)
    return Image.fromarray((c0 * (1 - d) + c1 * d).astype(np.uint8))


def compose(rgba, kind):
    bbox = rgba.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    box = int(SIZE * .76)
    rgba.thumbnail((box, box), Image.LANCZOS)
    bg = backdrop(kind).convert('RGBA')
    x = (SIZE - rgba.width) // 2
    y = int(SIZE * .47 - rgba.height / 2)
    y = max(int(SIZE * .08), min(y, SIZE - rgba.height - int(SIZE * .14)))
    # контактная тень на «полу»
    sh = Image.new('L', (SIZE, SIZE), 0)
    ell = Image.new('L', (SIZE, SIZE), 0)
    ew, eh = int(rgba.width * .8), max(14, int(rgba.height * .07))
    ex, ey = (SIZE - ew) // 2, y + rgba.height - eh // 2
    from PIL import ImageDraw
    ImageDraw.Draw(ell).ellipse((ex, ey, ex + ew, ey + eh), fill=120)
    sh = ell.filter(ImageFilter.GaussianBlur(14))
    # мягкая тень от силуэта
    sil = Image.new('L', (SIZE, SIZE), 0)
    sil.paste(rgba.getchannel('A').point(lambda v: int(v * .28)), (x + 8, y + 14))
    sil = sil.filter(ImageFilter.GaussianBlur(18))
    shadow = ImageChops.lighter(sh, sil)
    tint = (150, 60, 100) if kind != 'white' else (70, 70, 80)
    bg.paste(Image.new('RGBA', (SIZE, SIZE), tint + (255,)), (0, 0), shadow)
    bg.alpha_composite(rgba, (x, y))
    return bg.convert('RGB')


def enhance(im):
    im = ImageOps.autocontrast(im, cutoff=0.5)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    return ImageEnhance.Sharpness(im).enhance(1.25)


def fallback_square(im, kind):
    """Без вырезки: товар остаётся на своём фоне, кадр квадратный."""
    im = ImageOps.fit(im, (SIZE, SIZE), Image.LANCZOS, centering=(.5, .5))
    return im


def process(path, kind):
    im = load(path)
    note = ''
    rgba = None
    try:
        if rembg_remove:
            rgba = cut_rembg(im)
        elif cv2 is not None:
            rgba = cut_grabcut(im)
    except Exception as e:  # noqa
        note = f'ошибка вырезки: {e}'
    if rgba is not None:
        rgba = refine_alpha(rgba)
    if rgba is not None and cutout_ok(rgba):
        out = compose(rgba, kind)
    else:
        out = fallback_square(im, kind)
        note = note or 'проверить: фон не вырезан'
    return enhance(out), note


def guess_name(stem):
    s = re.sub(r'[_\-]+', ' ', stem)
    s = re.sub(r'\b(IMG|WA\d+|images?|original|photo)\b', '', s, flags=re.I)
    s = re.sub(r'[\d\W_]+', ' ', s).strip()
    return s.capitalize() if len(s) > 3 else ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst', nargs='?', default='catalog')
    ap.add_argument('--bg', choices=['pink', 'white'], default='pink')
    a = ap.parse_args()
    src, dst = Path(a.src), Path(a.dst)
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in src.iterdir() if p.suffix.lower() in EXT)
    if not files:
        sys.exit('В папке нет фото')
    print(f'Фото: {len(files)} · вырезка: {"rembg" if rembg_remove else "GrabCut (проще: pip install rembg[cpu])"}')
    csv_path = dst / 'catalog.csv'
    old = {}
    if csv_path.exists():   # не затираем уже вписанные названия и цены
        with open(csv_path, encoding='utf-8-sig') as f:
            old = {r['file']: r for r in csv.DictReader(f)}
    rows = []
    for i, p in enumerate(files, 1):
        out_name = f'p{i:03d}.jpg'
        try:
            img, note = process(p, a.bg)
        except Exception as e:
            print(f'[{i}/{len(files)}] {p.name}: ПРОПУЩЕНО ({e})')
            continue
        img.save(dst / out_name, quality=88, optimize=True, progressive=True)
        prev = old.get(out_name, {})
        rows.append({'file': out_name, 'name': prev.get('name') or guess_name(p.stem),
                     'price': prev.get('price', ''), 'category': prev.get('category', ''),
                     'note': note, 'source': p.name})
        print(f'[{i}/{len(files)}] {p.name} -> {out_name} {note}')
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['file', 'name', 'price', 'category', 'note', 'source'])
        w.writeheader(); w.writerows(rows)
    bad = sum(1 for r in rows if r['note'])
    print(f'\nГотово: {len(rows)} фото в {dst}/. Требуют проверки: {bad}. Заполните name/price/category в {csv_path}')


if __name__ == '__main__':
    main()
