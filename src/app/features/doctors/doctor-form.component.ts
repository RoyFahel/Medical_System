import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DoctorService } from '../../core/services/doctor.service';
import { DiseaseService } from '../../core/services/disease.service';
import { Disease } from '../../core/models/disease.model';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './doctor-form.html',
})
export class DoctorFormComponent implements OnInit {
  diseases: Disease[] = [];
  error = '';
  isEdit = false;
  private id?: string;
  private imageFile?: File;
  private pdfFile?: File;

  form = this.fb.group({
    full_name: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    phone: ['', [Validators.required]],
   

    diseases: [[] as string[]]
  });

  constructor(
    private fb: FormBuilder,
    private doctorService: DoctorService,
    private diseaseService: DiseaseService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.diseaseService.list().subscribe((data) => this.diseases = data);
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEdit = true;
      this.id = id;
      this.doctorService.get(id).subscribe((doctor) => {
        this.form.patchValue({
          full_name: doctor.full_name,
          email: doctor.email,
          phone: doctor.phone,
        
          diseases: (doctor.diseases ?? []).map((d) => String(d))
        });
      });
    }
  }

  onImageSelected(event: Event): void { this.imageFile = (event.target as HTMLInputElement).files?.[0]; }
  onPdfSelected(event: Event): void { this.pdfFile = (event.target as HTMLInputElement).files?.[0]; }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.error = 'Please fix form errors before saving.';
      return;
    }
    this.error = '';
    const formData = new FormData();
    const value = this.form.getRawValue();
    formData.append('full_name', value.full_name ?? '');
    formData.append('email', value.email ?? '');
    formData.append('phone', value.phone ?? '');
    (value.diseases ?? []).forEach((id) => formData.append('diseases', String(id)));
    if (this.imageFile) formData.append('profile_image', this.imageFile);
    if (this.pdfFile) formData.append('license_pdf', this.pdfFile);

    const request = this.isEdit && this.id
      ? this.doctorService.update(this.id, formData)
      : this.doctorService.create(formData);

    request.subscribe({
      next: () => this.router.navigate(['/doctors']),
      error: (err: unknown) => {
        // Surface the backend JSON to make 400s actionable.
        // (Users were only seeing "400 Bad Request" in the console.)
        // eslint-disable-next-line no-console
        console.error('Doctor save failed', err);
        this.error = this.formatSaveError(err);
      }
    });
  }

  cancel(): void { this.router.navigate(['/doctors']); }

  private formatSaveError(err: unknown): string {
    if (!(err instanceof HttpErrorResponse)) {
      return 'Could not save doctor.';
    }

    if (err.status === 0) {
      return 'Could not reach the server. Is the backend running on port 8000?';
    }

    const data = err.error as any;
    if (err.status === 400 && data) {
      // DRF usually returns: { field: ["message"], non_field_errors: ["..."] }
      if (typeof data === 'string') return data;

      if (data.email) {
        const msg =
          Array.isArray(data.email) ? data.email.join(' ') :
          typeof data.email === 'string' ? data.email :
          '';
        if (msg) {
          this.form.controls.email.setErrors({ ...(this.form.controls.email.errors || {}), server: msg });
          this.form.controls.email.markAsTouched();
        }
      }

      const parts: string[] = [];
      Object.entries(data).forEach(([key, value]) => {
        const msg =
          Array.isArray(value) ? value.join(' ') :
          typeof value === 'string' ? value :
          value ? JSON.stringify(value) : '';
        if (msg) parts.push(`${key}: ${msg}`);
      });

      if (parts.length) return parts.join(' | ');
    }

    return err.message || `Could not save doctor (HTTP ${err.status}).`;
  }
}
