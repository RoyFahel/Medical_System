from django.urls import path
from .views import DiseaseListCreateView, DiseaseRetrieveUpdateDestroyView

urlpatterns = [
    path('', DiseaseListCreateView.as_view(), name='disease-list-create'),
    path('<str:pk>/', DiseaseRetrieveUpdateDestroyView.as_view(), name='disease-detail'),
]
