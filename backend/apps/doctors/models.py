from django.db import models
from apps.common.models import TimeStampedSoftDeleteModel
from apps.diseases.models import Disease

class Doctor(TimeStampedSoftDeleteModel):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    specialty = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='doctors/images/', null=True, blank=True)
    license_pdf = models.FileField(upload_to='doctors/pdfs/', null=True, blank=True)
    diseases = models.ManyToManyField(Disease, related_name='doctors', blank=True)
    
    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name
