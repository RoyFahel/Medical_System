from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField
from apps.diseases.models import Disease


class ActiveDoctorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def active(self):
        return self.get_queryset()


class Doctor(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    specialty = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to="doctors/images/", null=True, blank=True)
    license_pdf = models.FileField(upload_to="doctors/pdfs/", null=True, blank=True)
    diseases = models.ManyToManyField(Disease, related_name="doctors", blank=True)

    # Soft delete fields live directly in this model.
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveDoctorManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name
