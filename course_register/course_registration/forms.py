from django import forms
from .models import StudentRegistration, Course, FacultyAdvisor

class StudentRegistrationForm(forms.ModelForm):
    selected_courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple, # Use checkboxes instead of hidden field
        required=False
    )
    
    faculty = forms.ModelChoiceField(
        queryset=FacultyAdvisor.objects.all(),
        empty_label = 'Select Faculty Advisor',
        required = True
    )

    class Meta:
        model = StudentRegistration
        fields = [
            'previous_spi', 'previous_cpi', 'semester_applying_for',
            'selected_courses', 'faculty', 'college_fee_proof',
            'hostel_fee_proof', 'loan_refund_form'
        ]
        # Exclude fields set in the view
        exclude = ['student', 'email', 'name', 'branch_name', 'submitted_at']
        # fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
