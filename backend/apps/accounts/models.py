from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField


class User(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("patient", "Patient"),
    ]

    id = ObjectIdAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="patient")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
