from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from .models import Student
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib import messages


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                student = Student.objects.get(email=username)
                if check_password(password, student.password):
                    # Redirect to dashboard
                    return redirect('dashboard')
                else:
                    form.add_error(None, "Invalid credentials.")
            except Student.DoesNotExist:
                form.add_error(None, "User does not exist.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

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
    return render(request, 'accounts/dashboard.html')

def otp_verification(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

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
    
    return render(request, 'accounts/otp_verification.html')