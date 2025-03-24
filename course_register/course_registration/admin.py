from django.contrib import admin
from .models import Course, StudentRegistration, Enrolled

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'name', 'semester', 'branch_name', 'credits')
    list_filter = ('semester', 'branch_name')
    search_fields = ('course_code', 'name')



@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'semester_applying_for', 'branch_name', 'faculty')
    filter_horizontal = ('selected_courses',)  # Use a horizontal multi-select widget
    readonly_fields = ('submitted_at',)

@admin.register(Enrolled)
class EnrolledAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'get_college_id', 'faculty']  # Use a method to get college_id
    filter_horizontal = ('selected_courses',)


    def student_name(self, obj):
        return obj.student.student_name
    student_name.short_description = 'Student Name'  # Set a readable name for the column

    def get_college_id(self, obj):
        return obj.student.college_id
    get_college_id.short_description = 'College ID'  # Set a readable name for the column