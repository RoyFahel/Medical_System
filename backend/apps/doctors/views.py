from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    ordering_fields = ['full_name', 'specialty', 'city', 'created_at']

    def get_queryset(self):
        # NOTE:
        # `diseases` is write-only in `DoctorSerializer`, so we don't need to prefetch it.
        # With the MongoDB backend, we can have legacy/bad documents without a PK, and
        # `prefetch_related` crashes on those instances. Avoiding prefetch keeps the API stable.
        queryset = Doctor.objects.active()
        search = self.request.query_params.get('search', '').strip()
        specialty = self.request.query_params.get('specialty', '').strip()
        city = self.request.query_params.get('city', '').strip()
        disease_id = self.request.query_params.get('disease', '').strip()

        if search:
            queryset = queryset.filter(Q(full_name__icontains=search) | Q(email__icontains=search))
        if specialty:
            queryset = queryset.filter(specialty__icontains=specialty)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if disease_id:
            queryset = queryset.filter(diseases__id=disease_id)
        return queryset.distinct()

    def get_permissions(self):
        return [permissions.AllowAny()]

class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSerializer
    # Doctor records in this MongoDB setup may not have a usable primary key exposed to the client.
    # Email is unique and stable enough to use as the API identifier.
    lookup_field = 'email'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return Doctor.objects.active()

    def get_permissions(self):
        return [permissions.AllowAny()]

    def perform_destroy(self, instance):
        # Some legacy MongoDB documents can exist without a usable primary key.
        # Using `save(update_fields=...)` forces an UPDATE and fails with:
        # "Cannot force an update in save() with no primary key."
        # A queryset update is safe here because email is unique.
        Doctor.objects.filter(email=instance.email).update(
            is_deleted=True,
            deleted_at=timezone.now(),
        )
