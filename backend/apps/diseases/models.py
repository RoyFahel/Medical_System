from django.db import models
from apps.common.models import TimeStampedSoftDeleteModel

class Disease(TimeStampedSoftDeleteModel):
    name = models.CharField(max_length=150)
    description = models.TextField()
    symptoms = models.TextField()
    prevention = models.TextField()
    image = models.ImageField(upload_to='diseases/', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
