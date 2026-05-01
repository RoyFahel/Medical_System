import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { LoginComponent } from './features/auth/login.component';
import { RegisterComponent } from './features/auth/register.component';
import { DoctorsComponent } from './features/doctors/doctors.component';
import { DoctorFormComponent } from './features/doctors/doctor-form.component';
import { DiseasesComponent } from './features/diseases/diseases.component';
import { DiseaseFormComponent } from './features/diseases/disease-form.component';
import { AppointmentsComponent } from './features/appointments/appointments.component';
import { AppointmentFormComponent } from './features/appointments/appointment-form.component';
import { UsersComponent }   from './features/users/users.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'doctors', component: DoctorsComponent },
  { path: 'doctors/new', component: DoctorFormComponent },
  { path: 'doctors/:id/edit', component: DoctorFormComponent },
  { path: 'diseases', component: DiseasesComponent },
  { path: 'diseases/new', component: DiseaseFormComponent },
  { path: 'diseases/:id/edit', component: DiseaseFormComponent },
  { path: 'appointments', component: AppointmentsComponent },
  { path: 'appointments/new', component: AppointmentFormComponent },
  {
  path: 'users',
  component: UsersComponent
},

  { path: '**', redirectTo: '' }
];
