import os
import stripe
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

stripe_router = APIRouter()

@stripe_router.post("/create-checkout-session")
async def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'SEO Assistant Pro Plan',
                    },
                    'unit_amount': 5000,  # $50.00
                },
                'quantity': 1,
            }],
            success_url=os.getenv("SUCCESS_URL", "http://localhost:3000/success"),
            cancel_url=os.getenv("CANCEL_URL", "http://localhost:3000/checkout"),
        )
        return {"id": session.id}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)# Jouw bestaande Stripe checkout routes (niet gewijzigd)
