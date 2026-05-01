from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    AuthResponseSerializer,
    UserSerializer,
)
from .permissions import IsAdminHeader


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            AuthResponseSerializer.for_user(user),
            status=status.HTTP_201_CREATED
        )


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        return Response(AuthResponseSerializer.for_user(user))


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminHeader]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(is_deleted=False).order_by("-created_at")

        current_email = self.request.headers.get("X-User-Email")
        if current_email:
            queryset = queryset.exclude(email__iexact=current_email)

        return queryset
    
class UserRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminHeader]
    serializer_class = UserSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return User.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()