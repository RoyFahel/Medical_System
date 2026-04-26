import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AppointmentService } from '../../core/services/appointment.service';
import { Appointment } from '../../core/models/appointment.model';
import { AuthService } from '../../core/services/auth.service';
import { DoctorService } from '../../core/services/doctor.service';
import { Doctor } from '../../core/models/doctor.model';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './appointment.html',
})
export class AppointmentsComponent implements OnInit {
  appointments: Appointment[] = [];
  statusFilter = '';
  private doctorByEmail = new Map<string, Doctor>();

  constructor(
    private appointmentService: AppointmentService,
    private doctorService: DoctorService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    this.doctorService.list().subscribe({
      next: (doctors) => {
        this.doctorByEmail = new Map(
          doctors
            .filter((d) => !!d.email)
            .map((d) => [d.email.toLowerCase(), d])
        );
      },
      error: () => {
        this.doctorByEmail = new Map();
      }
    });

    this.load();
  }

  getDoctorName(appointment: Appointment): string {
    const fromDetails = appointment.doctor_details?.full_name?.trim();
    if (fromDetails) return fromDetails;

    const email = appointment.doctor_email?.trim().toLowerCase();
    if (email) {
      const doctor = this.doctorByEmail.get(email);
      const name = doctor?.full_name?.trim();
      if (name) return name;
    }

    return '—';
  }

  load(): void {
    this.appointmentService.list({ status: this.statusFilter }).subscribe({
      next: (data) => this.appointments = data,
      error: () => this.appointments = []
    });
  }

  saveStatus(appointment: Appointment): void {
    this.appointmentService.update(appointment.id, { status: appointment.status }).subscribe();
  }

  remove(id: string): void {
    if (!confirm('Delete this appointment?')) return;
    this.appointmentService.delete(id).subscribe(() => this.load());
  }
}
