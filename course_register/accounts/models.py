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

    def __str__(self):
        return self.student_name
