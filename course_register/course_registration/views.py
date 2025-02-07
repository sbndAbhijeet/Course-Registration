
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm

def register_student(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("registration_success")
    else:
        form = StudentRegistrationForm()
    return render(request, "course_registration/register.html", {"form": form})

def registration_success(request):
    return render(request, "course_registration/success.html")
