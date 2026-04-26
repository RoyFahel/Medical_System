from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User
from .permissions import IsAdmin
from .serializers import RegisterSerializer, LoginSerializer, AuthResponseSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(AuthResponseSerializer.for_user(user), status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(AuthResponseSerializer.for_user(user))

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_deleted=False).order_by('-created_at')
