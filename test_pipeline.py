import pytest
import os
from concurrent.futures import ThreadPoolExecutor
from dedup import DedupStore
from scorer import score_lead

@pytest.fixture
def temp_db():
    db_path = "test_leads_regression.db"
    store = DedupStore(db_path)
    yield store
    if os.path.exists(db_path):
        os.remove(db_path)

def test_dedup_fallback_key(temp_db):
    assert temp_db.is_new(None, None, "Sharma Cafe", "osm_mumbai") == True
    temp_db.mark_processed(None, None, "Sharma Cafe", "osm_mumbai")
    assert temp_db.is_new(None, None, "Sharma Cafe", "osm_mumbai") == False

def test_dedup_thread_safety(temp_db):
    def worker(i):
        temp_db.mark_processed(f"test{i}.com", None, f"Biz{i}", "test_src")
        return temp_db.is_new(f"test{i}.com", None, f"Biz{i}", "test_src")
        
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(worker, range(50)))
    
    assert all(res == False for res in results)

def test_scorer_silent_failure():
    score, signal = score_lead({"title": "Test"}, "invalid_service_key")
    assert score == 0
    assert signal == ""

def test_videoediting_strict_matching():
    false_positive = {"name": "Karena Fashion Boutique", "amenity": "shop"}
    score, _ = score_lead(false_positive, "api_videoediting")
    assert score == 0

    valid_lead = {"name": "Level Up Arena", "club": "esport"}
    score, sig = score_lead(valid_lead, "api_videoediting")
    assert score >= 8
    assert "gaming_venue" in sig

def test_rss_disqualifiers():
    disqualified = {"title": "Downtown Cafe Launches New Menu, Website Redesign Wins"}
    score, sig = score_lead(disqualified, "rss_webdesign")
    assert score == 0
    assert "disqualified" in sig

    valid_opening = {"title": "New Bakery Now Open in Andheri, Visit Our Website for Hours"}
    score, sig = score_lead(valid_opening, "rss_webdesign")
    assert score >= 8
    assert "grand_opening" in sig

def test_freshness_grader_signals():
    decayed_lead = {
        "name": "Old School Boutique",
        "website": "http://oldschoolboutique.in",
        "ssl_broken": True,
        "outdated_copyright": True,
        "decay_score": 18
    }
    score, sig = score_lead(decayed_lead, "playwright_webdesign")
    
    assert score >= 23 
    assert "broken_ssl" in sig
    assert "high_decay" in sig