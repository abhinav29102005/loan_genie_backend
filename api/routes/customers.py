from fastapi import APIRouter, HTTPException
from typing import List
from database.models import Customer
from services import customer_service

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/", response_model=List[Customer])
def list_customers():
    return customer_service.get_all()

@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: str):
    customer = customer_service.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/", response_model=Customer, status_code=201)
def create_customer(customer: Customer):
    existing = customer_service.get_by_id(customer.customer_id)
    if existing:
        raise HTTPException(status_code=400, detail="Customer ID already exists")
    return customer_service.create(customer)

@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: str, updates: dict):
    updated = customer_service.update(customer_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated

@router.delete("/{customer_id}")
def delete_customer(customer_id: str):
    deleted = customer_service.delete(customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}