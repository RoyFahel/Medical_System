from django.utils import timezone
from rest_framework import generics, permissions
from .models import Disease
from .serializers import DiseaseSerializer

class DiseaseListCreateView(generics.ListCreateAPIView):
    serializer_class = DiseaseSerializer
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        return Disease.objects.active()

    def get_permissions(self):
        return [permissions.AllowAny()]

class DiseaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiseaseSerializer
    # Some MongoDB documents may not have a usable primary key for updates.
    # `name` is used here as the API identifier (most projects keep it unique).
    lookup_field = 'name'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return Disease.objects.active()

    def get_permissions(self):
        return [permissions.AllowAny()]

    def perform_destroy(self, instance):
        Disease.objects.filter(name=instance.name).update(
            is_deleted=True,
            deleted_at=timezone.now(),
        )
