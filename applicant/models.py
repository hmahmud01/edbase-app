from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    guardian_mobile = models.CharField(max_length=11, null=True, blank=True)
    email = models.EmailField(max_length=128, null=True, blank=True)
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

class PaymentInfo(models.Model):
    student = models.ForeignKey(Student, related_name='student_payment_info', on_delete=models.CASCADE)
    payment_option = models.CharField(max_length=128, null=True, blank=True)
    trx_id = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.student    

class PersonalInfo(models.Model):
    student = models.ForeignKey(Student, related_name='student_personal_info', on_delete=models.CASCADE)
    acceptance = models.BooleanField(default=False, null=True, blank=True)
    father = models.CharField(max_length=128, null=True, blank=True)
    mother = models.CharField(max_length=128, null=True, blank=True)
    father_mobile = models.CharField(max_length=128, null=True, blank=True)
    mother_mobile = models.CharField(max_length=128, null=True, blank=True)
    street_1 = models.CharField(max_length=128, null=True, blank=True)
    street_2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    zip_code = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    dob = models.CharField(max_length=128, null=True, blank=True)
    blood_group = models.CharField(max_length=128, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    photo = models.FileField('app_files', upload_to='photos', blank=True, null=True)

    def __str__(self):
        return self.student

class StudentFile(models.Model):
    file = models.FileField('app_files', upload_to='files', blank=True, null=True)

    def __str__(self):
        return self.file