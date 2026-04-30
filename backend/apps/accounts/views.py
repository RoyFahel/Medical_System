from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, AuthResponseSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(AuthResponseSerializer.for_user(user), status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(AuthResponseSerializer.for_user(user))


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_object(self):
        # This project currently uses simple localStorage auth in Angular.
        # Profile is not used by the frontend, so return the first active user as a safe fallback.
        return User.objects.filter(is_deleted=False).first()


class UserListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_deleted=False).order_by("-created_at")
