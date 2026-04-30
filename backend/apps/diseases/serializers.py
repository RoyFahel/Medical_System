from rest_framework import serializers
from .models import Disease


class DiseaseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Disease
        fields = [
            "id", "name", "description", "symptoms", "prevention",
            "image", "image_url", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return ""
