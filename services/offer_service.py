from typing import Optional, List
from database.connection import offers_collection
from database.models import LoanOffer

def get_all(skip: int = 0, limit: int = 100) -> List[LoanOffer]:
    docs = offers_collection.find({}, {"_id": 0}).skip(skip).limit(limit)
    return [LoanOffer(**doc) for doc in docs]

def get_by_id(offer_id: str) -> Optional[LoanOffer]:
    doc = offers_collection.find_one({"offer_id": offer_id}, {"_id": 0})
    return LoanOffer(**doc) if doc else None

def get_eligible(required_amount: float) -> List[LoanOffer]:
    query = {
        "min_amount": {"$lte": required_amount},
        "max_amount": {"$gte": required_amount}
    }
    docs = offers_collection.find(query, {"_id": 0})
    return [LoanOffer(**doc) for doc in docs]

def create(offer: LoanOffer) -> LoanOffer:
    offers_collection.insert_one(offer.model_dump())
    return offer

def update(offer_id: str, updates: dict) -> Optional[LoanOffer]:
    result = offers_collection.update_one(
        {"offer_id": offer_id},
        {"$set": updates}
    )
    return get_by_id(offer_id) if result.modified_count > 0 else None

def delete(offer_id: str) -> bool:
    result = offers_collection.delete_one({"offer_id": offer_id})
    return result.deleted_count > 0

## todo: make these async