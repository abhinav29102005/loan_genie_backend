from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from database.models import LoanOffer, Customer
from services import offer_service, customer_service

router = APIRouter(prefix="/offers", tags=["offers"])

class OfferRequest(BaseModel):
    required_amount: float

class OfferResponse(BaseModel):
    eligible_offers: List[LoanOffer]
    message: str

@router.get("/", response_model=List[LoanOffer])
def list_offers():
    return offer_service.get_all()

@router.get("/{offer_id}", response_model=LoanOffer)
def get_offer(offer_id: str):
    offer = offer_service.get_by_id(offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.post("/", response_model=LoanOffer, status_code=201)
def create_offer(offer: LoanOffer):
    existing = offer_service.get_by_id(offer.offer_id)
    if existing:
        raise HTTPException(status_code=400, detail="Offer ID already exists")
    return offer_service.create(offer)

@router.put("/{offer_id}", response_model=LoanOffer)
def update_offer(offer_id: str, updates: dict):
    updated = offer_service.update(offer_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Offer not found")
    return updated

@router.delete("/{offer_id}")
def delete_offer(offer_id: str):
    deleted = offer_service.delete(offer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Offer not found")
    return {"message": "Offer deleted successfully"}

@router.post("/eligible", response_model=OfferResponse)
def get_eligible_offers(request: OfferRequest):
    
    eligible = offer_service.get_eligible(request.required_amount)
    
    message = (
        f"Found {len(eligible)} eligible offer(s)" if eligible
        else f"No eligible offers found for amount ₹{request.required_amount:,.0f}"
    )
    
    return OfferResponse(
        eligible_offers=eligible,
        message=message
    )
    
#to do make these async