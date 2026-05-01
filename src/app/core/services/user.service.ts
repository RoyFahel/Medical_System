import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';
import { User } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private api: ApiService) {}

  list(): Observable<User[]> {
    return this.api.get<User[]>('/auth/users/');
  }

  delete(id: string): Observable<void> {
    return this.api.delete<void>(`/auth/users/${id}/`);
  }
}