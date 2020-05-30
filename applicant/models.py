from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    guardian_mobile = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(max_length=128, unique=True, null=True, blank=True)
    school = models.CharField(max_length=128, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    user_type = models.CharField(max_length=128, null=True, blank=True)
    qualification = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Qualification(models.Model):
    student = models.ForeignKey(Student, related_name='student_qualification', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    level = models.CharField(max_length=128)

    def __str__(self):
        return self.student
