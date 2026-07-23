import httpx
import time
from backend.models.discovery import WebsiteStatus, Socials

SOCIAL_DOMAINS = ["instagram.com", "facebook.com", "linkedin.com", "wa.me", "whatsapp.com"]

async def analyze_website_status(url: Optional[str]) -> tuple[WebsiteStatus, Optional[str], Socials]:
    socials = Socials()
    if not url:
        return WebsiteStatus.MISSING, None, socials
        
    if any(domain in url.lower() for domain in SOCIAL_DOMAINS):
        if "instagram.com" in url: socials.instagram = url
        if "facebook.com" in url: socials.facebook = url
        if "linkedin.com" in url: socials.linkedin = url
        return WebsiteStatus.SOCIAL_ONLY, None, socials

    # Add scheme if missing
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    async with httpx.AsyncClient(timeout=6.0, follow_redirects=True, verify=False) as client:
        try:
            response = await client.get(url)
            final_url = str(response.url)
            
            # Check redirects to marketplaces/socials
            if any(domain in final_url.lower() for domain in SOCIAL_DOMAINS):
                return WebsiteStatus.REDIRECTS, final_url, socials
                
            if response.status_code >= 400:
                return WebsiteStatus.BROKEN, url, socials
                
            text_lower = response.text.lower()
            if any(term in text_lower for term in ["under construction", "coming soon", "domain for sale"]):
                return WebsiteStatus.UNDER_CONSTRUCTION, final_url, socials
                
            return WebsiteStatus.EXISTS, final_url, socials
        except httpx.RequestError:
            return WebsiteStatus.BROKEN, url, socials