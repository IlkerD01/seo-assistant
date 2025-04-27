# SEO Assistant Backend

## Installatie

```bash
pip install -r requirements.txt
```

## Starten

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## .env Instellen

Maak een `.env` bestand met:
```
STRIPE_SECRET_KEY=your_secret_key_here
SUCCESS_URL=https://yourfrontend.com/success
CANCEL_URL=https://yourfrontend.com/checkout
```