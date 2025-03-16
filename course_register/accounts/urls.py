from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # Maps to /login/
    path('signup/', views.signup, name='signup'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('all_courses/', views.all_courses, name='all_courses'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
]