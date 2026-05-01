import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserService } from '../../core/services/user.service';
import { User } from '../../core/models/user.model';
import { AuthService } from '../../core/services/auth.service';

@Component({
  standalone: true,
  imports: [CommonModule],
  templateUrl: './users.html'
})
export class UsersComponent implements OnInit {
  users: User[] = [];
  loading = false;
  error = '';

  constructor(
    private userService: UserService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.loading = true;
    this.error = '';

    this.userService.list().subscribe({
      next: (data) => {
        this.users = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'You are not allowed to view users, or the server returned an error.';
        this.loading = false;
        console.error(err);
      }
    });
  }
  deleteUser(id: string): void {
  if (!confirm('Delete this user?')) return;

  this.userService.delete(id).subscribe({
    next: () => {
      this.loadUsers();
    },
    error: (err) => {
      console.error(err);
      this.error = 'Could not delete user.';
    }
  });
}
}