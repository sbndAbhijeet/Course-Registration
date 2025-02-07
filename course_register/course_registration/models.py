from django.db import models

class StudentRegistration(models.Model):
    SEMESTER_CHOICES = [(str(i), f"Semester {i}") for i in range(1, 9)]  # Semesters 1 to 8

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    previous_spi = models.FloatField()
    previous_cpi = models.FloatField()
    semester_applying_for = models.CharField(max_length=2, choices=SEMESTER_CHOICES)

    selected_courses = models.TextField(help_text="Comma-separated list of selected courses")
    program_electives = models.TextField(help_text="Comma-separated list of program electives")
    open_electives = models.TextField(help_text="Comma-separated list of open electives")

    college_fee_proof = models.FileField(upload_to="fee_documents/")
    hostel_fee_proof = models.FileField(upload_to="fee_documents/")
    loan_refund_form = models.FileField(upload_to="fee_documents/", blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Semester {self.semester_applying_for}"
