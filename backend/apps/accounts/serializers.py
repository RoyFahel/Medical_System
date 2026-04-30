from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "role", "created_at", "updated_at"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        # Public registration is patient-only. Do not accept role from frontend.
        fields = ["id", "full_name", "email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value, is_deleted=False).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value.lower()

    def create(self, validated_data):
        validated_data["role"] = "patient"
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email", "").lower()
        password = attrs.get("password")
        user = User.objects.filter(email__iexact=email, is_deleted=False).first()
        if not user or user.password != password:
            raise serializers.ValidationError("Invalid email or password")
        attrs["user"] = user
        return attrs


class AuthResponseSerializer(serializers.Serializer):
    user = UserSerializer()

    @staticmethod
    def for_user(user):
        return {"user": UserSerializer(user).data}
