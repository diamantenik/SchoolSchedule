def is_teacher(user):
    return user.is_authenticated and user == "TEACHER"

def is_student(user):
    return user.is_authenticated and user == "STUDENT"

def is_admin(user):
    return user.is_authenticated and user == "ADMIN"