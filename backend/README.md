# Medical Backend - Django + MongoDB

This backend is the Django + MongoDB version of the medical project.
It keeps the same subject as the previous project:
- doctors
- diseases
- appointments
- authentication

## Stack
- Django
- Django REST Framework
- MongoDB
- django-mongodb-backend
- JWT authentication

## Main relationships
- User -> Appointment = one to many
- Doctor -> Appointment = one to many
- Doctor <-> Disease = many to many

## Main endpoints
### Auth
- POST `/api/auth/register/`
- POST `/api/auth/login/`
- GET `/api/auth/profile/`

### Doctors
- GET `/api/doctors/`
- POST `/api/doctors/` admin only
- GET `/api/doctors/<id>/`
- PUT `/api/doctors/<id>/` admin only
- DELETE `/api/doctors/<id>/` admin only

### Diseases
- GET `/api/diseases/`
- POST `/api/diseases/` admin only
- GET `/api/diseases/<id>/`
- PUT `/api/diseases/<id>/` admin only
- DELETE `/api/diseases/<id>/` admin only

### Appointments
- GET `/api/appointments/`
- POST `/api/appointments/`
- GET `/api/appointments/<id>/`
- PUT `/api/appointments/<id>/`
- DELETE `/api/appointments/<id>/`

## Run steps
1. Create a virtual environment
2. Install requirements
3. Copy `.env.example` to `.env`
4. Run migrations
5. Create a superuser
6. Start the server

### Commands
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scriptsctivate      # Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Notes for your report
- MongoDB uses collections instead of SQL tables.
- Each document has a unique id.
- In this Django version, the models are implemented with Django model classes and stored in MongoDB through the Django MongoDB backend.
- `Doctor.diseases` is a many-to-many relationship.
- `Appointment.patient` and `Appointment.doctor` are foreign-key style relationships.

## Important project behavior
- Patient creates appointment -> status is automatically `pending`
- Admin can add, update, delete doctors and diseases
- Admin can manage appointments
- Doctors have image and PDF file fields
- Diseases have image field
