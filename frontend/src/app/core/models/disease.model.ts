export interface Disease {
  id: string;
  name: string;
  description: string;
  symptoms: string;
  prevention: string;
  image?: string | null;
  image_url?: string;
  created_at: string;
  updated_at: string;
}
