from django.contrib import admin
from .models import StudentRegistration, Course

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "semester_applying_for", "submitted_at")
    search_fields = ("name", "email")
    list_filter = ("semester_applying_for",)
    filter_horizontal = ("selected_courses",)  # ✅ Allows selecting multiple courses in admin panel

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "semester", "credits")
