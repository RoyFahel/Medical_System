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
})
export class DiseasesComponent implements OnInit {
  diseases: Disease[] = [];
  search = '';
  ordering = 'name';

  constructor(private diseaseService: DiseaseService, public auth: AuthService, private router: Router) {}

  ngOnInit(): void { this.load(); }

  getKey(disease: any): string {
    const key = disease.id || disease._id?.$oid || disease._id;
  
    if (!key) {
      console.error('Disease has no ID:', disease);
      return '';
    }
  
    return String(key);
  }

  load(): void {
    this.diseaseService.list().subscribe((data) => this.diseases = data);
  }

  edit(id: string): void { this.router.navigate(['/diseases', id, 'edit']); }

  remove(id: string): void {
    if (!confirm('Delete this disease?')) return;
    this.diseaseService.delete(id).subscribe(() => this.load());
  }
}
