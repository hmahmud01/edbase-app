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
    code = models.CharField(max_length=128, null=True, blank=True)
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
    unique_id = models.CharField(max_length=26, null=True, blank=True)
    acceptance = models.BooleanField(default=False, null=True, blank=True)
    passport = models.CharField(max_length=128, null=True, blank=True)
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
        return self.batch


class StudentSessionBatchTracker(models.Model):
    students = models.ForeignKey(Student, related_name='students', on_delete=models.CASCADE)    
    session = models.ForeignKey(Session, related_name='sessions', on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, related_name='batchs', on_delete=models.CASCADE)

    def __str__(self):
        return self.student


# STARTING FROM NEW
# TODO : CREATE NECESSARY CLASS MODELS
class EdbaseTeacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    createt_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name
    
class EdbaseBoard(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.name

class EdbaseSubject(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    level = models.CharField(max_length=128, null=True, blank=True)
    code = models.CharField(max_length=128, null=True, blank=True)
    board = models.ForeignKey(EdbaseBoard, related_name='edbaseboardforsubject', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title

class EdbaseLocation(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.name

class EdbaseQualification(models.Model):
    level = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.level

class EdbaseTeacherSubject(models.Model):
    teacher = models.ForeignKey(EdbaseTeacher, related_name='edbaseteacher', on_delete=models.CASCADE)
    location = models.ForeignKey(EdbaseLocation, related_name='edbaselocation', on_delete=models.CASCADE)
    board = models.ForeignKey(EdbaseBoard, related_name='edbaseboard', on_delete=models.CASCADE)
    qualification = models.ForeignKey(EdbaseQualification, related_name='edbasequalification', on_delete=models.CASCADE)
    subject = models.ForeignKey(EdbaseSubject, related_name='edbasesubject', on_delete=models.CASCADE)

    def __str__(self):
        return self.teacher.name


class EdbaseStudentQualification(models.Model):
    student = models.ForeignKey(Student, related_name='edbase_student_qualification_connection', on_delete=models.CASCADE)
    qualification = models.ForeignKey(EdbaseQualification, related_name='qualification', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class EdbaseStudentSubjects(models.Model):
    student = models.ForeignKey(Student, related_name='edbase_student', on_delete=models.CASCADE)
    subect = models.ForeignKey(EdbaseTeacherSubject, related_name='edbase_student_teacher_subject', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class EdbaseStudentGuardian(models.Model):
    student = models.ForeignKey(Student, related_name='edbase_student_guardian', on_delete=models.CASCADE)
    guardian1 = models.CharField(max_length=128, null=True, blank=True)
    guardian1relation = models.CharField(max_length=128, null=True, blank=True)
    guardian2 = models.CharField(max_length=128, null=True, blank=True)
    guardian2relation = models.CharField(max_length=128, null=True, blank=True)
    parent_email = models.EmailField(max_length=128, null=True, blank=True)
    parent_phone = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.id

class EdbaseStudentLocationBoard(models.Model):
    student = models.ForeignKey(Student, related_name='edbase_student_loc', on_delete=models.CASCADE)
    location = models.ForeignKey(EdbaseLocation, related_name='edbase_location', on_delete=models.CASCADE)
    board = models.ForeignKey(EdbaseBoard, related_name='edbase_board', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class EdbaseSesssion(models.Model):
    session = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class EdbaseBatch(models.Model):
    session = models.ForeignKey(EdbaseSesssion, related_name='edbase_session_batch', on_delete=models.CASCADE)
    batch = models.CharField(max_length=128, null=True, blank=True)
    seat = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class EdbaseBatchSubject(models.Model):
    subject = models.ForeignKey(EdbaseTeacherSubject, related_name='edbase_subect_batch', on_delete=models.CASCADE)
    batch = models.ForeignKey(EdbaseBatch, related_name='edbase_batch', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class EdbaseStudentBatch(models.Model):    
    batch = models.ForeignKey(EdbaseBatch, related_name='edbase_batch_student', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='edbase_student_batch', on_delete=models.CASCADE)      
    edsubject = models.ForeignKey(EdbaseStudentSubjects, related_name='edb_stu_sub', on_delete=models.CASCADE, null=True, blank=True)  
    subject = models.ForeignKey(EdbaseTeacherSubject, related_name='edb_subject', on_delete=models.CASCADE, null=True, blank=True)  
    create_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class EdbaseSubjectContent(models.Model):
    file = models.FileField('contents', upload_to='content', blank=True, null=True)
    name = models.CharField(max_length=36, null=True, blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(EdbaseTeacherSubject, related_name='content_subject', on_delete=models.CASCADE)
    batch = models.ForeignKey(EdbaseBatch, related_name='content_batch', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)    

    def __str__(self):
        return str(self.id)

class EdbaseGuardianAccount(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class EdbaseGuardianProfile(models.Model):    
    useracc = models.ForeignKey(EdbaseGuardianAccount, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, related_name='students_guardian', on_delete=models.CASCADE)
    info = models.ForeignKey(EdbaseStudentGuardian, related_name='students_guardian_info', on_delete=models.CASCADE)
    studentinfo = models.ForeignKey(PersonalInfo, related_name='students_personal_ifo', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class EdbaseRoutine(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    session = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField('routines',upload_to='routines', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name