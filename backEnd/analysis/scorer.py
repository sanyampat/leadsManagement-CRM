from backend.models.discovery import DiscoveredBusiness, WebsiteStatus, OpportunityAssessment

def calculate_opportunity(business: DiscoveredBusiness) -> OpportunityAssessment:
    deficiencies = []
    base_score = 30 # Default low opportunity if website is perfect
    
    status = business.website_status
    reviews = business.review_count
    audit = business.website_audit

    # Base score assignment by website presence
    if status == WebsiteStatus.MISSING:
        base_score = 85
        deficiencies.append("No official website")
    elif status in [WebsiteStatus.BROKEN, WebsiteStatus.UNDER_CONSTRUCTION]:
        base_score = 90
        deficiencies.append(f"Website is {status.value.lower()}")
    elif status == WebsiteStatus.SOCIAL_ONLY:
        base_score = 75
        deficiencies.append("Relies exclusively on social media")
    elif status == WebsiteStatus.EXISTS and audit:
        # Inverse of web quality: poorer quality = higher opportunity
        base_score = int((100 - audit.overall_quality_score) * 0.8)
        if not audit.mobile_friendly: deficiencies.append("Not mobile friendly")
        if not audit.contact_form: deficiencies.append("Missing contact form")
        if audit.loading_speed_ms > 3000: deficiencies.append("Slow page load speed")
        if not audit.seo_basics: deficiencies.append("Poor basic SEO")

    # Reputation Multiplier (More reviews = higher commercial value to pitch)
    multiplier = 1.0
    if reviews > 200:
        multiplier = 1.25
    elif reviews > 50:
        multiplier = 1.15
    elif reviews > 10:
        multiplier = 1.05

    final_score = min(100, int(base_score * multiplier))
    
    # Reason Generation
    if status != WebsiteStatus.EXISTS:
        reason = f"{business.category} has {reviews} reviews but {status.value.lower()}. Very strong prospect."
    elif deficiencies:
        reason = f"Website exists but suffers from: {', '.join(deficiencies[:2])}. High redesign potential."
    else:
        reason = "Modern, high-performing web presence detected. Low immediate opportunity."

    return OpportunityAssessment(
        score=final_score,
        reason=reason,
        deficiencies=deficiencies
    )