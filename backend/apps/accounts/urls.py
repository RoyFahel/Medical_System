from django.urls import path
from .views import RegisterView, LoginView, UserListView, UserRetrieveDestroyView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UserListView.as_view(), name="users"),
    path("users/<str:id>/", UserRetrieveDestroyView.as_view(), name="user-detail"),
]