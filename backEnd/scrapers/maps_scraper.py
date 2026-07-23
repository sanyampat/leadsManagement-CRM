import httpx
import uuid
from typing import List, Dict, Any
from backend.models.discovery import DiscoveredBusiness, Socials, WebsiteStatus
from backend.utils.drops import is_unwanted_url

OVERPASS разные_API_URL = "https://overpass-api.de/api/interpreter"

async def search_local_businesses(business_type: str, location: str, country: str, max_results: int = 20) -> List[DiscoveredBusiness]:
    """
    Queries OpenStreetMap for physical business nodes matching the category and city.
    """
    query = f"""
    [out:json][timeout:25];
    area[name="{location}"]->.searchArea;
    (
      node["name"]["shop"~"{business_type}",i](area.searchArea);
      node["name"]["amenity"~"{business_type}",i](area.searchArea);
      node["name"]["office"~"{business_type}",i](area.searchArea);
    );
    out body {max_results};
    """
    
    discovered = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post("https://overpass-api.de/api/interpreter", data={"data": query})
            data = response.json()
            
            for element in data.get("elements", []):
                tags = element.get("tags", {})
                name = tags.get("name")
                if not name:
                    continue
                
                website = tags.get("website") or tags.get("contact:website")
                if website and is_unwanted_url(website):
                    website = None # Drop article links if erroneously listed
                
                phone = tags.get("phone") or tags.get("contact:phone")
                email = tags.get("email") or tags.get("contact:email")
                
                # Extract socials if present in OSM tags
                socials = Socials(
                    instagram=tags.get("contact:instagram"),
                    facebook=tags.get("contact:facebook"),
                    linkedin=tags.get("contact:linkedin")
                )
                
                business = DiscoveredBusiness(
                    id=str(uuid.uuid4()),
                    business_name=name,
                    category=business_type.capitalize(),
                    location=f"{location}, {country}",
                    country=country,
                    latitude=element.get("lat"),
                    longitude=element.get("lon"),
                    official_website=website,
                    phone_number=phone,
                    email=email,
                    socials=socials,
                    rating=4.5, # Placeholder: Replace with Google Places/Yelp rating merge if API keys added
                    review_count=120, # Placeholder
                    description=f"{business_type.capitalize()} located in {location}.",
                    website_status=WebsiteStatus.EXISTS if website else WebsiteStatus.MISSING
                )
                discovered.append(business)
        except Exception as e:
            print(f"Scraper Error: {e}")
            
    return discovered