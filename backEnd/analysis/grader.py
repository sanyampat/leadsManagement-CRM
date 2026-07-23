import httpx
import time
from bs4 import BeautifulSoup
from backend.models.discovery import WebsiteAudit

async def audit_website(url: str) -> WebsiteAudit:
    start_time = time.time()
    audit = WebsiteAudit()
    
    if not url:
        return audit

    if url.startswith("https://"):
        audit.https = True

    async with httpx.AsyncClient(timeout=8.0, follow_redirects=True, verify=False) as client:
        try:
            response = await client.get(url)
            audit.loading_speed_ms = int((time.time() - start_time) * 1000)
            
            if response.status_code != 200:
                return audit

            soup = BeautifulSoup(response.text, "html.parser")
            
            # Mobile friendly check (viewport tag)
            viewport = soup.find("meta", attrs={"name": "viewport"})
            if viewport:
                audit.mobile_friendly = True
                audit.responsive = True
                
            # SEO Basics (<title>, <h1>, meta description)
            if soup.title and soup.find("h1") and soup.find("meta", attrs={"name": "description"}):
                audit.seo_basics = True
                
            # Contact Form or Mailto
            forms = soup.find_all("form")
            mailtos = soup.select('a[href^="mailto:"]')
            if forms or mailtos:
                audit.contact_form = True
                
            # Call to action detection
            cta_keywords = ["book", "contact", "order", "quote", "call", "schedule", "buy"]
            buttons = soup.find_all(["button", "a"])
            if any(any(kw in button.get_text().lower() for kw in cta_keywords) for button in buttons):
                audit.call_to_action = True
                
            # Modern Design heuristic (Flexbox/Grid stylesheets or semantic tags like <main>, <section>)
            if soup.find_all(["main", "section", "article", "nav"]):
                audit.modern_design = True
                
            # Calculate Overall Quality Score
            score = 0
            if audit.https: score += 10
            if audit.mobile_friendly: score += 20
            if audit.loading_speed_ms < 2000: score += 15
            if audit.seo_basics: score += 15
            if audit.contact_form: score += 20
            if audit.call_to_action: score += 10
            if audit.modern_design: score += 10
            
            audit.overall_quality_score = min(100, score)
            
        except Exception:
            pass # Return partial audit on failure
            
    return audit