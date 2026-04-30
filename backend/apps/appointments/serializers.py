from rest_framework import serializers
from .models import Appointment
from apps.accounts.models import User
from apps.doctors.models import Doctor


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    patient_email = serializers.EmailField(write_only=True)
    doctor_email = serializers.EmailField(write_only=True)

    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor",
            "patient_email",
            "doctor_email",
            "patient_name",
            "doctor_name",
            "appointment_date",
            "appointment_time",
            "notes",
            "status",
            "created_at",
            "updated_at",
            "is_deleted",
        ]
        read_only_fields = [
            "id",
            "patient",
            "doctor",
            "patient_name",
            "doctor_name",
            "created_at",
            "updated_at",
            "is_deleted",
        ]

    def get_patient(self, obj):
        return str(obj.patient_id) if obj.patient_id else None

    def get_doctor(self, obj):
        return str(obj.doctor_id) if obj.doctor_id else None

    def get_patient_name(self, obj):
        return obj.patient.full_name if obj.patient else ""

    def get_doctor_name(self, obj):
        return obj.doctor.full_name if obj.doctor else ""

    def create(self, validated_data):
        patient_email = validated_data.pop("patient_email")
        doctor_email = validated_data.pop("doctor_email")

        patient = User.objects.filter(email=patient_email, role="patient", is_deleted=False).first()
        if not patient:
            raise serializers.ValidationError({"patient_email": "Patient not found."})

        doctor = Doctor.objects.filter(email=doctor_email, is_deleted=False).first()
        if not doctor:
            raise serializers.ValidationError({"doctor_email": "Doctor not found."})

        exists = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=validated_data.get("appointment_date"),
            appointment_time=validated_data.get("appointment_time"),
            is_deleted=False,
        ).exists()

        if exists:
            raise serializers.ValidationError({
                "appointment_time": "This doctor already has an appointment at this time."
            })

        return Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            **validated_data
        )