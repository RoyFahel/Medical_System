import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { DiseaseService } from '../../core/services/disease.service';
import { Disease } from '../../core/models/disease.model';
import { AuthService } from '../../core/services/auth.service';

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './diseases.html',
  styleUrl: './style.css'
})
export class DiseasesComponent implements OnInit {
  diseases: Disease[] = [];
  search = '';
  ordering = 'name';
  error = '';

  constructor(private diseaseService: DiseaseService, public auth: AuthService, private router: Router) {}

  ngOnInit(): void { this.load(); }

  getKey(disease: Disease): string {
    return String((disease as any).id || (disease as any)._id?.$oid || (disease as any)._id || disease.name || '');
  }

  load(): void {
    this.error = '';
    this.diseaseService.list({ search: this.search, ordering: this.ordering }).subscribe({
      next: (data) => {
        const items = Array.isArray(data) ? data : [];
        const q = this.search.trim().toLowerCase();
        this.diseases = q
          ? items.filter((d) => d.name?.toLowerCase().includes(q))
          : items;

        if (this.ordering === '-name') {
          this.diseases = [...this.diseases].sort((a, b) => b.name.localeCompare(a.name));
        } else {
          this.diseases = [...this.diseases].sort((a, b) => a.name.localeCompare(b.name));
        }
      },
      error: (err) => {
        console.error('Disease list failed', err);
        this.error = 'Could not load diseases. Check that Django is running on port 8000.';
        this.diseases = [];
      }
    });
  }

  edit(id: string): void { this.router.navigate(['/diseases', id, 'edit']); }

  remove(id: string): void {
    if (!id || !confirm('Delete this disease?')) return;
    this.diseaseService.delete(id).subscribe({
      next: () => this.load(),
      error: (err) => {
        console.error('Disease delete failed', err);
        this.error = 'Could not delete disease.';
      }
    });
  }
}
