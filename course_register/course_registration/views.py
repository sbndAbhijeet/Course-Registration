from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentRegistrationForm
from .models import Course, StudentRegistration, Enrolled, Course
from accounts.models import Student, Faculty
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout

@login_required
def register_student(request):
    student_email = request.session.get("student_email")

    if not student_email:
        messages.error(request, "User session expired. Please log in again.")
        return redirect('login')
    
    student = get_object_or_404(Student, email=student_email)
    registration = StudentRegistration.objects.filter(student=student).first()
    # try: 
    #     registration = StudentRegistration.objects.get(student = student)
    # except StudentRegistration.DoesNotExist:
    #     registration = None


    if request.method == "POST":
        print("POST data:", request.POST) #debug
        print("Files:", request.FILES)
        
        form = StudentRegistrationForm(request.POST, request.FILES, instance=registration)  # Handle form & file data

        if form.is_valid():
            print("Cleaned Data:", form.cleaned_data)  # Debugging
            registration = form.save(commit=False)  # Save the form but do not commit to DB yet
            registration.student = student
            registration.email = student.email  # Ensure email is set
            registration.name = request.POST.get('name', '')  # Get name from form input
            registration.branch_name = request.POST.get('branch', 'CSE/IT')
            registration.faculty = form.cleaned_data['faculty']
            registration.save()  # Save student record first
            print("Registration saved with id:", registration.id) #confirm save
            form.save_m2m() #save selected courses
            print("ManyToMany saved:", registration.selected_courses.all()) #confirm courses


            try:
                enrolled, created = Enrolled.objects.get_or_create(
                    student=student,
                    defaults={'college_id': student.college_id}
                )
                enrolled.selected_courses.set(registration.selected_courses.all())
                enrolled.faculty = registration.faculty
                enrolled.save()
                print("Enrolled saved with ID:", enrolled.id)
            except Exception as e:
                print("Error saving Enrolled:", str(e))

            messages.success(request, "Registration submitted successfully.")
            return redirect("registration_success")
        else:
            print("Form errors:", form.errors)

            messages.success(request, "Registration submitted successfully.")
            return redirect("registration_success")

    else:
        form = StudentRegistrationForm(instance=registration)

    # print("Logged in user:", request.user.email)  # Debugging (sbndabhijeet@gmail.com)
    # print("Logged in user:", student_email)  # Debugging (202351127@iiitvadodara.ac.in)
    faculty_advisors = Faculty.objects.all()
    print("Faculty Advisors:", list(faculty_advisors))  # Debug: Check if data exists
    return render(request, "course_registration/register.html", {"form": form})

@login_required
def registration_success(request):
    return render(request, "course_registration/success.html")

def get_courses(request):
    # This view does not require authentication since it's used for AJAX requests
    semester = request.GET.get('semester')
    branch = request.GET.get('branch', '')

    if not semester:
        return JsonResponse([], safe=False)
    
    courses = Course.objects.filter(semester=semester)

    if branch:
        print(f"Filtering for branch: {branch}")  # Debugging
        if branch == 'CSE/IT':
            courses = courses.filter(branch_name__in=['CSE', 'IT'])
        else:
            courses = courses.filter(branch_name=branch)

    if not courses.exists():
        print("No courses found!")  # Debugging
        return JsonResponse([], safe=False)

    unique_courses = {course['course_code']: course for course in courses.values('id', 'course_code', 'name', 'credits')}.values()

    return JsonResponse(list(unique_courses), safe=False)

