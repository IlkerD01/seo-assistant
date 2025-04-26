from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import stripe
import os
import jwt
import datetime

# Load environment variables
load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")

stripe.api_key = STRIPE_SECRET_KEY

# Maak FastAPI app
app = FastAPI()

# CORS Middleware correct instellen
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL] if FRONTEND_URL else ["*"],  # Veiliger
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

# In-memory API Key database
api_keys_db = []

# Request models
class LoginRequest(BaseModel):
    username: str
    password: str

class APIKeyRequest(BaseModel):
    api_key: str

# JWT Authentication
def authenticate(token: str = Depends(lambda: None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        if payload.get("username") != ADMIN_USERNAME:
            raise HTTPException(status_code=403, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

# Routes
@app.get("/")
async def root():
    return {"message": "API is running 🚀"}

@app.post("/admin/login")
async def login(request: LoginRequest):
    if request.username == ADMIN_USERNAME and request.password == ADMIN_PASSWORD:
        token = jwt.encode(
            {
                "username": request.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
            },
            JWT_SECRET,
            algorithm="HS256"
        )
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/admin/api-keys")
async def list_api_keys(token: str = Depends(authenticate)):
    return {"api_keys": api_keys_db}

@app.post("/admin/api-keys")
async def add_api_key(request: APIKeyRequest, token: str = Depends(authenticate)):
    api_keys_db.append(request.api_key)
    return {"message": "API key added"}

@app.post("/create-checkout-session")
async def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Premium API Access",
                    },
                    "unit_amount": 5000,
                },
                "quantity": 1,
            }],
            success_url=f"{FRONTEND_URL}/success",
            cancel_url=f"{FRONTEND_URL}/cancelled",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"Payment successful! Session ID: {session['id']}")

    return {"status": "success"}

