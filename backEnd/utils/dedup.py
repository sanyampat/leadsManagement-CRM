import re
from typing import Optional, Dict, Any

def normalize_phone(phone: Optional[str]) -> str:
    if not phone:
        return ""
    # Strip all non-numeric characters except leading '+'
    return re.sub(r"(?!^\+)\D", "", phone)

def normalize_domain(url: Optional[str]) -> str:
    if not url:
        return ""
    url = url.lower().replace("http://", "").replace("https://", "").replace("www.", "")
    return url.split("/")[0].strip()

def check_duplicate(existing_leads: list[Dict[str, Any]], new_business: Dict[str, Any]) -> Optional[str]:
    """
    Checks if a discovered business already exists in the legacy CRM.
    Returns the existing CRM Lead ID if a match is found, otherwise None.
    """
    new_phone = normalize_phone(new_business.get("phone_number"))
    new_domain = normalize_domain(new_business.get("official_website"))
    new_name = new_business.get("business_name", "").lower().strip()

    for lead in existing_leads:
        lead_phone = normalize_phone(lead.get("phone"))
        lead_domain = normalize_domain(lead.get("website"))
        lead_name = lead.get("company_name", "").lower().strip()

        # Match by Phone
        if new_phone and lead_phone and new_phone == lead_phone:
            return str(lead["id"])
            
        # Match by Website Domain
        if new_domain and lead_domain and new_domain == lead_domain:
            return str(lead["id"])
            
        # Exact Name + City Match
        if new_name == lead_name and new_name != "":
            return str(lead["id"])

    return None