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
    

class MessSchedule(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK, unique=True)
    breakfast = models.TextField()  # Store breakfast items as a single text field (e.g., "CORN FLAKES\nCHOCOLATE POWDER\n...")
    lunch = models.TextField()      # Store lunch items
    hi_tea = models.TextField()     # Store hi tea items
    dinner = models.TextField()     # Store dinner items

    def __str__(self):
        return f"Mess Schedule for {self.day}"

    class Meta:
        verbose_name = "Mess Schedule"
        verbose_name_plural = "Mess Schedules"

class BusSchedule(models.Model):
    day = models.CharField(max_length=10)  # e.g., "Monday"
    from_location = models.CharField(max_length=50)  # e.g., "Hostel"
    to_location = models.CharField(max_length=50)  # e.g., "Institute"
    time_to_board = models.CharField(max_length=10)  # e.g., "8:30 AM"
    last_time_to_board = models.CharField(max_length=10)  # e.g., "8:55 AM"
    no_of_buses = models.IntegerField()  # e.g., 5
    batch = models.CharField(max_length=50)  # e.g., "2024+2023+2022"
    no_of_students = models.IntegerField()  # e.g., 284
    

    def __str__(self):
        return f"Bus Schedule for {self.day} from {self.from_location} to {self.to_location} at {self.time_to_board}"
    
from accounts.models import Student  # Assuming Student model exists in accounts app

# Model to store Class Schedule
class ClassSchedule(models.Model):
    day = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ])
    room = models.CharField(max_length=20)  # e.g., 9001, 9101
    course_code = models.CharField(max_length=10)  # e.g., MA201, CS203
    section = models.CharField(max_length=10, blank=True, null=True)  # e.g., S1, L1
    semester = models.IntegerField()  # Determined from course_code using UG Curriculum
    start_time = models.TimeField()  # e.g., 9:15
    end_time = models.TimeField()  # e.g., 10:15

    def __str__(self):
        return f"{self.course_code} ({self.section}) on {self.day} from {self.start_time} to {self.end_time} in {self.room}"

# Link Student to their semester (optional, assuming Student model has semester field)
# If not, you can add a semester field to the Student model