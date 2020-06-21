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


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    level = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    assigned = models.BooleanField(default=False, null=True, blank=True)
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    level = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title


class QualificationSubject(models.Model):
    student = models.ForeignKey(Student, related_name='student_subjects_qualified', on_delete=models.CASCADE)
    subjects = models.ForeignKey(Subject, related_name='subjects', on_delete=models.CASCADE)

    def __str__(self):
        return self.student


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
    parent_email = models.EmailField(max_length=128, null=True, blank=True)
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


class SubjectMaterial(models.Model):
    subject = models.ForeignKey(Subject, related_name='subject_files', on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True, blank=True)
    level = models.CharField(max_length=128, null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class MaterialContent(models.Model):
    material = models.ForeignKey(SubjectMaterial, related_name='subject_materials', on_delete=models.CASCADE)
    file = models.FileField('subject_contents', upload_to='subject', blank=True, null=True)

    def __str__(self):
        return self.file


class Session(models.Model):
    session = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.session


class Batch(models.Model):
    batch = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.session


class StudentSessionBatchTracker(models.Model):
    students = models.ForeignKey(Student, related_name='students', on_delete=models.CASCADE)    
    session = models.ForeignKey(Session, related_name='sessions', on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, related_name='batchs', on_delete=models.CASCADE)

    def __str__(self):
        return self.student