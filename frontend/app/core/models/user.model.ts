export interface User {
  id: string;
  full_name: string;
  email: string;
  role: 'admin' | 'patient';
  created_at?: string;
  updated_at?: string;
}

export interface AuthResponse {
  user: User;
}
