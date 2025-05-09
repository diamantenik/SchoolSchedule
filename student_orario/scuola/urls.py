from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_user, name="login"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout', views.logout_user, name="logout"),
    path('register/', views.registration, name="register"),
    path('doRegister/', views.doRegistration, name="doRegister"),
    path('schedule/', views.schedule, name="schedule"),
    path('attendance/', views.attendance, name="attendance"),
    path('add_student/', views.add_student, name="add_student"),
    path('student_list/', views.student_list, name="student_list"),
    path('add_teachers/', views.add_teachers, name="add_teacher"),
    path('teachers_list/', views.teachers_list, name="teachers_list"),
    path('add_subject/', views.add_subject, name="add_subject"),
    path('subjects_list/', views.subjects_list, name="subjects_list"),
    path('add_schedule/', views.add_schedule, name="add_schedule"),
    path('schedule_list/', views.schedule_list, name="schedule_list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)