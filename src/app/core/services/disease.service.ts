import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { Disease } from '../models/disease.model';

@Injectable({ providedIn: 'root' })
export class DiseaseService {
  constructor(private api: ApiService) {}

  private encodeKey(id: string): string {
    return encodeURIComponent(id);
  }

  list(params?: Record<string, string>): Observable<Disease[]> {
    return this.api.get<Disease[]>('/diseases/', params);
  }

  getAll(): Observable<Disease[]> {
    return this.list();
  }

  get(id: string): Observable<Disease> {
    return this.api.get<Disease>(`/diseases/${this.encodeKey(id)}/`);
  }

  create(data: FormData): Observable<Disease> {
    return this.api.post<Disease>('/diseases/', data);
  }

  update(id: string, data: FormData): Observable<Disease> {
    return this.api.put<Disease>(`/diseases/${this.encodeKey(id)}/`, data);
  }

  delete(id: string): Observable<void> {
    return this.api.delete<void>(`/diseases/${this.encodeKey(id)}/`);
  }
}
