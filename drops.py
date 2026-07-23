import time
import random
import logging
from urllib import robotparser
from urllib.parse import urlparse
import requests

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
]

_robots_cache = {}

def is_scraping_permitted(url, user_agent):
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    robots_url = f"{base_url}/robots.txt"
    
    if base_url not in _robots_cache:
        rp = robotparser.RobotFileParser()
        rp.set_url(robots_url)
        try:
            r = requests.get(robots_url, timeout=5, headers={"User-Agent": user_agent})
            if r.status_code == 200:
                rp.parse(r.text.splitlines())
            _robots_cache[base_url] = rp
        except requests.RequestException as e:
            logger.debug(f"robots.txt fetch failed for {base_url} (defaulting to allow): {e}")
            _robots_cache[base_url] = None
            
    rp = _robots_cache[base_url]
    return rp.can_fetch(user_agent, url) if rp else True

def _get(url, retries=3, method="GET", check_robots=True, delay_range=(0, 0), **kwargs):
    ua = random.choice(USER_AGENTS)
    
    if check_robots and method.upper() == "GET" and not is_scraping_permitted(url, ua):
        logger.warning(f"robots.txt blocked scraping for {url}")
        return None

    if delay_range != (0, 0):
        time.sleep(random.uniform(*delay_range))

    session = requests.Session()
    session.headers.update({
        "User-Agent": ua,
        "Accept": "application/json, text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.5"
    })
    
    for attempt in range(retries):
        try:
            response = session.request(method, url, timeout=15, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt == retries - 1:
                logger.error(f"HTTP {method} failed for {url}: {e}")
                return None
            time.sleep((2 ** attempt) + random.uniform(0.1, 1.0))