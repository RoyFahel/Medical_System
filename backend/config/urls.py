from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.urls import path, include

def home(request):
    return JsonResponse({
        "message": "Medical API is running",
        "routes": [
            "/api/auth/",
            "/api/doctors/",
            "/api/diseases/",
            "/api/appointments/",
        ]
    })

urlpatterns = [
    path("", home),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/doctors/", include("apps.doctors.urls")),
    path("api/diseases/", include("apps.diseases.urls")),
    path("api/appointments/", include("apps.appointments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)