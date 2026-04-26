from rest_framework import serializers
from .models import Disease

class DiseaseSerializer(serializers.ModelSerializer):
    # With the MongoDB backend, the primary key can be an ObjectId; expose it as a string.
    id = serializers.CharField(source='pk', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Disease
        fields = ['id', 'name', 'description', 'symptoms', 'prevention', 'image', 'image_url', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Same legacy-PK issue as other models in this MongoDB setup.
        if not getattr(instance, 'pk', None):
            if 'image' in validated_data:
                raise serializers.ValidationError({
                    'image': 'Cannot update image for a legacy record without a primary key.'
                })
            Disease.objects.filter(name=instance.name).update(**validated_data)
            return Disease.objects.get(name=instance.name)

        return super().update(instance, validated_data)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return ''
