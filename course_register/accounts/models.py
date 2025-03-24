from django.db import models
from django.core.exceptions import ValidationError

def validate_email_format(value):
    """Validate email format: {ending with}@iiitvadodara.ac.in"""
    if not value.endswith("@iiitvadodara.ac.in"):
        raise ValidationError("Email must end with @iiitvadodara.ac.in")
    student_id_part = value.split("@")[0]
    
    if not (student_id_part.isdigit() and len(student_id_part) == 9):
        raise ValidationError("Student ID must be a 9-digit number ")
    

class Student(models.Model):
    student_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    college_id = models.CharField(max_length=20)
    email = models.EmailField(primary_key=True, unique=True, validators=[validate_email_format])
    department = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='{% static "images/default.png" %}', null = True, blank = True)

    def __str__(self):
        return self.student_name

class Faculty(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)  # Moved from FacultyAdvisor
    gender = models.CharField(max_length=10)
    department = models.CharField(max_length=100)  # Moved from FacultyAdvisor
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    academic_batch = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='faculty_images/', default='{% static "images/default.png" %}', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name