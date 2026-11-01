"""Автозагрузка студийных фото в каталог.

Папка catalog/ лежит в репозитории (фото + catalog.csv), поэтому каталог
восстанавливается при каждом запуске, даже если Railway стёр shop.db.
Уже добавленные товары (по имени файла) не дублируются.
"""
import csv, os
from flask import send_from_directory, abort

CATALOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'catalog')


def seed(app, db, Product, Category):
    if 'catalog_img' not in app.view_functions:
        @app.route('/catalog-img/<path:fname>', endpoint='catalog_img')
        def catalog_img(fname):
            if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                abort(404)
            resp = send_from_directory(CATALOG_DIR, fname)
            resp.headers['Cache-Control'] = 'public, max-age=604800'
            return resp

    csv_path = os.path.join(CATALOG_DIR, 'catalog.csv')
    if not os.path.exists(csv_path):
        return
    added = 0
    with app.app_context():
        existing_urls = {url for (url,) in db.session.query(Product.image_url).all() if url}
        with open(csv_path, encoding='utf-8-sig', newline='') as f:
            for r in csv.DictReader(f):
                fname, name = (r.get('file') or '').strip(), (r.get('name') or '').strip()
                if (not fname or os.path.basename(fname) != fname or
                        not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) or
                        not name or not os.path.isfile(os.path.join(CATALOG_DIR, fname))):
                    continue
                url = f'/catalog-img/{fname}'
                if url in existing_urls:
                    continue
                try:
                    price = float((r.get('price') or '0').replace(',', '.').replace(' ', ''))
                except ValueError:
                    price = 0.0
                cat = None
                cname = (r.get('category') or '').strip()
                if cname:
                    cat = Category.query.filter_by(name=cname).first()
                    if not cat:
                        cat = Category(name=cname)
                        db.session.add(cat)
                        db.session.flush()
                description = (r.get('description') or '').strip()
                db.session.add(Product(name=name[:200], description=description,
                                       image_url=url, category_id=cat.id if cat else None))
                existing_urls.add(url)
                added += 1
        db.session.commit()
    if added:
        print(f'[catalog_seed] добавлено товаров: {added}')
