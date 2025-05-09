from django.db import models

class CustomUser(models.Model):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN = "ADMIN"

    USER_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Admin'),
    ]

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    group = models.CharField(max_length=150)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    @property
    def is_anonymous(self):
        return not self.is_active

    @property
    def is_authenticated(self):
        return self.is_active

    REQUIRED_FIELDS = ['first_name', 'last_name', 'group']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Students(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    group = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, {self.group}"

class Subjects(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subjects", limit_choices_to={"user_type": CustomUser.TEACHER})
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField()

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.date} {self.present}"

class Schedule(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=200)
    start_time = models.CharField(max_length=100)  # Добавлен max_length
    end_time = models.CharField(max_length=100)    # Добавлен max_length
    room = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject.name} - {self.day_of_week} - {self.start_time} - {self.room}"


    def __str__(self):
        return f"{self.subject.name} - {self.day_of_week} - {self.start_time} - {self.room}"