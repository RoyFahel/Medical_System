import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DiseaseService {
  private apiUrl = 'http://127.0.0.1:8000/api/diseases/';

  constructor(private http: HttpClient) {}

  list(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  getAll(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  get(id: string): Observable<any> {
    return this.http.get(`${this.apiUrl}${id}/`);
  }

  create(data: FormData): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }

  update(id: string, data: FormData): Observable<any> {
    return this.http.put(`${this.apiUrl}${id}/`, data);
  }

  delete(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}/`);
  }
}