# Medical Project - Angular + Django + MongoDB

This package contains two folders that are already matched to each other:
- `backend/` = Django + MongoDB backend
- `frontend/` = Angular frontend

## Backend API base URL expected by frontend
`http://127.0.0.1:8000/api`

You can change it in:
`frontend/src/environments/environment.ts`

## Main features
- JWT login and register
- Doctors CRUD
- Diseases CRUD
- Appointments CRUD
- Admin can manage doctors and diseases
- Patient can create appointments
- Search and ordering
- Image upload and PDF upload
- Angular routing + reactive forms + validators

## Run backend
1. Open terminal in `backend`
2. Create virtual environment
3. Install requirements
4. Copy `.env.example` to `.env`
5. Run:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Run frontend
1. Open terminal in `frontend`
2. Install dependencies
3. Start Angular

```bash
npm install
npm start
```

Angular will run on:
`http://localhost:4200`

## Important compatibility notes
- Frontend sends requests to Django endpoints under `/api/...`
- Frontend uses JWT token in `Authorization: Bearer <token>`
- File uploads for doctors and diseases use `FormData`
- Patient appointment creation does not send status; backend sets it automatically to `pending`
