import re
import time
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def grade_website_freshness(url: str, timeout: int = 10):
    signals = {
        "ssl_broken": False,
        "unreachable": False,
        "slow_load": False,
        "outdated_copyright": False,
        "copyright_year": None,
        "decay_score": 0
    }
    
    if not url.startswith("http"):
        url = "https://" + url

    start_time = time.time()
    try:
        response = requests.get(url, timeout=timeout)
    except requests.exceptions.SSLError:
        signals["ssl_broken"] = True
        signals["decay_score"] += 15
        try:
            url = url.replace("https://", "http://")
            response = requests.get(url, timeout=timeout)
        except Exception:
            signals["unreachable"] = True
            signals["decay_score"] += 20
            return signals
    except requests.exceptions.RequestException:
        signals["unreachable"] = True
        signals["decay_score"] += 20
        return signals

    load_time = time.time() - start_time
    if load_time > 5.0:
        signals["slow_load"] = True
        signals["decay_score"] += 5

    soup = BeautifulSoup(response.text, 'html.parser')
    text_content = soup.get_text()

    current_year = datetime.now().year
    years_found = [int(y) for y in re.findall(r'(?:©|Copyright|&copy;)\s*(?:[A-Za-z\s,-]+)?\s*(20\d{2})', text_content, re.IGNORECASE)]
    
    if years_found:
        max_year = max(years_found)
        signals["copyright_year"] = max_year
        if max_year < current_year - 1:
            signals["outdated_copyright"] = True
            signals["decay_score"] += (current_year - max_year) * 3

    return signals