export type WebsiteStatus = 
  | 'Has Official Website'
  | 'No Website'
  | 'Website Broken'
  | 'Under Construction'
  | 'Redirects Elsewhere'
  | 'Social Media Only';

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
  website_status: WebsiteStatus;
  website_audit?: WebsiteAudit;
  opportunity?: OpportunityAssessment;
  crm_saved: boolean;
  crm_lead_id?: string;
}