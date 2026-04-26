import uuid

from django.db import models
from apps.accounts.models import User
from apps.common.models import TimeStampedSoftDeleteModel
from apps.doctors.models import Doctor

class Appointment(TimeStampedSoftDeleteModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'

    # NOTE: With the current MongoDB backend setup, many documents end up with `id=None`,
    # which breaks relational fields. Keep FKs nullable for compatibility, and store
    # stable identifiers (emails) for API operations.
    public_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False, db_index=True)
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='appointments', null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, related_name='appointments', null=True, blank=True)
    patient_email = models.EmailField(null=True, blank=True)
    doctor_email = models.EmailField(null=True, blank=True)
    appointment_date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ['appointment_date', '-created_at']

    def __str__(self):
        return f'{self.patient_email} - {self.doctor_email}'
