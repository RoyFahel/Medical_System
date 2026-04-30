import { Doctor } from './doctor.model';
import { User } from './user.model';

export interface Appointment {
  id: string;
  patient?: string | null;
  doctor?: string | null;
  patient_email?: string;
  doctor_email?: string;
  appointment_date: string;
  appointment_time: string;
  notes: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
  patient_details?: User | null;
  doctor_details?: Doctor | null;
  created_at?: string;
  updated_at?: string;
}
