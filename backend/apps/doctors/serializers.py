from rest_framework import serializers
from apps.diseases.models import Disease
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    # With the MongoDB backend, the primary key can be an ObjectId; expose it as a string.
    id = serializers.CharField(source='pk', read_only=True)
    diseases = serializers.PrimaryKeyRelatedField(queryset=Disease.objects.active(), many=True, required=False, write_only=True)
    profile_image_url = serializers.SerializerMethodField()
    license_pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = [
            'id', 'full_name', 'email', 'phone', 'specialty', 'city',
            'profile_image', 'profile_image_url', 'license_pdf', 'license_pdf_url',
            'diseases', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        diseases = validated_data.pop('diseases', [])
        doctor = Doctor.objects.create(**validated_data)
        if diseases:
            doctor.diseases.set(diseases)
        return doctor

    def update(self, instance, validated_data):
        diseases = validated_data.pop('diseases', None)
        profile_image = validated_data.pop('profile_image', None)
        license_pdf = validated_data.pop('license_pdf', None)
        # In this MongoDB setup we may have legacy documents without a usable PK.
        if not getattr(instance, 'pk', None):
            if profile_image or license_pdf:
                errors = {}
                if profile_image:
                    errors['profile_image'] = 'Cannot update this file field for a legacy record without a primary key.'
                if license_pdf:
                    errors['license_pdf'] = 'Cannot update this file field for a legacy record without a primary key.'
                raise serializers.ValidationError(errors)
            if diseases is not None:
                raise serializers.ValidationError({
                    'diseases': 'Cannot update diseases for a legacy record without a primary key.'
                })

            Doctor.objects.filter(email=instance.email).update(**validated_data)
            return Doctor.objects.get(email=instance.email)

        update_data = dict(validated_data)
        if profile_image is not None:
            instance.profile_image.save(profile_image.name, profile_image, save=False)
            update_data['profile_image'] = instance.profile_image.name
        if license_pdf is not None:
            instance.license_pdf.save(license_pdf.name, license_pdf, save=False)
            update_data['license_pdf'] = instance.license_pdf.name

        Doctor.objects.filter(email=instance.email).update(**update_data)
        instance = Doctor.objects.get(email=instance.email)
        if diseases is not None:
            instance.diseases.set(diseases)
        return instance

    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.profile_image and request:
            return request.build_absolute_uri(obj.profile_image.url)
        return ''

    def get_license_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.license_pdf and request:
            return request.build_absolute_uri(obj.license_pdf.url)
        return ''
