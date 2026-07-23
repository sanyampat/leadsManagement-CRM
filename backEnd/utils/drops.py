import re
from urllib.parse import urlparse

# Aggregators, review boards, and editorial platforms to permanently ignore
BLACKLISTED_DOMAINS = {
    "yelp.com", "tripadvisor.com", "foursquare.com", "zomato.com", "justdial.com",
    "medium.com", "forbes.com", "reddit.com", "quora.com", "timeout.com",
    "eater.com", "yellowpages.com", "bbb.org", "group-on.com", "hubspot.com"
}

# Regex patterns catching listicles, Top 10s, and blog posts
LISTICLE_PATTERNS = [
    r"/top-\d+-", r"/best-", r"/\d+-great-", r"/review/", r"/blog/",
    r"/article/", r"/news/", r"/list/", r"/top10", r"-vs-"
]

def is_unwanted_url(url: str) -> bool:
    if not url:
        return True
    
    try:
        parsed = urlparse(url.lower())
        domain = parsed.netloc.replace("www.", "")
        
        # Check against domain blacklist
        if any(domain.endswith(blacklisted) for blacklisted in BLACKLISTED_DOMAINS):
            return True
            
        # Check against URL path listicle patterns
        path = parsed.path
        if any(re.search(pattern, path) for pattern in LISTICLE_PATTERNS):
            return True
            
        return False
    except Exception:
        return True