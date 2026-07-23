from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.models.discovery import SearchRequest, DiscoveredBusiness, WebsiteStatus
from backend.scrapers.maps_scraper import search_local_businesses
from backend.analysis.enrich import analyze_website_status
from backend.analysis.grader import audit_website
from backend.analysis.scorer import calculate_opportunity
from backend.database import repository

router = APIRouter(prefix="/api/discovery", tags=["Discovery"])

@router.post("/search", response_model=List[DiscoveredBusiness])
async def discover_businesses(request: SearchRequest):
    # 1. Discover local physical entities
    raw_leads = await search_local_businesses(
        request.business_type, request.location, request.country, request.max_results
    )
    
    enriched_leads = []
    for lead in raw_leads:
        # 2. Check website availability & extract socials
        status, final_url, socials = await analyze_website_status(lead.official_website)
        lead.website_status = status
        lead.official_website = final_url
        if socials.instagram or socials.facebook or socials.linkedin:
            lead.socials = socials

        # 3. Audit website if present
        if status == WebsiteStatus.EXISTS and final_url:
            lead.website_audit = await audit_website(final_url)
            
        # 4. Score Opportunity
        lead.opportunity = calculate_opportunity(lead)
        enriched_leads.append(lead)

    repository.store_discovered_leads(enriched_leads)
    repository.save_search_history(request.dict(), len(enriched_leads))
    return enriched_leads

@router.get("/history")
def fetch_search_history():
    return repository.get_search_history()

@router.get("/business/{lead_id}", response_model=DiscoveredBusiness)
def fetch_business_profile(lead_id: str):
    lead = repository.get_discovered_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Business not found")
    return lead