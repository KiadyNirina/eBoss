from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone

# Create your models here.

class CustomUserManager(BaseUserManager) :
    def create_user(self, email, username, password=None, role='school', **extra_fields):
        if not email :
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields) :
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('school', 'School'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=True)

    #school
    school_name = models.CharField(max_length=100, null=True)
    school_address = models.CharField(max_length=100, null=True)
    school_number = models.IntegerField(null=True)
    school_type = models.CharField(max_length=10, null=True)
    school_level = models.JSONField(null=True)
    school_classes = models.JSONField(null=True)
    
    #student
    student_name = models.CharField(max_length=100, null=True, blank=True)
    student_lastname = models.CharField(max_length=100, null=True, blank=True)
    student_sexe = models.CharField(max_length=10, null=True, blank=True)
    student_address = models.CharField(max_length=100, null=True)
    student_class = models.CharField(max_length=10, null=True, blank=True)
    student_number = models.IntegerField(null=True, blank=True)
    student_birthday_date = models.DateField(null=True, blank=True)
    register_date = models.DateTimeField(null=True, blank=True)
    student_register_number = models.IntegerField(unique=True, null=True, blank=True)
    student_picture = models.ImageField(upload_to='images/students/', null=True, blank=True)
    
    #teacher
    teacher_name = models.CharField(max_length=100, null=True, blank=True)
    teacher_lastname = models.CharField(max_length=100, null=True, blank=True)
    teacher_sexe = models.CharField(max_length=10, null=True, blank=True)
    teacher_classes = models.JSONField(null=True, blank=True)
    teacher_subjects = models.JSONField(null=True, blank=True)
    teacher_number = models.IntegerField(null=True, blank=True)
    teacher_address = models.CharField(max_length=100, null=True) 
    teacher_birthday = models.DateField(null=True, blank=True)
    teacher_register_date = models.DateField(null=True, blank=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='school')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Changez le related_name pour éviter les conflits
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Changez le related_name pour éviter les conflits
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.email
    
class Matiere(models.Model):
    school = models.CharField(max_length=100)
    classe = models.JSONField()
    subject = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.subject
    
class InfoFamiliale(models.Model) :
    student = models.ForeignKey(CustomUser, related_name='student', on_delete=models.CASCADE)
    mother_name = models.CharField(max_length=100)
    mother_lastname = models.CharField(max_length=100)
    mother_profession = models.CharField(max_length=100)
    mother_number = models.IntegerField()
    father_name = models.CharField(max_length=100)
    father_lastname = models.CharField(max_length=100)
    father_profession = models.CharField(max_length=100)
    father_number = models.IntegerField()

    def __str__(self) -> str:
        return self.student
    
class Course(models.Model) :
    date = models.DateTimeField(auto_now_add=True)
    nameSchool = models.CharField(max_length=100)
    classe = models.CharField(max_length=100)
    matiere = models.CharField(max_length=100)
    teacher = models.CharField(max_length=150)
    course = models.CharField(max_length=50)
    course_start = models.TimeField(null=True, blank=True)
    course_end = models.TimeField(null=True, blank=True)
    activities = models.TextField(null=True, blank=True)
    students_missing = models.JSONField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.date
    
class Schedule(models.Model) :
    school = models.CharField(max_length=100)
    classe = models.CharField(max_length=100)
    schedule = models.TextField()

    def __str__(self) -> str:
        return self.school
    
class Note(models.Model) :
    school = models.CharField(max_length=100)
    student = models.CharField(max_length=100)
    classe = models.CharField(max_length=100)
    school_year = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)
    session_start = models.DateField()
    session_end = models.DateField()
    matiere = models.CharField(max_length=50)
    note = models.FloatField()
    coef = models.IntegerField()

    def __str__(self) -> str:
        return self.student

class RegistrationData(models.Model) :
    school = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    student = models.CharField(max_length=100, null=True, blank=True)
    classe = models.CharField(max_length=100, null=True, blank=True)
    prof = models.CharField(max_length=100, blank=True, null=True)
    prof_de = models.JSONField(null=True, blank=True)
    classes = models.JSONField(null=True, blank=True)
    motif = models.TextField()
    somme = models.IntegerField()
    reste = models.IntegerField()

    def __str__(self) -> str:
        return self.school 

# class Message(models.Model):
#     sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField(default=timezone.now)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f'Message from {self.sender} to {self.receiver}'

#     class Meta:
#         ordering = ('-timestamp',)