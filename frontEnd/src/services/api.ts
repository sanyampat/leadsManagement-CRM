import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface SearchParams {
  business_type: string;
  location: string;
  country: string;
  max_results: number;
}

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
  socials: {
    instagram?: string;
    facebook?: string;
    linkedin?: string;
  };
  rating?: number;
  review_count: number;
  website_status: string;
  website_audit?: {
    https: boolean;
    mobile_friendly: boolean;
    loading_speed_ms: number;
    contact_form: boolean;
    overall_quality_score: number;
  };
  opportunity?: {
    score: number;
    reason: string;
    deficiencies: string[];
  };
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