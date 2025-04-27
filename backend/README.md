# SEO Assistant Backend

## Installatie
```bash
pip install -r requirements.txt
```

## Start server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Belangrijk
Maak een `.env` bestand met:
```
STRIPE_SECRET_KEY=your_secret_key
STRIPE_WEBHOOK_SECRET=your_webhook_secret
FRONTEND_URL=https://your-frontend-url.com
```