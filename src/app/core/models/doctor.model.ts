import { Disease } from './disease.model';

export interface Doctor {
  id: string;
  full_name: string;
  email: string;
  phone: string;


  profile_image?: string;
  profile_image_url?: string;

  license_pdf?: string;
  license_pdf_url?: string;

  diseases?: string[];
  disease_details?: Disease[];

  created_at?: string;
  updated_at?: string;
}