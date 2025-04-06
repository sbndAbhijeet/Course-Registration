from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentRegistrationForm
from .models import Course, StudentRegistration, Enrolled, Course
from accounts.models import Student, Faculty
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings

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
            return redirect("registration_success", registration_id=registration.id)
        else:
            print("Form errors:", form.errors)
            messages.error(request, "Please correct the errors below.")
            return render(request, "course_registration/register.html", {"form": form})

    else:
        form = StudentRegistrationForm(instance=registration)

    # print("Logged in user:", request.user.email)  # Debugging (sbndabhijeet@gmail.com)
    # print("Logged in user:", student_email)  # Debugging (202351127@iiitvadodara.ac.in)
    faculty_advisors = Faculty.objects.all()
    print("Faculty Advisors:", list(faculty_advisors))  # Debug: Check if data exists
    return render(request, "course_registration/register.html", {"form": form})

@login_required
def registration_success(request, registration_id):
    print("Session user_type:", request.session.get('user_type'))
    email = request.session.get('student_email')
    try:
        student = Student.objects.get(email=email)
    except Student.DoesNotExist:    
        messages.error(request, "Student profile not found.")
        return redirect('login')
    
    registration = get_object_or_404(StudentRegistration, id=registration_id, student=student)
    
    faculty = registration.faculty
    # Send email to the student
    subject = "Registration Submitted Successfully"
    email_message = (
        f"Dear {registration.student.student_name},\n\n"
        f"Your registration for Semester {registration.semester_applying_for} has been submitted successfully.\n"
        f"It has been assigned to your faculty advisor, {faculty.name}, for review.\n\n"
        f"Please check your dashboard for updates.\n\n"
        f"Regards,\nIIIT Vadodara"
    )
    send_mail(
        subject=subject,
        message=email_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[registration.student.email],
        fail_silently=False,
    )

    # Send email to the faculty
    subject_faculty = "New Registration Assigned for Review"
    email_message_faculty = (
        f"Dear {faculty.name},\n\n"
        f"A new registration from {registration.student.student_name} (Semester {registration.semester_applying_for}) has been assigned to you for review.\n\n"
        f"Please check your dashboard for details.\n\n"
        f"Regards,\nIIIT Vadodara"
    )
    send_mail(
        subject=subject_faculty,
        message=email_message_faculty,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[faculty.email],
        fail_silently=False,
    )


    return render(request, "course_registration/success.html", {"registration": registration})

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

