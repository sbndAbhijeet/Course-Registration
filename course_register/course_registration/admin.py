from django.contrib import admin
from .models import Course, FacultyAdvisor, StudentRegistration, Enrolled

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'name', 'semester', 'branch_name', 'credits')
    list_filter = ('semester', 'branch_name')
    search_fields = ('course_code', 'name')

@admin.register(FacultyAdvisor)
class FacultyAdvisorAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'name', 'email', 'academic_batch')
    
    search_fields = ('name', 'email')

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'semester_applying_for', 'branch_name', 'faculty')
    filter_horizontal = ('selected_courses',)  # Use a horizontal multi-select widget
    readonly_fields = ('submitted_at',)

@admin.register(Enrolled)
class EnrolledAdmin(admin.ModelAdmin):
    list_display = ('get_student_email', 'college_id', 'faculty')  # Use a custom method
    filter_horizontal = ('selected_courses',)

    def get_student_email(self, obj):
        return obj.student.email
    get_student_email.short_description = 'Student Email'