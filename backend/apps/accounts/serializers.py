from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'role', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'password', 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.filter(email=email, is_deleted=False).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')
        attrs['user'] = user
        return attrs

class AuthResponseSerializer(serializers.Serializer):
    user = UserSerializer()

    @staticmethod
    def for_user(user):
        return {
            'user': UserSerializer(user).data,
        }
