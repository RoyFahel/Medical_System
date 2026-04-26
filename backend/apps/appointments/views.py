from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentAdminSerializer

class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentAdminSerializer
    ordering_fields = ['appointment_date', 'created_at', 'status']

    def get_queryset(self):
        queryset = Appointment.objects.active()
        status_value = self.request.query_params.get('status', '').strip()
        doctor_key = self.request.query_params.get('doctor', '').strip()
        if status_value:
            queryset = queryset.filter(status=status_value)
        if doctor_key:
            queryset = queryset.filter(doctor_email=doctor_key)
        return queryset

    def get_permissions(self):
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        patient_email = self.request.data.get('patient_email')
        doctor_email = self.request.data.get('doctor_email')
        if not patient_email:
            raise ValidationError({'patient_email': 'Patient email is required.'})
        if not doctor_email:
            raise ValidationError({'doctor_email': 'Doctor email is required.'})
        serializer.save(status='pending')

class AppointmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentAdminSerializer
    lookup_field = 'public_id'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        return Appointment.objects.active()

    def get_object(self):
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get(self.lookup_url_kwarg or self.lookup_field)
        obj = queryset.filter(public_id=lookup_value).order_by('-updated_at', '-created_at').first()
        if obj is None:
            from rest_framework.exceptions import NotFound
            raise NotFound('Appointment not found.')
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        return [permissions.AllowAny()]

    def perform_destroy(self, instance):
        Appointment.objects.filter(public_id=instance.public_id).update(
            is_deleted=True,
            deleted_at=timezone.now(),
        )
