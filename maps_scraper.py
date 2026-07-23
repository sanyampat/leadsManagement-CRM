import logging
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

async def scrape_google_maps(search_query: str, max_results: int = 30):
    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
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
                import re
                phone_match = re.search(r'(\+91[\-\s]?\d{5}[\-\s]?\d{5})', text_content)
                if phone_match:
                    phone = phone_match.group(1)

                results.append({
                    "business_name": name,
                    "website": website_link,
                    "phone": phone,
                    "source": "google_maps_playwright",
                    "_raw": {"text_content": text_content}
                })
            except Exception as e:
                continue
                
        await browser.close()
        
    return results