from fastapi import FastAPI
from api.routes import customers,offers

app = FastAPI(title="Loan API", version="1.0.0")

app.include_router(customers.router)
app.include_router(offers.router)

@app.get("/")
def root():
    return {"message": "Welcome to Loan API", "status": "active"}