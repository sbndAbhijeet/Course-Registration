from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from .models import Course, StudentRegistration
from django.contrib import messages

# Helper function to check if the user is logged in
def is_authenticated(request):
    return 'student_email' in request.session

def register_student(request):
    # Check if the user is logged in
    if not is_authenticated(request):
        messages.error(request, "You need to log in to access this page.")
        return redirect('login')  # Redirect to the login page

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST, request.FILES)  # Handle form & file data

        if form.is_valid():
            student = form.save(commit=False)  # Save the form but do not commit to DB yet
            student.save()  # Save student record first

            # ✅ Get selected courses properly and ensure they are valid Course objects
            selected_course_ids = request.POST.getlist("selected_courses")  # Get selected courses as list
            valid_courses = Course.objects.filter(id__in=selected_course_ids)  # Fetch valid Course objects
            student.selected_courses.set(valid_courses)  # Assign Many-to-Many field properly

            return render(request, "course_registration/success.html")

    else:
        form = StudentRegistrationForm()

    return render(request, "course_registration/register.html", {"form": form})

def registration_success(request):
    # Check if the user is logged in
    if not is_authenticated(request):
        messages.error(request, "You need to log in to access this page.")
        return redirect('login')  # Redirect to the login page

    return render(request, "course_registration/success.html")

def get_courses(request):
    # This view does not require authentication since it's used for AJAX requests
    semester = request.GET.get("semester")
    if semester:
        try:
            semester = int(semester)  # Convert to integer
            courses = Course.objects.filter(semester=semester).values("id", "name", "credits")
            return JsonResponse(list(courses), safe=False)
        except ValueError:
            return JsonResponse({"error": "Invalid semester value"}, status=400)
    return JsonResponse({"error": "No semester provided"}, status=400)