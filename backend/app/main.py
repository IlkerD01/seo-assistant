from fastapi import FastAPI
from .stripe_routes import stripe_router

app = FastAPI()

app.include_router(stripe_router)

@app.get("/")
def read_root():
    return {"message": "SEO Assistant Backend Running"}# FastAPI app include router admin_routes
