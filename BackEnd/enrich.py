import re
import logging

logger = logging.getLogger(__name__)

def clean_phone_number(phone: str) -> str:
    """Standardizes Indian and international phone numbers."""
    if not phone:
        return None
    cleaned = re.sub(r'(?!^\+)\D', '', phone)
    if len(cleaned) == 10 and not cleaned.startswith('+'):
        cleaned = '+91' + cleaned
    return cleaned

def enrich_lead_record(lead: dict) -> dict:
    """Normalizes fields and sets contact readiness based on data presence."""
    if lead.get("phone"):
        lead["phone"] = clean_phone_number(lead["phone"])
    
    has_phone = bool(lead.get("phone"))
    has_email = bool(lead.get("email"))
    
    if has_phone or has_email:
        lead["contact_status"] = "ready"
    else:
        lead["contact_status"] = "needs_manual_lookup"
        
    return lead