from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, SignupForm
from .models import Student
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib import messages
from course_registration.models import Course, FacultyAdvisor, StudentRegistration
from django.contrib.auth.decorators import login_required
from .models import Student
from django.contrib.auth import authenticate, login, logout



# Helper function to check if the user is logged in
def is_authenticated(request):
    return request.user.is_authenticated or 'student_email' in request.session

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                student = Student.objects.get(email=username)
                if check_password(password, student.password):
                    # Set session variable to indicate the user is logged in
                    request.session['student_email'] = student.email
                    messages.success(request, "Logged in successfully!")
                    return redirect('dashboard')
                else:
                    form.add_error(None, "Invalid credentials.")
            except Student.DoesNotExist:
                form.add_error(None, "User does not exist.")
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
        messages.success(request, "Logged out successfully!")
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save data temporarily in session
            request.session['signup_data'] = form.cleaned_data

            # Generate and send OTP
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            email = form.cleaned_data['email']
            send_mail(
                "OTP Verification",
                f"Your OTP is {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('otp_verification')
        else:
            # Show form errors if validation fails
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def dashboard(request):
    # Check if the user is logged in
    if not is_authenticated(request):
        messages.error(request, "You need to log in to access this page.")
        return redirect('login')
    
    return render(request, 'accounts/dashboard.html')

def otp_verification(request):
    # Check if the user is logged in (optional, since this is part of the signup process)
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        email = request.session.get('email_for_reset')

        if not email:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('login')
        
        if user_otp == stored_otp:
            if 'email_for_reset' in request.session:
                #otp verified for password reset
                return redirect('reset_password')
        
            else:
                # OTP verified for signup (existing logic)
                if str(user_otp) == str(stored_otp):
                    # Save data to database
                    signup_data = request.session.get('signup_data')
                    form = SignupForm(signup_data)
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Account created! Please login.")
                        del request.session['signup_data']
                        del request.session['otp']
                        return redirect('login')
                    else:
                        messages.error(request, "Error saving data. Please try again.")
                else:
                    messages.error(request, "Invalid OTP!")
                    return redirect('signup')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('otp_verification')
    
    return render(request, 'accounts/otp_verification.html')

def all_courses(request):
    courses = Course.objects.all().order_by('semester', 'branch_name')
    # print(courses)
    return render(request, 'accounts/all_courses.html', {'courses': courses})


def contact_us(request):
    faculty_advisors = FacultyAdvisor.objects.all()
    print("Faculty Advisors fetched:", list(faculty_advisors))  # Debug
    return render(request, 'accounts/contact_us.html', {'faculty_advisors': faculty_advisors})

@login_required
def dashboard(request):
    student_email = request.session.get("student_email")
    if not student_email:
        return redirect('login')
    
    student = get_object_or_404(Student, email=student_email)
    registration = StudentRegistration.objects.filter(student=student).first()
    
    return render(request, 'accounts/dashboard.html', {
        'student': student,
        'registration': registration,
    })