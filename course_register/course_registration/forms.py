from django import forms
from .models import StudentRegistration, Course

class StudentRegistrationForm(forms.ModelForm):
    selected_courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.MultipleHiddenInput(),  # Hidden field to store checkboxes data
        required=False
    )

    class Meta:
        model = StudentRegistration
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
