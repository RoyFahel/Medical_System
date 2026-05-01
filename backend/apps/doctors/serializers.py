from rest_framework import serializers
from apps.diseases.models import Disease
from apps.diseases.serializers import DiseaseSerializer
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    diseases = serializers.PrimaryKeyRelatedField(
        queryset=Disease.objects.active(), many=True, required=False, write_only=True
    )
    disease_details = DiseaseSerializer(source="diseases", many=True, read_only=True)
    profile_image_url = serializers.SerializerMethodField()
    license_pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            "id", "full_name", "email", "phone", 
            "profile_image", "profile_image_url", "license_pdf", "license_pdf_url",
            "diseases", "disease_details", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        diseases = validated_data.pop("diseases", [])
        doctor = Doctor.objects.create(**validated_data)
        if diseases:
            doctor.diseases.set(diseases)
        return doctor

    def update(self, instance, validated_data):
        diseases = validated_data.pop("diseases", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if diseases is not None:
            instance.diseases.set(diseases)
        return instance

    def get_profile_image_url(self, obj):
        request = self.context.get("request")
        if obj.profile_image and request:
            return request.build_absolute_uri(obj.profile_image.url)
        return ""

    def get_license_pdf_url(self, obj):
        request = self.context.get("request")
        if obj.license_pdf and request:
            return request.build_absolute_uri(obj.license_pdf.url)
        return ""
