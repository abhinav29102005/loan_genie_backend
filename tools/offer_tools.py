from crewai.tools import tool
import requests
from typing import Dict, Any
import json

API_BASE_URL = "http://localhost:8000/offers"

@tool("Get All Loan Offers")
def get_all_loan_offers(params: str = "") -> str:
    """
    Use this tool to fetch ALL available loan offers from the system.
    This shows the complete catalog of loan products. No parameters needed.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        response.raise_for_status()
        
        offers = response.json()
        
        if not offers or len(offers) == 0:
            return "No loan offers available at the moment."
        
        result = f"Available Loan Offers (Total: {len(offers)}):\n\n"
        for i, offer in enumerate(offers, 1):
            result += f"Offer {i}:\n"
            result += f"  - Offer ID: {offer.get('offer_id', 'N/A')}\n"
            result += f"  - Loan Type: {offer.get('loan_type', 'N/A')}\n"
            result += f"  - Interest Rate: {offer.get('interest_rate', 'N/A')}%\n"
            result += f"  - Max Amount: ₹{offer.get('max_amount', 0):,.0f}\n"
            result += f"  - Min Amount: ₹{offer.get('min_amount', 0):,.0f}\n"
            result += f"  - Term: {offer.get('term_months', 'N/A')} months\n"
            
            if 'processing_fee' in offer:
                result += f"  - Processing Fee: {offer.get('processing_fee', 'N/A')}%\n"
            if 'description' in offer:
                result += f"  - Description: {offer.get('description', 'N/A')}\n"
            
            result += "\n"
        
        return result
            
    except requests.RequestException as e:
        return f"Error fetching loan offers: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


@tool("Get Eligible Offers")
def get_eligible_offers(amount: str) -> str:
    """
    Use this tool to find loan offers eligible for a specific amount.
    Pass the required loan amount as a parameter (e.g., "500000" for ₹5 lakhs).
    Returns only offers that can accommodate the requested amount with EMI calculations.
    
    Args:
        amount: Required loan amount as string (e.g., "500000")
    """
    try:
        required_amount = float(amount)
        
        response = requests.post(
            f"{API_BASE_URL}/eligible",
            json={"required_amount": required_amount},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        eligible_offers = data.get("eligible_offers", [])
        message = data.get("message", "")
        
        if not eligible_offers or len(eligible_offers) == 0:
            return f"{message}\n\nNo offers match the requested amount of ₹{required_amount:,.0f}"
        
        result = f"{message}\n\n"
        result += f"Eligible Loan Offers for ₹{required_amount:,.0f}:\n\n"
        
        for i, offer in enumerate(eligible_offers, 1):
            result += f"Offer {i}:\n"
            result += f"  - Offer ID: {offer.get('offer_id', 'N/A')}\n"
            result += f"  - Loan Type: {offer.get('loan_type', 'N/A')}\n"
            result += f"  - Interest Rate: {offer.get('interest_rate', 'N/A')}%\n"
            result += f"  - Max Amount: ₹{offer.get('max_amount', 0):,.0f}\n"
            result += f"  - Min Amount: ₹{offer.get('min_amount', 0):,.0f}\n"
            result += f"  - Term: {offer.get('term_months', 'N/A')} months\n"
            
            if 'interest_rate' in offer and 'term_months' in offer:
                rate = offer['interest_rate']
                months = offer['term_months']
                if rate and months:
                    monthly_rate = rate / (12 * 100)
                    emi = required_amount * monthly_rate * (1 + monthly_rate)**months / ((1 + monthly_rate)**months - 1)
                    result += f"  - Approx. EMI: ₹{emi:,.0f}/month\n"
            
            if 'processing_fee' in offer:
                result += f"  - Processing Fee: {offer.get('processing_fee', 'N/A')}%\n"
            
            result += "\n"
        
        return result
            
    except ValueError:
        return f"Invalid amount format. Please provide a numeric value."
    except requests.RequestException as e:
        return f"Error fetching eligible offers: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


@tool("Get Offer Details")
def get_offer_details(offer_id: str) -> str:
    """
    Use this tool to get detailed information about a specific loan offer.
    Pass the offer_id as parameter. Useful when customer asks about a particular offer.
    
    Args:
        offer_id: The ID of the loan offer
    """
    try:
        response = requests.get(f"{API_BASE_URL}/{offer_id}", timeout=10)
        response.raise_for_status()
        
        offer = response.json()
        
        result = f"Loan Offer Details:\n\n"
        result += f"Offer ID: {offer.get('offer_id', 'N/A')}\n"
        result += f"Loan Type: {offer.get('loan_type', 'N/A')}\n"
        result += f"Interest Rate: {offer.get('interest_rate', 'N/A')}%\n"
        result += f"Amount Range: ₹{offer.get('min_amount', 0):,.0f} - ₹{offer.get('max_amount', 0):,.0f}\n"
        result += f"Term: {offer.get('term_months', 'N/A')} months\n"
        
        if 'processing_fee' in offer:
            result += f"Processing Fee: {offer.get('processing_fee', 'N/A')}%\n"
        if 'description' in offer:
            result += f"Description: {offer.get('description', 'N/A')}\n"
        
        return result
            
    except requests.HTTPException as e:
        if e.response.status_code == 404:
            return f"Offer with ID '{offer_id}' not found."
        return f"Error fetching offer details: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"