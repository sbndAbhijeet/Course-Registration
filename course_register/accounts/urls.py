from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import view_excel_file
urlpatterns = [
    path('', views.login, name='login'),  # Maps to /login/
    path('login/', views.login, name='login'),
    path('accounts/dashboard/', views.dashboard, name='dashboard'),
    path('accounts/faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('signup/', views.signup, name='signup'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('logout/', views.logout, name='logout'),
    path('all_courses/', views.all_courses, name='all_courses'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('profile/', views.profile, name='profile'),
    path('faculty_profile/', views.profile, name='faculty_profile'),
    path('registration/<int:registration_id>/', views.registration_details, name='registration_details'),
    path('update_registration_status/<int:registration_id>/', views.update_registration_status, name='update_registration_status'),

    path('bus_schedule/', views.bus_schedule, name='bus_schedule'),
    path('mess_schedule/', views.mess_schedule, name='mess_schedule'),
    path('class_schedule/', views.class_schedule, name='class_schedule'),
    path('view-excel/', view_excel_file, name='view_excel'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)