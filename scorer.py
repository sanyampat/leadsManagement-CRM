import logging
import config

logger = logging.getLogger(__name__)

def score_lead(raw_data, service_key):
    if service_key not in config.ICP_SIGNALS:
        logger.error(f"FATAL: Missing or typo'd service_key '{service_key}' in config.ICP_SIGNALS. Fix your config.")
        return 0, ""
        
    config_entry = config.ICP_SIGNALS[service_key]
    signals = config_entry.get("signals", [])
    disqualifiers = config_entry.get("disqualifiers", [])
    
    for rule in disqualifiers:
        if rule["heuristic"](raw_data):
            return 0, f"disqualified: {rule['signal']}"
            
    score = 0
    matched_signals = []
    
    for rule in signals:
        if rule["heuristic"](raw_data):
            score += rule["weight"]
            matched_signals.append(rule["signal"])
            
    return score, ", ".join(matched_signals)