# Мир Канцелярии

Интернет-магазин канцтоваров · предзаказ · админка · долги · Telegram

## Railway

Start Command:
```
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1
```

Variables:
- ADMIN_PASSWORD
- TELEGRAM_BOT_TOKEN
- TELEGRAM_ADMIN_IDS
- SITE_PHONE
- DATA_DIR=/data (если Volume)
- DATABASE_URL (если PostgreSQL)

Админка: /admin
