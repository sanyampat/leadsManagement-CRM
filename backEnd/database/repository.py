from typing import List, Dict, Any, Optional
import uuid
from backend.models.discovery import DiscoveredBusiness

# In-memory storage representing database tables
SEARCH_HISTORY_DB: List[Dict[str, Any]] = []
DISCOVERED_LEADS_STORE: Dict[str, DiscoveredBusiness] = {}
LEGACY_CRM_LEADS: List[Dict[str, Any]] = [
    # Mocking legacy database records
    {"id": "crm-101", "company_name": "Apex Fitness", "phone": "+919876543210", "website": "apexfitness.com"}
]

def save_search_history(query: Dict[str, str], count: int):
    SEARCH_HISTORY_DB.insert(0, {
        "id": str(uuid.uuid4()),
        "query": f"{query['business_type']} {query['location']}",
        "params": query,
        "results_count": count
    })

def get_search_history() -> List[Dict[str, Any]]:
    return SEARCH_HISTORY_DB[:15]

def store_discovered_leads(leads: List[DiscoveredBusiness]):
    for lead in leads:
        DISCOVERED_LEADS_STORE[lead.id] = lead

def get_discovered_lead(lead_id: str) -> Optional[DiscoveredBusiness]:
    return DISCOVERED_LEADS_STORE.get(lead_id)

def add_to_legacy_crm(lead: DiscoveredBusiness) -> str:
    crm_id = f"crm-{uuid.uuid4().hex[:6]}"
    LEGACY_CRM_LEADS.append({
        "id": crm_id,
        "company_name": lead.business_name,
        "category": lead.category,
        "phone": lead.phone_number,
        "email": lead.email,
        "website": lead.official_website,
        "opportunity_score": lead.opportunity.score if lead.opportunity else 0,
        "ai_reason": lead.opportunity.reason if lead.opportunity else "",
        "source": "AI Lead Discovery"
    })
    return crm_id