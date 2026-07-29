import json
import uuid
import logging
import argparse
import asyncio
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

import config
from dedup import DedupStore
from scorer import score_lead
from drops import _get 
from maps_scraper import scrape_google_maps, enrich_leads_batch
from grader import grade_website_freshness
from enrich import enrich_lead_record

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def parse_osm_node(node, source_name, service_tag):
    tags = node.get("tags", {})
    return {
        "business_name": tags.get("name", "Unknown Business"),
        "contact_name": None,
        "email": tags.get("email", tags.get("contact:email")),
        "phone": tags.get("phone", tags.get("contact:phone")),
        "website": tags.get("website", tags.get("contact:website")),
        "service": service_tag,
        "source": source_name,
        "_raw": tags 
    }

def build_crm_lead(parsed, signal, score):
    base_lead = {
        "id": str(uuid.uuid4()),
        "business_name": parsed["business_name"],
        "contact_name": parsed.get("contact_name"),
        "email": parsed.get("email"),
        "phone": parsed.get("phone"),
        "website": parsed.get("website"),
        "service": parsed["service"],
        "signal": signal,
        "score": score,
        "status": "new",
        "source": parsed["source"],
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "notes": parsed.get("notes", "")
    }
    return enrich_lead_record(base_lead)

def process_source(source_name, source_config, dedup_store):
    logger.info(f"Fetching source: {source_name}")
    stats = {"found": 0, "new": 0, "duplicate": 0}
    valid_leads = []
    
    if source_config["type"] == "playwright":
        raw_leads = asyncio.run(
            scrape_google_maps(source_config["query"], source_config["max_results"])
        )
        stats["found"] = len(raw_leads)
        
        for parsed in raw_leads:
            parsed["service"] = source_config["service_tag"]
            
            if not dedup_store.is_new(parsed.get("website"), parsed.get("phone"), parsed.get("business_name"), source_name):
                stats["duplicate"] += 1
                continue
                
            if parsed.get("website"):
                freshness_signals = grade_website_freshness(parsed["website"])
                parsed["_raw"].update(freshness_signals)
            
            score, signal = score_lead(parsed["_raw"], f"playwright_{parsed['service']}")
            if score < config.TUNABLES["min_score_threshold"]:
                continue
                
            crm_lead = build_crm_lead(parsed, signal, score)
            valid_leads.append(crm_lead)
            stats["new"] += 1
            
        return valid_leads, stats

    response = _get(
        source_config["url"], 
        method=source_config["method"], 
        data=source_config.get("payload"),
        check_robots=source_config.get("check_robots", True),
        delay_range=source_config.get("delay_range", (0, 0))
    )
    
    if not response:
        return valid_leads, stats
        
    if source_config["type"] == "api":
        raw_nodes = response.json().get("elements", [])
        stats["found"] = len(raw_nodes)
        
        for node in raw_nodes:
            parsed = parse_osm_node(node, source_name, source_config["service_tag"])
            
            if not dedup_store.is_new(parsed["website"], parsed["phone"], parsed["business_name"], parsed["source"]):
                stats["duplicate"] += 1
                continue
                
            score, signal = score_lead(parsed["_raw"], f"api_{parsed['service']}")
            if score < config.TUNABLES["min_score_threshold"]:
                continue
                
            crm_lead = build_crm_lead(parsed, signal, score)
            valid_leads.append(crm_lead)
            stats["new"] += 1
            
    elif source_config["type"] == "rss":
        try:
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            stats["found"] = len(items)
            
            for item in items:
                raw_title = item.findtext("title", "")
                link = item.findtext("link", "")
                desc = item.findtext("description", "")
                
                clean_name = raw_title.split(" - ")[0].split(" | ")[0].strip()
                if len(clean_name) > 60:
                    clean_name = clean_name[:57] + "..."
                
                parsed = {
                    "business_name": clean_name,
                    "contact_name": None,
                    "email": None,
                    "phone": None,
                    "website": None, 
                    "service": source_config["service_tag"],
                    "source": source_name,
                    "_raw": {"title": raw_title, "desc": desc, "link": link},
                    "notes": f"Source article: {link}"
                }
                
                if not dedup_store.is_new(None, None, parsed["business_name"], parsed["source"]):
                    stats["duplicate"] += 1
                    continue
                    
                score, signal = score_lead(parsed["_raw"], f"rss_{parsed['service']}")
                if score < config.TUNABLES["min_score_threshold"]:
                    continue
                    
                crm_lead = build_crm_lead(parsed, signal, score)
                valid_leads.append(crm_lead)
                stats["new"] += 1
                
        except ET.ParseError as e:
            logger.error(f"RSS parse failed for {source_name}: {e}")
            
    return valid_leads, stats

def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    dedup_store = DedupStore(config.DB_PATH)
    all_leads = []
    global_stats = {"found": 0, "new": 0, "duplicate": 0, "errored": 0}

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(process_source, name, cfg, dedup_store): name 
            for name, cfg in config.SOURCES.items()
        }
        
        for future in futures:
            source_name = futures[future]
            try:
                results, stats = future.result()
                global_stats["found"] += stats["found"]
                global_stats["duplicate"] += stats["duplicate"]
                global_stats["new"] += stats["new"]
                
                for lead in results:
                    dedup_store.mark_processed(lead["website"], lead["phone"], lead["business_name"], lead["source"])
                    all_leads.append(lead)
            except Exception as e:
                global_stats["errored"] += 1
                logger.error(f"Source {source_name} failed: {str(e)}")

    # Sort high intent leads to the top
    all_leads.sort(key=lambda x: x["score"], reverse=True)

    # Automated Contact Enrichment (Google Maps + Website Crawl)
    logger.info("Starting automated contact enrichment...")
    all_leads = asyncio.run(enrich_leads_batch(all_leads))

    with open(config.EXPORT_PATH, "w") as f:
        json.dump(all_leads, f, indent=2)

    logger.info(f"Run complete. Stats: {global_stats}")
    print(f"Exported {len(all_leads)} leads to {config.EXPORT_PATH}")

if __name__ == "__main__":
    main()