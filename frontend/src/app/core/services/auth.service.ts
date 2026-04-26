import { Injectable, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, tap, throwError } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AuthResponse, User } from '../models/user.model';
import { StorageService } from './storage.service';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private currentUserSignal = signal<User | null>(this.storage.getUser());
  currentUser = computed(() => this.currentUserSignal());
  isLoggedIn = computed(() => !!this.currentUserSignal());
  isAdmin = computed(() => this.currentUserSignal()?.role === 'admin');

  constructor(private http: HttpClient, private storage: StorageService) {}

  register(payload: { full_name: string; email: string; password: string; role: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${environment.apiUrl}/auth/register/`, payload).pipe(
      tap((response) => this.handleAuth(response.user))
    );
  }

  login(payload: { email: string; password: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${environment.apiUrl}/auth/login/`, payload).pipe(
      tap((response) => this.handleAuth(response.user))
    );
  }

  fetchProfile(): Observable<User> {
    const user = this.currentUserSignal();
    return user ? of(user) : throwError(() => new Error('No user in storage'));
  }

  logout(): void {
    this.storage.clearAuth();
    this.currentUserSignal.set(null);
  }

  private handleAuth(user: User): void {
    this.storage.setAuth(user);
    this.currentUserSignal.set(user);
  }
}
