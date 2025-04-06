from django import forms
from .models import Student, Faculty
from django.contrib.auth.hashers import make_password
import os
import re
import logging

logger = logging.getLogger("accounts.views")
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100) 
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(
        choices=[
            ('student', 'Student'),
            ('faculty', 'Faculty'),
        ],
        required = True,
        label='Select Your Role',
    )


class SignupForm(forms.Form):
   role = forms.ChoiceField(choices=[('student', 'Student'), ('faculty', 'Faculty')], label='Select Your Role')
   student_name = forms.CharField(max_length=100, label='Name')
   gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], label='Gender')
   college_id = forms.CharField(max_length=20, label='College ID', required=False)
   email = forms.EmailField(label='Email')
   department = forms.CharField(max_length=100, label='Department')
   year_of_study = forms.CharField(max_length=10, label='Year of Study', required=False)
   phone_number = forms.CharField(max_length=15, label='Phone Number')
   password = forms.CharField(widget=forms.PasswordInput, label='Password', min_length=8)
   confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password') # A confirmation password field
   address = forms.CharField(widget=forms.Textarea, label='Address', required=False)
   date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label='Date of Birth')
   secret_code = forms.CharField(max_length=50, label='Secret Code (for Faculty)', required=False) # added for faculty signup
   
   def clean_email(self):
        email = self.cleaned_data.get('email')
        role = self.cleaned_data.get('role')

        logger.info(f"Validating email: {email}, Role: {role}")
        local_part = email.split('@')[0]

        if role == 'student':
            if not email.endswith('@iiitvadodara.ac.in'):
                raise forms.ValidationError("Please use your institute email (ending with @iiitvadodara.ac.in)")
            if not local_part.startswith(tuple(str(i) for i in range(10))):
                raise forms.ValidationError("Student email must start with a 9-digit ID (e.g., 202351127@iiitvadodara.ac.in)")
            if not (local_part.isdigit() and len(local_part) == 9):
                raise forms.ValidationError("Student email must start with a 9-digit ID (e.g., 202351127@iiitvadodara.ac.in)")
        elif role == 'faculty':
            if not email.endswith('@gmail.com'):
                raise forms.ValidationError("Please use your institute email (ending with @gmail.com)")

        # Debug: Get the actual records
        student_records = Student.objects.filter(email__iexact=email)
        faculty_records = Faculty.objects.filter(email__iexact=email)

        student_exists = student_records.exists()
        faculty_exists = faculty_records.exists()

        logger.info(f"Student exists: {student_exists}, Faculty exists: {faculty_exists}")
        logger.info(f"Student records: {list(student_records)}")
        logger.info(f"Faculty records: {list(faculty_records)}")

        if student_exists:
            raise forms.ValidationError("This email is already registered as a student.")
        if faculty_exists:
            raise forms.ValidationError("This email is already registered as a faculty member.")
        return email
   
   def clean_password(self):
    password = self.cleaned_data.get('password')
    if password:
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
    return password
   
   def clean(self):
       cleaned_data = super().clean()
       role = cleaned_data.get('role')
       college_id = cleaned_data.get('college_id')
       year_of_study = cleaned_data.get('year_of_study')
       secret_code = cleaned_data.get('secret_code')
       password = cleaned_data.get('password')
       confirm_password = cleaned_data.get('confirm_password')

       #Validate that password and confirm password match
       if password and confirm_password and password != confirm_password:
           raise forms.ValidationError('Passwords do not match')
       
       if role == 'student':
           if not college_id:
               raise forms.ValidationError('Please enter your college ID')
           if not year_of_study:
               raise forms.ValidationError('Please enter your year of study')

       elif role == 'faculty':
           FACULTY_SECRET_CODE = os.getenv('FACULTY_SECRET_CODE')
           if secret_code != FACULTY_SECRET_CODE:
               raise forms.ValidationError('Invalid secret code for faculty signup.')

       return cleaned_data
   
   def save(self):
    role = self.cleaned_data['role']
    email = self.cleaned_data['email'].lower()
    password = make_password(self.cleaned_data['password'])

    if role == 'student':
        student = Student(
            student_name=self.cleaned_data['student_name'],
            gender=self.cleaned_data['gender'],
            college_id=self.cleaned_data['college_id'],
            email=email,
            department=self.cleaned_data['department'],
            year_of_study=self.cleaned_data['year_of_study'],
            phone_number=self.cleaned_data['phone_number'],
            password=password,
            address=self.cleaned_data['address'],
            date_of_birth=self.cleaned_data['date_of_birth'],
        )
        student.save()
        return student
    else:  # Faculty
        faculty = Faculty(
            email=email,
            name=self.cleaned_data['student_name'],
            department=self.cleaned_data['department'],
            password=password,
            phone_number=self.cleaned_data['phone_number'],
        )
        faculty.save()
        return faculty
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email  # Temporarily disable all validations