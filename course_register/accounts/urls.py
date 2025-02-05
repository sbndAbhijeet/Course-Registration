from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),  # Maps to /login/
    path('signup/', views.signup, name='signup'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
]