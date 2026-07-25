import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface SearchParams {
  business_type: string;
  location: string;
  country: string;
  max_results: number;
}

export interface SocialLinks {
  instagram?: string;
  facebook?: string;
  linkedin?: string;
  whatsapp?: string;
}

export interface WebsiteAudit {
  https: boolean;
  mobile_friendly: boolean;
  responsive: boolean;
  loading_speed_ms: number;
  seo_basics: boolean;
  contact_form: boolean;
  modern_design: boolean;
  call_to_action: boolean;
  overall_quality_score: number;
}

export interface OpportunityAssessment {
  score: number;
  reason: string;
  deficiencies: string[];
}

// Ensure the "export" keyword is explicitly present right here:
export interface DiscoveredBusiness {
  id: string;
  business_name: string;
  category: string;
  location: string;
  country: string;
  latitude?: number;
  longitude?: number;
  official_website?: string;
  phone_number?: string;
  email?: string;
  socials: SocialLinks;
  rating?: number;
  review_count: number;
  description?: string;
  website_status: string;
  website_audit?: WebsiteAudit;
  opportunity?: OpportunityAssessment;
  crm_saved: boolean;
  crm_lead_id?: string;
}

export const searchBusinesses = async (params: SearchParams): Promise<DiscoveredBusiness[]> => {
  const response = await axios.post(`${API_BASE_URL}/discovery/search`, params);
  return response.data;
};

export const saveToCRM = async (leadId: string) => {
  const response = await axios.post(`${API_BASE_URL}/crm-bridge/save/${leadId}`);
  return response.data;
};

export const fetchSearchHistory = async () => {
  const response = await axios.get(`${API_BASE_URL}/discovery/history`);
  return response.data;
};