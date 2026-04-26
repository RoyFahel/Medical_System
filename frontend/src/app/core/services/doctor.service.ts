import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Doctor } from '../models/doctor.model';

@Injectable({ providedIn: 'root' })
export class DoctorService {
  constructor(private api: ApiService) {}

  private encodeKey(id: string): string {
    return encodeURIComponent(id);
  }

  list(params?: Record<string, string>): Observable<Doctor[]> {
    return this.api.get<Doctor[]>('/doctors/', params);
  }

  get(id: string): Observable<Doctor> {
    return this.api.get<Doctor>(`/doctors/${this.encodeKey(id)}/`);
  }

  create(formData: FormData): Observable<Doctor> {
    return this.api.post<Doctor>('/doctors/', formData);
  }

  update(id: string, formData: FormData): Observable<Doctor> {
    return this.api.put<Doctor>(`/doctors/${this.encodeKey(id)}/`, formData);
  }

  delete(id: string): Observable<void> {
    return this.api.delete<void>(`/doctors/${this.encodeKey(id)}/`);
  }
}
