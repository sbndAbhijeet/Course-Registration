

# Register your models here.
from django.contrib import admin
from .models import StudentRegistration

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "semester_applying_for", "submitted_at")
    search_fields = ("name", "email")
    list_filter = ("semester_applying_for",)
