import pytest
from enrich import clean_phone_number, enrich_lead_record

def test_clean_phone_number():
    assert clean_phone_number("9876543210") == "+919876543210"
    assert clean_phone_number("+91 98765 43210") == "+919876543210"
    assert clean_phone_number(None) is None

def test_enrich_lead_record_status():
    lead_ready = {"business_name": "Test Biz", "phone": "9876543210", "email": None}
    enriched = enrich_lead_record(lead_ready)
    assert enriched["contact_status"] == "ready"
    assert enriched["phone"] == "+919876543210"

    lead_pending = {"business_name": "Ghost Biz", "phone": None, "email": None}
    enriched_pending = enrich_lead_record(lead_pending)
    assert enriched_pending["contact_status"] == "needs_manual_lookup"