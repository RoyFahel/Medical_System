import { Doctor } from './doctor.model';
import { User } from './user.model';

export interface Appointment {
  id: string;
  patient?: string;
  doctor: string;
  patient_email?: string;
  doctor_email?: string;
  appointment_date: string;
  notes: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
  patient_details?: User;
  doctor_details?: Doctor;
  created_at: string;
  updated_at: string;
}
