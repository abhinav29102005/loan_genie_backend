from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    customer_id: str
    name: str
    age: int
    city: str
    monthly_income: float
    employment_status: str
    credit_score: int
    existing_loan_amount: float
    existing_loan_type: Optional[str]
    pre_approved_limit: float
    
class LoanOffer(BaseModel):
    offer_id: str
    loan_type: str
    min_amount: float
    max_amount: float
    interest_rate: float
    tenure_months: int
    processing_fee_percentage: float
    description: str