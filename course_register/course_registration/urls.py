from django.urls import path
from .views import register_student, registration_success, get_courses

urlpatterns = [
    path("register/", register_student, name="register_student"),
    path("success/", registration_success, name="registration_success"),
    path("get_courses/", get_courses, name="get_courses"),
]
