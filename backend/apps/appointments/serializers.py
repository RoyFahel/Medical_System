from rest_framework import serializers
from apps.accounts.serializers import UserSerializer
from apps.doctors.serializers import DoctorSerializer
from .models import Appointment
import uuid

class AppointmentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='public_id', read_only=True)
    # In this MongoDB setup, related objects may not have a usable PK.
    # Treat the relational fields as optional/read-only and rely on emails for writes.
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    patient_details = UserSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    patient_email = serializers.EmailField()
    doctor_email = serializers.EmailField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'patient_email', 'doctor_email', 'appointment_date', 'notes', 'status',
            'patient_details', 'doctor_details', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        # Backfill `public_id` for legacy docs (no PK needed; queryset update is OK).
        if not getattr(instance, 'public_id', None):
            new_id = str(uuid.uuid4())
            Appointment.objects.filter(
                created_at=instance.created_at,
                patient_email=instance.patient_email,
                doctor_email=instance.doctor_email,
                appointment_date=instance.appointment_date,
            ).update(public_id=new_id)
            instance.public_id = new_id
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        Appointment.objects.filter(public_id=instance.public_id).update(**validated_data)
        return Appointment.objects.filter(public_id=instance.public_id).order_by('-updated_at', '-created_at').first()

class AppointmentAdminSerializer(AppointmentSerializer):
    class Meta(AppointmentSerializer.Meta):
        read_only_fields = ['created_at', 'updated_at']
