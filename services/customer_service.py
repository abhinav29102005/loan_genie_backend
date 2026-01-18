from typing import Optional, List
from database.connection import customers_collection
from database.models import Customer

def get_all(skip: int = 0, limit: int = 100) -> List[Customer]:
    docs = customers_collection.find({}, {"_id": 0}).skip(skip).limit(limit)
    return [Customer(**doc) for doc in docs]

def get_by_id(customer_id: str) -> Optional[Customer]:
    doc = customers_collection.find_one({"customer_id": customer_id}, {"_id": 0})
    return Customer(**doc) if doc else None

def get_by_name(name: str) -> Optional[Customer]:
    doc = customers_collection.find_one(
        {"name": {"$regex": name, "$options": "i"}},
        {"_id": 0}
    )
    return Customer(**doc) if doc else None

def create(customer: Customer) -> Customer:
    customers_collection.insert_one(customer.model_dump())
    return customer

def update(customer_id: str, updates: dict) -> Optional[Customer]:
    result = customers_collection.update_one(
        {"customer_id": customer_id},
        {"$set": updates}
    )
    return get_by_id(customer_id) if result.modified_count > 0 else None

def delete(customer_id: str) -> bool:
    result = customers_collection.delete_one({"customer_id": customer_id})
    return result.deleted_count > 0