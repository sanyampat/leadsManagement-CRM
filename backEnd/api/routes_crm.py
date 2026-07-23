from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database import repository
from backend.utils.dedup import check_duplicate

router = APIRouter(prefix="/api/crm-bridge", tags=["CRM Bridge"])

class SaveLeadResponse(BaseModel):
    success: bool
    crm_lead_id: str
    is_duplicate: bool
    message: str

@router.post("/save/{lead_id}", response_model=SaveLeadResponse)
def save_lead_to_crm(lead_id: str):
    lead = repository.get_discovered_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Discovered lead not found")

    # Check duplicates in Legacy CRM
    existing_crm_id = check_duplicate(repository.LEGACY_CRM_LEADS, lead.dict())
    
    if existing_crm_id:
        lead.crm_saved = True
        lead.crm_lead_id = existing_crm_id
        return SaveLeadResponse(
            success=True,
            crm_lead_id=existing_crm_id,
            is_duplicate=True,
            message="Lead already exists in CRM. Linked successfully."
        )

    # Insert into Legacy CRM
    new_crm_id = repository.add_to_legacy_crm(lead)
    lead.crm_saved = True
    lead.crm_lead_id = new_crm_id
    
    return SaveLeadResponse(
        success=True,
        crm_lead_id=new_crm_id,
        is_duplicate=False,
        message="Lead saved to CRM successfully."
    )