import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
  const userRaw = localStorage.getItem('medical_user');
  let role = '';
  let email = '';

  if (userRaw) {
    try {
      const user = JSON.parse(userRaw);
      role = user?.role || '';
      email = user?.email || '';
    } catch {
      role = '';
      email = '';
    }
  }

  return new HttpHeaders({
    'X-User-Role': role,
    'X-User-Email': email
  });
}




  get<T>(endpoint: string, params?: Record<string, string>): Observable<T> {
    let httpParams = new HttpParams();

    if (params) {
      Object.keys(params).forEach((key) => {
        httpParams = httpParams.set(key, params[key]);
      });
    }

    return this.http.get<T>(`${this.baseUrl}${endpoint}`, {
      headers: this.getHeaders(),
      params: httpParams
    });
  }

  post<T>(endpoint: string, payload: any): Observable<T> {
    return this.http.post<T>(`${this.baseUrl}${endpoint}`, payload, {
      headers: this.getHeaders()
    });
  }

  patch<T>(endpoint: string, payload: any): Observable<T> {
    return this.http.patch<T>(`${this.baseUrl}${endpoint}`, payload, {
      headers: this.getHeaders()
    });
  }
  put<T>(endpoint: string, payload: any): Observable<T> {
    return this.http.put<T>(`${this.baseUrl}${endpoint}`, payload, {
      headers: this.getHeaders()
    });
  }

  delete<T>(endpoint: string): Observable<T> {
    return this.http.delete<T>(`${this.baseUrl}${endpoint}`, {
      headers: this.getHeaders()
    });
  }
}