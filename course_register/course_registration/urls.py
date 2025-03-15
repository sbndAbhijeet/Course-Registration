from django.urls import path
from .views import register_student, registration_success, get_courses
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("register/", register_student, name="register_student"),
    path("success/", registration_success, name="registration_success"),
    path("get_courses/", get_courses, name="get_courses"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)