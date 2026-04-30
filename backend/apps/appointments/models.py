from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField
from apps.accounts.models import User
from apps.doctors.models import Doctor


class ActiveAppointmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def active(self):
        return self.get_queryset()


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    id = ObjectIdAutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    # Soft delete fields live directly in this model.
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveAppointmentManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["appointment_date", "appointment_time", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date", "appointment_time"],
                name="unique_doctor_appointment_time",
            ),
            models.UniqueConstraint(
                fields=["patient", "appointment_date", "appointment_time"],
                name="unique_patient_appointment_time",
            ),
        ]

    def __str__(self):
        return f"{self.patient.email} - {self.doctor.full_name} - {self.appointment_date} {self.appointment_time}"
