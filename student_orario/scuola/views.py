from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser, Students, Attendance, Schedule, Subjects
from django.contrib import messages
from .utils import is_teacher
from django.contrib.auth.decorators import user_passes_test

def home(request):
    return render(request, 'schedule.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request,'login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'login.html')


def doLogin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not (username and password):
        messages.error(request, "Заполните все поля")
        return redirect('login')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        if user == "STUDENT":
            return redirect("schedule")
        elif user == "TEACHER":
            return redirect("attendance")
        elif user == "ADMIN":
            return redirect("/admin/")

    login(request, user)
    return redirect('home')

def logout_user(request):
    return redirect('login')

def registration(request):
    return render(request, 'registration.html')

def doRegistration(request):
    if request == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last.name')
        group = request.POST.get('group')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if CustomUser.objects.filter(username=first_name).exists():
            messages.error(request, "Пользователь уже существует")
            return redirect('register')

        user = CustomUser.objects.create_user(username=first_name, password=password)

        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True
            user.is_superuser = False

        if not (first_name and last_name and group and password and confirm_password):
            messages.error(request, "Заполните все поля")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Пароли должны совпадать")
            return redirect('register')

        user.save()
        messages.success(request, "Регистрация успешна!")
        return redirect('login')
    return redirect('register')

def schedule(request):
    schedules = Schedule.objects.all()
    return render(request, 'schedule.html', {'schedules': schedules})

@user_passes_test(is_teacher)
def attendance(request):
    if request.user.customer != "TEACHER":
        return redirect("schedule")
    attendances = Attendance.objects.all()
    return render(request, 'attendance.html', {'attendances': attendances})

def add_student(request):
    if request.method == "POST":
        first_name = request.POST.get("First_name")
        last_name = request.POST.get("last_name")
        group = request.POST.get("group")

        if not (first_name and last_name and group):
            messages.error(request, "Заполните все поля!")
            return redirect("add_student")

        student = CustomUser.objects.create(
            username=f"{first_name.lower()}_{last_name.lower()}",
            first_name=first_name,
            last_name=last_name,
            group=group,
            user_type=CustomUser.STUDENT
        )
        Students.objects.create(user=student, group=group)

        messages.success(request, "Студент успешно добавен")
        return redirect("students_list")

    return render(request, "add_student.html")

def student_list(request):
    students = Students.objects.all()
    return render(request, "students_list.html", {"students": students})

def teachers_list(request):
    teachers = CustomUser.objects.filter(user_type=CustomUser.TEACHER)
    return render(request, "teachers_list.html", {"teachers": teachers})

def add_teachers(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if not (first_name and last_name):
            messages.error(request, "Заполните все поля")
            return redirect("add_teacher")

        teacher = CustomUser.objects.create(
            username=f"{first_name.lower()}_{last_name.lower()}",
            first_name=first_name,
            last_name=last_name,
            user_type=CustomUser.TEACHER
        )

        messages.success(request, "Учитель успешно добавлен")
        return redirect("teachers_list")

    return render(request, "add_teacher.html")

def add_subject(request):
    if request.method == "POST":
        name = request.POST.get("name")
        teacher_id = request.POST.get("teacher_id")

        if not (name and teacher_id):
            messages.error(request, "Заполните все полня")
            return redirect("add_subject")

        teacher = CustomUser.objects.get(id=teacher_id)

        subject = Subjects.objects.create(
            name=name,
            teacher=teacher
        )

        messages.success(request, "Предмет успешно добавлен")
        return render(request, "subjects_list")

    teachers = CustomUser.objects.filter(user_type=CustomUser.TEACHER)
    return render(request, "add_subject.html", {"teachers": teachers})

def subjects_list(request):
    subjects = Subjects.objects.all()
    return render(request, "subjects_list.html", {"subjects": subjects})

def add_schedule(request):
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        day_of_week = request.POST.get("day_of_week")
        start_time = request.POST.get("start_timr")
        end_time = request.POST.get("end_time")
        room = request.POST.get("room")

        if not (subject_id and day_of_week and start_time and end_time and room):
            messages.error(request, "Заполните все поля")
            return redirect("add_schedule")

        subject = Subjects.objects.get(id=subject_id)

        Schedule.objects.create(
            subjects=subject,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            room=room
        )

        messages.success(request, "Расписание успешно добавлено!")
        return redirect("schedule_list")

    subjects = Subjects.objects.all()
    return render(request, "add_schedule.html", {"subjects": subjects})

def schedule_list(request):
    schedule = Schedule.objects.all().order_by("day_of_week", "start_time")
    return render(request, "schedule_list.html", {"schedule": schedule})