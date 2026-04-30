import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.accounts.models import User
from apps.doctors.models import Doctor
from apps.appointments.serializers import AppointmentAdminSerializer

patient = User.objects.filter(email__iexact='roy@gmail.com').first()
doctor = Doctor.objects.filter(email__iexact='ahmad.khalil@gmail.com').first()
print('patient', patient)
print('doctor', doctor)

payload = {
    'patient_email': 'roy@gmail.com',
    'doctor_email': 'ahmad.khalil@gmail.com',
    'appointment_date': '2026-05-09',
    'appointment_time': '22:00',
    'notes': 'test'
}

serializer = AppointmentAdminSerializer(data=payload)
print('valid', serializer.is_valid())
print('errors', serializer.errors)
