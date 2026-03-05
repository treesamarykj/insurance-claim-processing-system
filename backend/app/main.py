from fastapi import FastAPI
from app.api.claim_routes import router as claim_router

app = FastAPI()

app.include_router(claim_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Health Claim Processing API is running"}