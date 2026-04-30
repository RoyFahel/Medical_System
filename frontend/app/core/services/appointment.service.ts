import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Appointment } from '../models/appointment.model';

@Injectable({ providedIn: 'root' })
export class AppointmentService {
  constructor(private api: ApiService) {}

  list(params?: Record<string, string>): Observable<Appointment[]> {
    return this.api.get<Appointment[]>('/appointments/', params);
  }

  create(payload: { patient_email: string; doctor_email: string; appointment_date: string; appointment_time: string; notes: string }): Observable<Appointment> {
    return this.api.post<Appointment>('/appointments/', payload);
  }

  update(id: string, payload: Partial<Appointment>): Observable<Appointment> {
    return this.api.patch<Appointment>(`/appointments/${id}/`, payload);
  }

  delete(id: string): Observable<void> {
    return this.api.delete<void>(`/appointments/${id}/`);
  }
}
