from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class Admin(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Profession(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=255)
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE, null=True, related_name="technologies"
    )

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=40)
    salary = models.IntegerField()
    profession = models.ManyToManyField(Profession, related_name="profession_t")
    technologies = models.ManyToManyField(Technology, related_name="technologies_t")

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.IntegerField()
    profession = models.ManyToManyField(Profession, related_name="profession_s")
    teachers = models.ManyToManyField(Teacher, related_name="teacher_f")

    def __str__(self):
        return self.name


class WeekDays(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Groups(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.IntegerField()
    week_days = models.ManyToManyField(WeekDays, related_name="days")
    begin_date = models.CharField(max_length=50)
    when_start = models.CharField(max_length=50)
    complete_date = models.CharField(max_length=50)
    technologies = models.ManyToManyField(Technology, related_name="group_technology")
    students = models.ManyToManyField(Student, related_name="students")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Davomat(models.Model):
    sana = models.CharField(max_length=255)
    keldi = models.CharField(max_length=55)
    student = models.ForeignKey(
        Student, related_name="davomat", on_delete=models.CASCADE
    )
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.student.name


class Payment(models.Model):
    quantity = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    administrator = models.ForeignKey(Admin, on_delete=models.CASCADE)
    month = models.CharField(max_length=50, null=True)
    payment = models.CharField(max_length=40, null=True)
    when = models.CharField(max_length=40, null=True)

    def __str__(self):
        return f"{self.quantity} {self.student.name}"


DISCOUNT_CODE_TYPES_CHOICES = [
    ("percent", "Percentage-based"),
    ("value", "Value-based"),
]


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, username, role, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            username=username,
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, date_of_birth, password=None):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )

    class Role(models.TextChoices):
        Director = "DR", "DIRECTOR"
        Administrator = "AD", "ADMINISTRATOR"
        Teacher = "TR", "TEACHER"
        Student = "ST", "STUDENT"

    date_of_birth = models.DateField()
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=2, choices=Role.choices, default=Role.Student)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    linkedin_token = models.TextField(blank=True, default="")
    expiry_date = models.DateTimeField(null=True, blank=True)
    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def linkedin_signed_in(self):
        return bool(self.linkedin_token) and self.expiry_date > timezone.now()
