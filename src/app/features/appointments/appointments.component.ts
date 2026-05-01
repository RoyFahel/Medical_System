import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AppointmentService } from '../../core/services/appointment.service';
import { Appointment } from '../../core/models/appointment.model';
import { AuthService } from '../../core/services/auth.service';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './appointment.html',
})
export class AppointmentsComponent implements OnInit {
  allAppointments: Appointment[] = [];
  appointments: Appointment[] = [];
  statusFilter = '';

  constructor(
    private appointmentService: AppointmentService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    this.load();
  }

  getDoctorName(appointment: Appointment): string {
    return (
      appointment.doctor_name ||
      appointment.doctor_email_display ||
      '—'
    );
  }

  getPatientName(appointment: Appointment): string {
    return (
      appointment.patient_name ||
      appointment.patient_email_display ||
      '—'
    );
  }

  load(): void {
    this.appointmentService.getAppointments().subscribe({
      next: (data) => {
        this.allAppointments = data;

        if (this.statusFilter) {
          this.appointments = this.allAppointments.filter(
            (appointment) => appointment.status === this.statusFilter
          );
        } else {
          this.appointments = this.allAppointments;
        }
      },
      error: (err) => {
        console.error('Error loading appointments:', err);
      },
    });
  }

  saveStatus(appointment: Appointment): void {
    this.appointmentService.update(appointment.id, {
      status: appointment.status,
    }).subscribe(() => this.load());
  }

  remove(id: string): void {
    if (!confirm('Delete this appointment?')) return;

    this.appointmentService.delete(id).subscribe(() => this.load());
  }
}