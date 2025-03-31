from django.shortcuts import render, redirect, get_object_or_404
import datetime
from .forms import LoginForm, SignupForm
from .models import Student, Faculty,MessSchedule,BusSchedule
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib import messages
from course_registration.models import Course, StudentRegistration
from django.contrib.auth.decorators import login_required
from .models import Student
from django.contrib.auth import authenticate, login, logout
import logging
from course_registration.models import StudentRegistration, Enrolled
import os
# Define the logger at the top of the file
logger = logging.getLogger(__name__)



# Helper function to check if the user is logged in
def is_authenticated(request):
    return request.user.is_authenticated or 'student_email' in request.session

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            logger.info(f"Login attempt with username: {username}, role: {role}")
            try:
                student = Student.objects.get(email=username)
                if check_password(password, student.password):
                    # Set session variable to indicate the user is logged in
                    request.session['student_email'] = student.email
                    request.session['role'] = 'student'
                    print('role: ', request.session['role'])
                    
                    messages.success(request, "Logged in successfully!")
                    return redirect('dashboard')
                else:
                    form.add_error(None, "Invalid credentials.")
            except Student.DoesNotExist:
                try:
                    faculty = Faculty.objects.get(email=username)
                    if check_password(password, faculty.password):
                        request.session['faculty_email'] = faculty.email
                        request.session['role'] = 'faculty'
                        print('role: ', request.session['role'])
                        messages.success(request, "Logged in successfully!")
                        return redirect('faculty_dashboard')
                    else:
                        messages.error(request, "Invalid credentials.")
                except Faculty.DoesNotExist:
                    messages.error(request, "User does not exist.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            student = Student.objects.get(email=email)
            if not email.endswith('@iiitvadodara.ac.in'):
                messages.error(request, 'Please use your institute email (ending with @iiitvadodara.ac.in)')
                return redirect('forgot_password')
            #generate otp
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['email_for_reset'] = email
            #send otp via email
            send_mail(
                'Password Reset OTP - IIIT Vadodara',
                f'Your OTP for password reset is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent successfully!')
            return redirect('otp_verification')
        except Student.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return render(request, 'accounts/forgot_password.html')

    return render(request, 'accounts/forgot_password.html')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('email_for_reset')

        if not email:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('forgot_password')
        
        try:
            student = Student.objects.get(email=email)
            #Hash the new password manually
            hashed_password = make_password(password)
            student.password = hashed_password # Update the password field
            student.save()
            del request.session['email_for_reset']
            del request.session['otp']
            messages.success(request, 'Password reset successfully! Please log in.')
            return redirect('login')
        except Student.DoesNotExist:
            messages.error(request, 'No student found with this email.')
            return redirect('forgot_password')

    return render(request, 'accounts/reset_password.html')

def logout(request):
    if 'student_email' in request.session:
        del request.session['student_email']  # Clear session
        del request.session['role']
        messages.success(request, "Logged out successfully!")
    return redirect('login')

def signup(request):
    if request.method == 'GET':
        # Clear session data only on GET requests
        if 'signup_data' in request.session:
            del request.session['signup_data']
        if 'otp' in request.session:
            del request.session['otp']
        if 'signup_role' in request.session:
            del request.session['signup_role']
        logger.info(f"Session after clearing (GET): {request.session.items()}")

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            request.session['signup_data'] = form.cleaned_data
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['signup_role'] = form.cleaned_data['role']
            email = form.cleaned_data['email']
            logger.info(f"Session after setting data: {request.session.items()}")
            send_mail(
                "OTP Verification",
                f"Your OTP is {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('otp_verification')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})
# def dashboard(request):
#     # Check if the user is logged in
#     if not is_authenticated(request):
#         messages.error(request, "You need to log in to access this page.")
#         return redirect('login')
    
#     return render(request, 'accounts/dashboard.html')

def otp_verification(request):
    logger.info(f"Session at start of otp_verification: {request.session.items()}")

    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        # Check if OTP exists in session
        if not stored_otp:
            messages.error(request, 'Session expired or OTP not found. Please try again.')
            return redirect('login')

        # Check if the OTP matches
        if str(user_otp) != str(stored_otp):
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('otp_verification')

        # Determine the flow: Forgot Password or Signup
        if 'email_for_reset' in request.session:
            # Forgot Password flow
            email = request.session.get('email_for_reset')
            if not email:
                messages.error(request, 'Session expired. Please try again.')
                return redirect('login')
            logger.info(f"OTP verified for password reset for email: {email}")
            return redirect('reset_password')
        else:
            # Signup flow
            signup_data = request.session.get('signup_data')
            if not signup_data:
                messages.error(request, 'Session expired or signup data not found. Please try again.')
                return redirect('signup')

            email = signup_data.get('email')
            if not email:
                messages.error(request, 'Email not found in signup data. Please try again.')
                return redirect('signup')

            # Save the user to the database
            form = SignupForm(signup_data)
            if form.is_valid():
                form.save()
                messages.success(request, "Account created successfully! Please login.")
                # Clean up session
                del request.session['signup_data']
                del request.session['otp']
                logger.info(f"Account created for email: {email}")
                return redirect('login')
            else:
                messages.error(request, "Error saving data. Please try again.")
                logger.error(f"Form errors during signup: {form.errors}")
                return redirect('signup')

    return render(request, 'accounts/otp_verification.html')

def all_courses(request):
    courses = Course.objects.all().order_by('semester', 'branch_name')
    # print(courses)
    return render(request, 'accounts/all_courses.html', {'courses': courses})


def contact_us(request):
    faculty_advisors = Faculty.objects.all()
    print("Faculty Advisors fetched:", list(faculty_advisors))  # Debug
    return render(request, 'accounts/contact_us.html', {'faculty_advisors': faculty_advisors})

@login_required
def dashboard(request):
    student_email = request.session.get("student_email")
    print('role: ', request.session['role'])
    if not student_email:
        return redirect('login')
    
    student = get_object_or_404(Student, email=student_email)

    # Fetch the most recent submitted registration
    registration = StudentRegistration.objects.filter(student=student).first()
    
    return render(request, 'accounts/dashboard.html', {
        'student': student,
        'registration': registration,
    })



@login_required
def faculty_dashboard(request):
    faculty_email = request.session.get('faculty_email')
    print('role: ', request.session['role'])
    if not faculty_email:
        messages.error(request, "User session expired. Please log in again.")
        return redirect('login')
    
    faculty = get_object_or_404(Faculty, email=faculty_email)
    registrations = StudentRegistration.objects.filter(faculty=faculty)

    return render(request, 'accounts/faculty_dashboard.html', {
        'faculty': faculty,
        'registrations': registrations,
    })

@login_required
def registration_details(request, registration_id):
    faculty_email = request.session.get('faculty_email')
    print('role: ', request.session['role'])
    if not faculty_email:
        messages.error(request, "User session expired. Please log in again.")
        return redirect('login')
    
    faculty = get_object_or_404(Faculty, email=faculty_email)
    # Fetch the specific registration
    registration = get_object_or_404(StudentRegistration, id=registration_id)

    # Ensure the registration is assigned to this faculty
    if registration.faculty != faculty:
        messages.error(request, "You are not authorized to view this registration.")
        return redirect('faculty_dashboard')

    return render(request, 'accounts/registration_details.html', {'registration': registration, 'faculty': faculty})

@login_required
def profile(request):
    student_email = request.session.get("student_email")
    if not student_email:
        return redirect('login?toast_type=error&toast_title=Error&toast_message=You need to log in to access this page.')

    student = get_object_or_404(Student, email=student_email)

    if request.method == 'POST':
        student.student_name = request.POST.get('student_name', student.student_name)
        student.gender = request.POST.get('gender', student.gender)
        student.college_id = request.POST.get('college_id', student.college_id)
        student.department = request.POST.get('department', student.department)
        student.year_of_study = request.POST.get('year_of_study', student.year_of_study)
        student.phone_number = request.POST.get('phone_number', student.phone_number)
        student.address = request.POST.get('address', student.address)
        student.date_of_birth = request.POST.get('date_of_birth', student.date_of_birth)

        # Handle password change (only if provided)
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if new_password:
            student.password = make_password(new_password)

        # Handle profile image upload
        if 'profile_image' in request.FILES:
            student.profile_image = request.FILES['profile_image']

        student.save()
        return redirect('profile')  # Redirect back to profile page

    return render(request, 'accounts/profile.html', {'student': student})


# Implement the Status Update Logic
# We need to create a new view to handle the status update, add a URL pattern for it, and ensure the change is reflected on both dashboards.

def update_registration_status(request, registration_id):
    email = request.session.get('faculty_email')
    print('role: ', request.session['role'])
    if not email:
        messages.error(request, "User session expired. Please log in again.")
        return redirect('login')
    
    try:
        faculty = Faculty.objects.get(email=email)
    except Faculty.DoesNotExist:
        messages.error(request, "Faculty profile not found.")
        return redirect('login')
    
    registration = get_object_or_404(StudentRegistration, id=registration_id)

    # Ensure the registration is assigned to this faculty
    if registration.faculty != faculty:
        messages.error(request, "You are not authorized to update this registration.")
        return redirect('faculty_dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        message = request.POST.get('message')
        if new_status in ['In Progress', 'Issues', 'Rejected', 'Accepted']:
            registration.status = new_status
            registration.message = message
            registration.save()
            messages.success(request, f"Status updated to '{new_status}' for {registration.student.student_name}.")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('registration_details', registration_id=registration_id)


def class_schedule(request):
    return render(request, 'accounts/class_schedule.html')

def bus_schedule(request):
    return render(request, 'accounts/bus_schedule.html')

def mess_schedule(request):
    email = request.session.get('student_email')
    if not email:
        messages.error(request, "User session expired. Please log in again.")
        return redirect('login')

    # Fetch the mess schedule, ordered by ID to maintain Monday to Sunday order
    schedules = MessSchedule.objects.all().order_by('id')

    return render(request, 'accounts/mess_schedule.html', {
        'schedules': schedules,
        'request': request,
    })

def bus_schedule(request):
    
    email = request.session.get('student_email')
    if not email:
        messages.error(request, "User session expired. Please log in again.")
        return redirect('login')

    # Fetch bus schedules and group by day
    schedules = BusSchedule.objects.all()
    # current_day = datetime.now().strftime('%A')

    # Group schedules by day for the template
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    schedules_by_day = {day: [] for day in days}
    for schedule in schedules:
        if schedule.day in days:
            schedules_by_day[schedule.day].append(schedule)

    return render(request, 'accounts/bus_schedule.html', {
        'schedules_by_day': schedules_by_day,
        # 'current_day': current_day,
    })

def view_excel_file(request):
    excel_path = os.path.join(settings.MEDIA_URL, '2024-25_academic_planning.xlsx')
    return redirect(excel_path)

def class_schedule_view(request):
    return render(request, "class_schedule.html")