from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField


class ActiveDiseaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def active(self):
        return self.get_queryset()


class Disease(models.Model):
    id = ObjectIdAutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    symptoms = models.TextField()
    prevention = models.TextField()
    image = models.ImageField(upload_to="diseases/", null=True, blank=True)

    # Soft delete fields live directly in this model.
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ActiveDiseaseManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
