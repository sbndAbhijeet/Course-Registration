from django.contrib import admin
from .models import Student, Faculty, MessSchedule,BusSchedule
# Register your models here.
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(MessSchedule)
admin.site.register(BusSchedule)