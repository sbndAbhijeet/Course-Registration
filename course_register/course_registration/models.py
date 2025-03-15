from django.db import models
from accounts.models import Student 
class Course(models.Model):
    BRANCH_CHOICES = [
        ("CSE", "Computer Science"),
        ("IT", "Information Technology"),
        ("CSE/IT", "Computer Science or Information Technology"),
    ]

    semester = models.IntegerField()
    course_code = models.CharField(max_length=10, default="Unknown")
    name = models.CharField(max_length=255)
    credits = models.CharField(max_length=10)  # Format: "L-T-P : C"
    branch_name = models.CharField(max_length=10, choices=BRANCH_CHOICES, default="CSE/IT")  # Mapping courses to branch

    def __str__(self):
        return f"{self.name} (Semester {self.semester})"

# Need : if you want to distinguish between a registration attempt (StudentRegistration) and confirmed enrollment (Enrolled), perhaps after admin approval or fee verification.
class FacultyAdvisor(models.Model):
    faculty_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(null=False, unique=True) 
    academic_batch = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.name
class StudentRegistration(models.Model):
    SEMESTER_CHOICES = [(str(i), f"Semester {i}") for i in range(1, 9)]  # Semesters 1 to 8
    BRANCH_CHOICES = [
        ("CSE", "Computer Science Engineering"),
        ("IT", "Information Technology"),
        ("CSE/IT", "Computer Science or Information Technology"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, to_field="email", related_name="registrations")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    previous_spi = models.FloatField()
    previous_cpi = models.FloatField()
    branch_name = models.CharField(max_length=10, choices=BRANCH_CHOICES, default="CSE/IT")  # Restrict to CSE or IT
    semester_applying_for = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    faculty = models.ForeignKey(FacultyAdvisor, on_delete=models.SET_NULL, null=True)

    selected_courses = models.ManyToManyField(Course)  # ✅ Fix
    # program_electives = models.TextField(help_text="Comma-separated list of program electives", blank=True, null=True)
    # open_electives = models.TextField(help_text="Comma-separated list of open electives", blank=True, null=True)

    college_fee_proof = models.FileField(upload_to="fee_documents/")
    hostel_fee_proof = models.FileField(upload_to="fee_documents/")
    loan_refund_form = models.FileField(upload_to="fee_documents/", blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Semester {self.semester_applying_for}"



class Enrolled(models.Model):
    college_id = models.CharField(max_length=20, unique=True)
    student = models.OneToOneField(Student, on_delete= models.CASCADE)
    selected_courses = models.ManyToManyField(Course)
    faculty = models.ForeignKey(FacultyAdvisor, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Enrollment - {self.student.student_name} ({self.college_id})"
