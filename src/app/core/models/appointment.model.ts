import { Doctor } from './doctor.model';
import { User } from './user.model';

export interface Appointment {
  id: string;

  // MongoDB ObjectId strings returned by backend
  patient?: string | null;
  doctor?: string | null;

  // Used when creating appointment
  patient_email?: string;
  doctor_email?: string;

  // Returned by backend for display
  patient_name?: string;
  doctor_name?: string;
  patient_email_display?: string;
  doctor_email_display?: string;
  doctor_specialty?: string;

  appointment_date: string;
  appointment_time: string;
  notes: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';

  // Old optional nested fields, keep them if some component still uses them
  patient_details?: User | null;
  doctor_details?: Doctor | null;

  created_at?: string;
  updated_at?: string;
  is_deleted?: boolean;
}