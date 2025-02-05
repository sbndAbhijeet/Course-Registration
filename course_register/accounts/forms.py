from django import forms
from .models import Student
from django.contrib.auth.hashers import make_password
class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Student
        fields = [
            'student_name', 
            'gender', 
            'college_id', 
            'email', 
            'department', 
            'year_of_study', 
            'phone_number', 
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Validate password match
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        # Validate email format: 9-digit@iiitvadodara.ac.in
        email = cleaned_data.get('email')
        if email:
            student_id_part = email.split('@')[0]
            if not (student_id_part.isdigit() and len(student_id_part) == 9):
                raise forms.ValidationError("Email must be in the format: 9-digit@iiitvadodara.ac.in")
            if not email.endswith("@iiitvadodara.ac.in"):
                raise forms.ValidationError("Only institute emails are allowed!")

        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        student.password = make_password(self.cleaned_data['password'])
        if commit:
            student.save()
        return student