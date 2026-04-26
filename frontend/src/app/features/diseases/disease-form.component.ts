import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DiseaseService } from '../../core/services/disease.service';

@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './diseases-form.html',
})
export class DiseaseFormComponent implements OnInit {
  error = '';
  isEdit = false;
  private id?: string;
  private imageFile?: File;

  form = this.fb.group({
    name: ['', [Validators.required]],
    description: ['', [Validators.required]],
    symptoms: ['', [Validators.required]],
    prevention: ['', [Validators.required]],
  });

  constructor(
    private fb: FormBuilder,
    private diseaseService: DiseaseService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');

    // Add disease page: /diseases/new
    if (!id || id === 'undefined' || id === 'null') {
      this.isEdit = false;
      this.id = undefined;
      return;
    }

    // Edit disease page: /diseases/:id/edit
    this.isEdit = true;
    this.id = id;

    this.diseaseService.get(id).subscribe({
      next: (disease) => {
        this.form.patchValue({
          name: disease.name || '',
          description: disease.description || '',
          symptoms: disease.symptoms || '',
          prevention: disease.prevention || '',
        });
      },
      error: (err) => {
        console.error(err);
        this.error = 'Could not load disease.';
      },
    });
  }

  onImageSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.imageFile = input.files?.[0] || undefined;
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const value = this.form.getRawValue();
    const formData = new FormData();

    formData.append('name', value.name ?? '');
    formData.append('description', value.description ?? '');
    formData.append('symptoms', value.symptoms ?? '');
    formData.append('prevention', value.prevention ?? '');

    if (this.imageFile) {
      formData.append('image', this.imageFile);
    }

    const request =
      this.isEdit && this.id
        ? this.diseaseService.update(this.id, formData)
        : this.diseaseService.create(formData);

    request.subscribe({
      next: () => this.router.navigate(['/diseases']),
      error: (err) => {
        console.error(err);
        this.error = 'Could not save disease.';
      },
    });
  }

  cancel(): void {
    this.router.navigate(['/diseases']);
  }
}