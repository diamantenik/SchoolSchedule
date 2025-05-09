from django.contrib import admin
from .models import CustomUser, Students, Subjects, Attendance, Schedule

admin.site.register(CustomUser)
admin.site.register(Students)
admin.site.register(Subjects)
admin.site.register(Attendance)
admin.site.register(Schedule)