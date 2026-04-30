from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions
from .models import Disease
from .serializers import DiseaseSerializer


class DiseaseListCreateView(generics.ListCreateAPIView):
    serializer_class = DiseaseSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]

    def get_queryset(self):
        queryset = Disease.objects.active()
        search = self.request.query_params.get("search", "").strip()
        ordering = self.request.query_params.get("ordering", "name").strip()
        if search:
            queryset = queryset.filter(name__icontains=search)
        if ordering in ["name", "-name", "created_at", "-created_at"]:
            queryset = queryset.order_by(ordering)
        return queryset


class DiseaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiseaseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Disease.objects.active()

    def get_object(self):
        key = self.kwargs.get("pk")
        queryset = self.get_queryset()
        # Prefer ObjectId id, fallback to name for old frontend links.
        obj = queryset.filter(pk=key).first() or queryset.filter(name=key).first()
        if obj is None:
            obj = get_object_or_404(queryset, name__iexact=key)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_destroy(self, instance):
        Disease.all_objects.filter(pk=instance.pk).update(is_deleted=True, deleted_at=timezone.now())
