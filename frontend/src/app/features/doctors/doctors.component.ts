import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { DoctorService } from '../../core/services/doctor.service';
import { Doctor } from '../../core/models/doctor.model';
import { AuthService } from '../../core/services/auth.service';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './doctors.html',
})
export class DoctorsComponent implements OnInit {
  doctors: Doctor[] = [];
  search = '';
  specialty = '';
  city = '';
  ordering = 'full_name';

  constructor(private doctorService: DoctorService, public auth: AuthService, private router: Router) { }

  ngOnInit(): void { this.load(); }

  getKey(doctor: Doctor): string {
  
    return (doctor as any).id || doctor.email;
  }

  getDiseaseNames(doctor: Doctor): string {
    const names = doctor.disease_details?.map((d) => d.name) ?? [];
    return names.length ? names.join(', ') : '—';
  }

  load(): void {
    this.doctorService.list({ search: this.search, specialty: this.specialty, city: this.city, ordering: this.ordering }).subscribe({
      next: (data) => this.doctors = data,
      error: () => this.doctors = []
    });
  }

  edit(id: string): void { this.router.navigate(['/doctors', id, 'edit']); }

  remove(id: string): void {
    if (!confirm('Delete this doctor?')) return;
    this.doctorService.delete(id).subscribe(() => this.load());
  }
}
