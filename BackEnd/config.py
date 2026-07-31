import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "leads_dedup.db"
EXPORT_PATH = BASE_DIR / "crm_import.json"

MUMBAI_BBOX = "18.89,72.77,19.27,73.00"

SOURCES = {
    "osm_established_businesses": {
        "type": "api",
        "url": "https://overpass-api.de/api/interpreter",
        "method": "POST",
        "check_robots": False,
        "payload": f'[out:json][timeout:25];(node["shop"](18.92,72.82,19.05,72.85);node["amenity"~"restaurant|dentist|clinic"](18.92,72.82,19.05,72.85););out body;',
        "service_tag": "webdesign"
    },
    "osm_established_fitness": {
        "type": "api",
        "url": "https://overpass-api.de/api/interpreter",
        "method": "POST",
        "check_robots": False,
        "payload": f'[out:json][timeout:25];(node["leisure"="fitness_centre"](18.92,72.82,19.05,72.85););out body;',
        "service_tag": "videoediting"
    },
    "mumbai_openings_rss": {
        "type": "rss",
        "url": "https://news.google.com/rss/search?q=Mumbai+(restaurant+OR+cafe+OR+boutique+OR+store+OR+clinic+OR+hotel)+(%22grand+opening%22+OR+%22now+open%22)&hl=en-IN&gl=IN&ceid=IN:en",
        "method": "GET",
        "check_robots": False,
        "delay_range": (1.0, 2.0),
        "service_tag": "webdesign"
    },
    "google_maps_mumbai_boutiques": {
        "type": "playwright",
        "query": "boutique clothing in Mumbai",
        "max_results": 30,
        "service_tag": "webdesign"
    }
}

ICP_SIGNALS = {
    "api_webdesign": {
        "signals": [
            {"signal": "established_no_website", "weight": 15, "heuristic": lambda tags: not tags.get("website") and not tags.get("contact:website")},
            {"signal": "http_only_legacy_site", "weight": 8, "heuristic": lambda tags: str(tags.get("website", "")).startswith("http://")},
        ],
        "disqualifiers": []
    },
    "api_videoediting": {
        "signals": [
            {"signal": "gaming_venue", "weight": 8, "heuristic": lambda tags: tags.get("club") in ["esport", "games"]},
            {"signal": "event_venue", "weight": 7, "heuristic": lambda tags: tags.get("amenity") in ["events_venue", "theatre"] or tags.get("leisure") in ["stadium", "sports_centre"]},
            {"signal": "fitness_gym_video_potential", "weight": 10, "heuristic": lambda tags: tags.get("leisure") == "fitness_centre"},
        ],
        "disqualifiers": []
    },
    "rss_webdesign": {
        "signals": [
            {"signal": "grand_opening", "weight": 8, "heuristic": lambda data: bool(re.search(r'\b(grand opening|now open|new location)\b', str(data.get("title", "")).lower()))},
        ],
        "disqualifiers": [
            {"signal": "recent_website_update", "heuristic": lambda data: bool(re.search(r'\bwebsite\s+(redesign|launch|relaunch|live|updated)\b', str(data.get("title", "")).lower()))}
        ]
    },
    "playwright_webdesign": {
        "signals": [
            {"signal": "broken_ssl", "weight": 10, "heuristic": lambda data: data.get("ssl_broken") is True},
            {"signal": "ancient_copyright", "weight": 8, "heuristic": lambda data: data.get("outdated_copyright") is True},
            {"signal": "high_decay", "weight": 5, "heuristic": lambda data: data.get("decay_score", 0) >= 15},
        ],
        "disqualifiers": []
    }
}

TUNABLES = {
    "min_score_threshold": 5,
    "max_retries": 3,
    "base_backoff_sec": 2
}