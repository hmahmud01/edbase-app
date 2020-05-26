from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=False, blank=False)
    mobile = models.CharField(max_length=11, null=False, blank=False)
    guardian_mobile = models.CharField(max_length=11, null=False, blank=False)
    email = models.EmailField(max_length=128, unique=True, null=False, blank=False)
    school = models.CharField(max_length=128, null=False, blank=False)
    status = models.BooleanField(default=False, null=False, blank=False)
    user_type = models.CharField(max_length=128, null=False, blank=False)
    qualification = models.CharField(max_length=128, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.name

class Qualification(models.Model):
    student = models.ForeignKey(Student, related_name='student_qualification', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    level = models.CharField(max_length=128)

    def __str__(self):
        return self.student
