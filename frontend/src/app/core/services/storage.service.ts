import { Injectable } from '@angular/core';
import { User } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class StorageService {
  private userKey = 'medical_user';

  setAuth(user: User): void {
    localStorage.setItem(this.userKey, JSON.stringify(user));
  }

  clearAuth(): void {
    localStorage.removeItem(this.userKey);
  }

  getUser(): User | null {
    const raw = localStorage.getItem(this.userKey);
    return raw ? JSON.parse(raw) as User : null;
  }
}
