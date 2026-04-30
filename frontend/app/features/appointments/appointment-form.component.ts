import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { DoctorService } from '../../core/services/doctor.service';
import { AppointmentService } from '../../core/services/appointment.service';
import { Doctor } from '../../core/models/doctor.model';
import { AuthService } from '../../core/services/auth.service';

@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './appointment-form.html',
    
})
export class AppointmentFormComponent implements OnInit {
  doctors: Doctor[] = [];
  error = '';

  form = this.fb.nonNullable.group({
    doctor: '',
    appointment_date: ['', [Validators.required]],
    appointment_time: ['', [Validators.required]],
    notes: ['']
  });

  constructor(
    private fb: FormBuilder,
    private doctorService: DoctorService,
    private appointmentService: AppointmentService,
    private auth: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.doctorService.list({ ordering: 'full_name' }).subscribe((data) => this.doctors = data);
  }

  submit(): void {
    this.error = '';
    if (this.form.invalid || !this.form.value.doctor) {
      this.error = 'Please choose a doctor, date and time.';
      return;
    }
    const patientEmail = this.auth.currentUser()?.email;
    if (!patientEmail) {
      this.error = 'Please log in again before creating an appointment.';
      return;
    }
    this.appointmentService.create({
      patient_email: patientEmail,
      doctor_email: this.form.value.doctor,
      appointment_date: this.form.value.appointment_date ?? '',
      appointment_time: this.form.value.appointment_time ?? '',
      notes: this.form.value.notes ?? ''
    }).subscribe({
      next: () => this.router.navigate(['/appointments']),
      error: (err) => {
        this.error = this.formatServerError(err?.error) || 'Could not create appointment.';
      }
    });
  }

  private formatServerError(error: any): string {
    if (!error) {
      return '';
    }
    if (typeof error === 'string') {
      return error;
    }
    if (Array.isArray(error)) {
      return error.map(String).join(' ');
    }

    const messages: string[] = [];
    if (error.detail) {
      messages.push(error.detail);
    }
    if (error.non_field_errors) {
      messages.push(...[].concat(error.non_field_errors).map(String));
    }
    for (const field of ['patient_email', 'doctor_email', 'appointment_date', 'appointment_time', 'notes']) {
      if (error[field]) {
        messages.push(...[].concat(error[field]).map(String));
      }
    }
    return messages.join(' ').trim();
  }

  cancel(): void { this.router.navigate(['/appointments']); }
}
