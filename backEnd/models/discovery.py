from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, List
from enum import Enum

class WebsiteStatus(str, Enum):
    EXISTS = "Has Official Website"
    MISSING = "No Website"
    BROKEN = "Website Broken"
    UNDER_CONSTRUCTION = "Under Construction"
    REDIRECTS = "Redirects Elsewhere"
    SOCIAL_ONLY = "Social Media Only"

class Socials(BaseModel):
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    linkedin: Optional[str] = None
    whatsapp: Optional[str] = None

class WebsiteAudit(BaseModel):
    https: bool = False
    mobile_friendly: bool = False
    responsive: bool = False
    loading_speed_ms: int = 0
    seo_basics: bool = False
    contact_form: bool = False
    modern_design: bool = False
    call_to_action: bool = False
    overall_quality_score: int = Field(default=0, ge=0, le=100)

class OpportunityAssessment(BaseModel):
    score: int = Field(default=0, ge=0, le=100)
    reason: str
    deficiencies: List[str] = []

class DiscoveredBusiness(BaseModel):
    id: str
    business_name: str
    category: str
    location: str
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    official_website: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    socials: Socials = Socials()
    rating: Optional[float] = None
    review_count: int = 0
    description: Optional[str] = None
    website_status: WebsiteStatus = WebsiteStatus.MISSING
    website_audit: Optional[WebsiteAudit] = None
    opportunity: Optional[OpportunityAssessment] = None
    crm_saved: bool = False
    crm_lead_id: Optional[str] = None

class SearchRequest(BaseModel):
    business_type: str
    location: str
    country: str
    max_results: int = Field(default=20, le=100)