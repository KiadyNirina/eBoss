from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
        # (3, 'Teacher'),
        # (4, 'Parent')
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=True)
    school_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    school_number = models.IntegerField(null=True)
    school_type = models.CharField(max_length=10, null=True)
    school_level = models.JSONField(null=True)
    school_classes = models.JSONField(null=True)
    student_name = models.CharField(max_length=100, null=True)
    student_lastname = models.CharField(max_length=100, null=True)
    student_sexe = models.CharField(max_length=10, null=True)
    student_class = models.CharField(max_length=10, null=True, blank=True)
    student_birthday_date = models.DateField(null=True)
    register_date = models.DateTimeField(null=True)
    student_register_number = models.IntegerField(null=True)
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


# class Student(models.Model) :
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    
#     address = models.CharField(max_length=100)
#     number = models.IntegerField()
#     classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
#     register_date = models.DateTimeField()
#     register_number = models.IntegerField()
#     school = models.ForeignKey(School, on_delete=models.CASCADE)
#     picture = models.ImageField(upload_to='images/students', null=True, blank=True)

#     def __str__(self) :
#         return self.lastname


    # def save(self, *args, **kwargs) :
    #     if self.password and not self.password.startswith('pbkdf2_sha256') :
    #         self.password = make_password(self.password)
    #     super().save(*args, **kwargs)

    # def __str__(self) -> str:
    #     return self.name
    

# class SchoolYear(models.Model) :
#     school_year = models.DateField()
#     school = models.ForeignKey(School, related_name='school', on_delete=models.CASCADE)
    
#     def __str__(self) -> str:
#         return self.school


# class Classe(models.Model) :
#     class_degree = models.CharField(max_length=50)
#     school_year = models.ForeignKey(SchoolYear, related_name='school_year', on_delete=models.CASCADE)
#     school = models.ForeignKey(School, related_name='school', on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return self.class_degree