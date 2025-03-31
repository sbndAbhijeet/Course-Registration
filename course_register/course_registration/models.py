from django.db import models
from accounts.models import Student, Faculty
class Course(models.Model):
    BRANCH_CHOICES = [
        ("CSE", "Computer Science"),
        ("IT", "Information Technology"),
        ("CSE/IT", "Computer Science or Information Technology"),
    ]

    semester = models.IntegerField()
    course_code = models.CharField(max_length=15, default="Unknown")
    name = models.CharField(max_length=255)
    credits = models.CharField(max_length=15)  # Format: "L-T-P : C"
    branch_name = models.CharField(max_length=10, choices=BRANCH_CHOICES, default="CSE/IT")  # Mapping courses to branch

    def __str__(self):
        return f"{self.name} (Semester {self.semester})"

# Need : if you want to distinguish between a registration attempt (StudentRegistration) and confirmed enrollment (Enrolled), perhaps after admin approval or fee verification.

class StudentRegistration(models.Model):
    SEMESTER_CHOICES = [(str(i), f"Semester {i}") for i in range(1, 9)]  # Semesters 1 to 8
    BRANCH_CHOICES = [
        ("CSE", "Computer Science Engineering"),
        ("IT", "Information Technology"),
        ("CSE/IT", "Computer Science or Information Technology"),
    ]
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Issues', 'Issues'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, to_field="email", related_name="registrations")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    previous_spi = models.FloatField()
    previous_cpi = models.FloatField()
    branch_name = models.CharField(max_length=10, choices=BRANCH_CHOICES, default="CSE/IT")  # Restrict to CSE or IT
    semester_applying_for = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    selected_courses = models.ManyToManyField(Course)  # ✅ Fix
    # program_electives = models.TextField(help_text="Comma-separated list of program electives", blank=True, null=True)
    # open_electives = models.TextField(help_text="Comma-separated list of open electives", blank=True, null=True)
    college_fee_proof = models.FileField(upload_to="fee_documents/")
    hostel_fee_proof = models.FileField(upload_to="fee_documents/")
    loan_refund_form = models.FileField(upload_to="fee_documents/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='In Progress')  # Updated status field
    message = models.TextField(max_length=500, blank=True, null=True, help_text="Message from faculty regarding the registration status.")


    def __str__(self):
        return f"{self.name} - Semester {self.semester_applying_for}"



class Enrolled(models.Model):
    student = models.OneToOneField(Student, on_delete= models.CASCADE)
    selected_courses = models.ManyToManyField(Course)
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Enrollment - {self.student.student_name}"
