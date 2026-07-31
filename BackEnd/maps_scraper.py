import asyncio
import logging
import random
import re
import requests
from playwright.async_api import async_playwright

try:
    from playwright_stealth import stealth_async
except ImportError:
    stealth_async = None

logger = logging.getLogger(__name__)

# Strict Indian Telecom Regex: Prevents matching telemetry IDs
INDIAN_PHONE_REGEX = r'((?:\+|0{0,2})91[\-\s]?[6-9]\d{4}[\-\s]?\d{5}|\b022[\-\s]?\d{8}\b|\b0\d{2,4}[\-\s]?\d{6,8}\b|\b[6-9]\d{9}\b)'

# Randomization pools to prevent fingerprint tracking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
]

VIEWPORTS = [
    {"width": 1920, "height": 1080},
    {"width": 2560, "height": 1440},
    {"width": 1440, "height": 900},
    {"width": 1366, "height": 768}
]

async def scrape_google_maps(search_query: str, max_results: int = 30):
    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport=random.choice(VIEWPORTS)
        )
        page = await context.new_page()
        if stealth_async:
            await stealth_async(page)
        
        url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
        logger.info(f"Navigating to {url}")
        
        await page.goto(url, timeout=60000)
        try:
            await page.wait_for_selector('div[role="feed"]', timeout=15000)
        except Exception:
            await browser.close()
            return results

        feed_element = page.locator('div[role="feed"]')
        
        while len(results) < max_results:
            await feed_element.evaluate("node => node.scrollBy(0, 1000)")
            await page.wait_for_timeout(1500)
            
            cards = await page.locator('div.Nv254').all()
            if len(cards) >= max_results:
                break
                
            if await page.locator("text=You've reached the end of the list").is_visible():
                break

        cards = await page.locator('div.Nv254').all()
        for card in cards[:max_results]:
            try:
                name = await card.locator('div.qBF1Pd').inner_text()
                
                website_link = None
                website_buttons = await card.locator('a[data-value="Website"]').all()
                if website_buttons:
                    website_link = await website_buttons[0].get_attribute("href")
                
                phone = None
                text_content = await card.inner_text()
                phone_match = re.search(INDIAN_PHONE_REGEX, text_content)
                if phone_match:
                    phone = phone_match.group(1).strip()

                results.append({
                    "business_name": name,
                    "website": website_link,
                    "phone": phone,
                    "source": "google_maps_playwright",
                    "_raw": {"text_content": text_content}
                })
            except Exception:
                continue
                
        await browser.close()
        
    return results


def _sync_extract_email_and_name(url):
    """Synchronous homepage crawler executed in a background thread pool."""
    if not url:
        return None, None
    try:
        if not url.startswith("http"):
            url = "https://" + url
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=6)
        
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
        
        junk = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', 'sentry', 'example.com', 'wix.com', 'domain.com', 'sentry.io', '2x.png']
        valid_emails = [e for e in set(emails) if not any(j in e.lower() for j in junk)]
        
        email = valid_emails[0] if valid_emails else None
        contact_name = None

        if email:
            user_part = email.split("@")[0]
            if "." in user_part or "_" in user_part or len(user_part) > 3:
                clean_user = re.sub(r'[._]', ' ', user_part).title()
                generic_words = ['Info', 'Contact', 'Admin', 'Hello', 'Support', 'Sales', 'Team', 'Help', 'Office', 'General', 'Enquiry', 'Reservations', 'Orders', 'Customercare', 'Personaldata']
                if not any(w in clean_user for w in generic_words):
                    contact_name = clean_user

        return email, contact_name
    except Exception:
        return None, None


async def _enrich_single_lead(lead, browser, semaphore, location="Mumbai"):
    """Worker function that enriches a single lead inside the concurrent semaphore pool."""
    async with semaphore:
        try:
            clean_search_name = re.sub(r'(?i)\b(now open|celebrates the grand opening of|debuts in india|marks expansion|is now open|opens in mumbai|arrives in hyderabad|flagship store|in mumbai|at bkc)\b.*', '', lead['business_name']).strip()
            if not clean_search_name or len(clean_search_name) < 3:
                clean_search_name = lead['business_name'][:30]

            query = f"{clean_search_name} {location}".replace(' ', '+')
            url = f"https://www.google.com/maps/search/{query}"
            logger.info(f"Enriching: {clean_search_name}")
            
            # Create a dedicated, randomized context for this tab
            context = await browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                viewport=random.choice(VIEWPORTS)
            )
            page = await context.new_page()
            if stealth_async:
                await stealth_async(page)
            
            await page.goto(url, timeout=25000)
            await page.wait_for_timeout(random.uniform(1500, 2500))

            # Grab Official Website
            if not lead.get("website"):
                website_buttons = await page.locator('a[data-value="Website"], a[data-item-id="authority"], a[aria-label^="Website:"]').all()
                if website_buttons:
                    lead["website"] = await website_buttons[0].get_attribute("href")

            # Grab Phone Number from visible rendered body text only
            if not lead.get("phone"):
                text_content = await page.locator("body").inner_text()
                phone_match = re.search(INDIAN_PHONE_REGEX, text_content)
                if phone_match:
                    lead["phone"] = phone_match.group(1).strip()

            await context.close()

            # Grab Email & Infer Name without blocking the async event loop
            if lead.get("website") and not lead.get("email"):
                email, inferred_name = await asyncio.to_thread(_sync_extract_email_and_name, lead["website"])
                if email:
                    lead["email"] = email
                if inferred_name and not lead.get("contact_name"):
                    lead["contact_name"] = inferred_name

            # Upgrade readiness status
            if lead.get("phone") or lead.get("email"):
                lead["contact_status"] = "ready"
                
        except Exception as e:
            logger.debug(f"Could not enrich {lead['business_name']}: {e}")
            
        return lead


async def enrich_leads_batch(leads, location="Mumbai"):
    """Spawns up to 8 concurrent Chromium tabs to process missing lead contacts simultaneously."""
    leads_to_enrich = [l for l in leads if not l.get("phone") or not l.get("website")]
    if not leads_to_enrich:
        return leads

    logger.info(f"Starting CONCURRENT contact enrichment for {len(leads_to_enrich)} leads (Max Concurrency: 8 tabs)...")
    
    # 8 concurrent tabs will use ~2-3 GB of your 64 GB RAM
    semaphore = asyncio.Semaphore(8)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Schedule all enrichment tasks concurrently
        tasks = [
            _enrich_single_lead(lead, browser, semaphore, location)
            for lead in leads_to_enrich
        ]
        
        await asyncio.gather(*tasks)
        await browser.close()
        
    return leads