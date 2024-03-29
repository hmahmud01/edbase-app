from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from edbase.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from xlrd import open_workbook
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from applicant.models import Student, Qualification, StudentFile, PersonalInfo, PaymentInfo, Teacher, Subject, SubjectMaterial, MaterialContent, QualificationSubject, Batch, Session, StudentSessionBatchTracker
from applicant.models import EdbaseBoard, EdbaseLocation, EdbaseQualification, EdbaseSubject, EdbaseTeacher, EdbaseTeacherSubject, EdbaseStudentQualification, EdbaseStudentSubjects, EdbaseStudentGuardian, EdbaseStudentLocationBoard
from applicant.models import EdbaseBatch, EdbaseSesssion, EdbaseBatchSubject, EdbaseStudentBatch, EdbaseSubjectContent, EdbaseGuardianAccount, EdbaseGuardianProfile, EdbaseRoutine

def home(request):
    data = ""
    return render(request, 'index.html', {'data': data})


def signUp(request):
    data = ""
    return render(request, 'signup.html', {'data': data})


def createStudentAccount(request):
    data = "failed"
    post_data = request.POST
    if post_data['pass'] == post_data['conf_pass']:
        user = User.objects.create_user(post_data['username'], post_data['email'], post_data['pass'])
        student = Student(
            user = user,
            name = post_data['name'],
            email = post_data['email'],
            user_type = "Student",
        )
        student.save()
        return redirect('accountcreatesuccess')
    else:
        return render(request, 'signup.html', {'data': data})  


def activateStudent(request, sid):
    student = Student.objects.get(id=sid)
    student.status = True
    student.save()

    subject = 'Account Create success in Edbase'
    message = 'Congrats! Your Account Has been Activated. You can now admit yourself for online system. Thanks for staying with us.'

    send_mail(subject, message, EMAIL_HOST_USER, [student.email], fail_silently=False)

    return redirect('dashboard')


def deactivateStudent(request, sid):
    student = Student.objects.get(id=sid)
    student.status = False
    student.save()

    subject = 'Account De-activation in Edbase'
    message = 'Your Account has been de activated in the system. Please contact office for further information. Thanks for staying with us.'

    send_mail(subject, message, EMAIL_HOST_USER, [student.email], fail_silently=False)

    return redirect('dashboard')


def studentAdmissionForm(request, sid):
    print(sid)
    student = Student.objects.get(id=sid)        
    aslevel = Subject.objects.filter(level__contains="AS")
    a2level = Subject.objects.filter(level__contains="A2")
    olevel = Subject.objects.filter(level__contains="O")
    return render(request, 'studentForm.html', {'data': student, 'aslevel': aslevel, 'a2level': a2level, 'olevel': olevel})


def loadsubject(request):
    get_data = request.GET
    location = get_data.get('locations')
    board = get_data.get('boards')
    qualifications = get_data.getlist('qualifications[]')
    

    subjects = EdbaseTeacherSubject.objects.all()
    subjects = subjects.filter(board_id=board)   
    subjects = subjects.filter(location_id=location)

    oLevel = None
    asLevel = None
    a2level = None

    # local host id
    # for qual in qualifications:
    #     if qual == '1':
    #         oLevel = subjects.filter(qualification_id=qual)
    #     elif qual == '2':
    #         asLevel = subjects.filter(qualification_id=qual)
    #     elif qual == '3':
    #         a2level = subjects.filter(qualification_id=qual)
    
    # Considering the id created again
    for qual in qualifications:
        if qual == '4':
            oLevel = subjects.filter(qualification_id=qual)
        elif qual == '5':
            asLevel = subjects.filter(qualification_id=qual)
        elif qual == '6':
            a2level = subjects.filter(qualification_id=qual)

    batchs = EdbaseBatchSubject.objects.all()

    return render(request, 'loadSubject.html', {'olevel': oLevel, 'aslevel': asLevel, 'a2level': a2level, "batchs": batchs})

def loadbatch(request):
    get_data = request.GET    
    sid = get_data.get('session')
    batchs = EdbaseBatchSubject.objects.filter(batch__session_id=sid)
    return render(request, 'loadbatch.html', {'batchs': batchs})

def demoTeacher(request):
    data = ""
    return render(request, 'teacherdemo.html', {'data': data})


def saveStudentData(request):
    print(request.POST)
    print(request.FILES)
    post_data = request.POST
    photo = request.FILES['photo']
    sid = post_data['id']
    student = Student.objects.get(id=sid)
    student.mobile = post_data['mobile']
    student.guardian_mobile = post_data['father_mobile']
    student.school = post_data['school']
    student.qualification = post_data['qualification']
    student.save()

    session = Session.objects.get(id=1)
    batch = Batch.objects.get(id=1)
    tracker = StudentSessionBatchTracker(
        students = student,
        session=session,
        batch=batch,
    )
    tracker.save()

    personal_info = PersonalInfo(
        student = student,
        acceptance = True,
        father = post_data['father'],
        mother = post_data['mother'],
        father_mobile = post_data['father_mobile'],
        mother_mobile = post_data['mother_mobile'],
        parent_email = post_data['parent_email'],
        street_1 = post_data['street_1'],
        street_2 = post_data['street_2'],
        city = post_data['city'],
        zip_code = post_data['zip_code'],
        country = post_data['country'],
        dob = post_data['dob'],
        blood_group = post_data['blood_group'],
        experience = post_data['experience'], 
        photo = photo
    )
    personal_info.save()

    session = Session.objects.get(id=1)
    batch = Batch.objects.get(id=1)

    tracker = StudentSessionBatchTracker(
        students = student,
        session = session,
        batch = batch
    )
    tracker.save()

    payment_option = post_data['payment_option']

    if 'Cash' in payment_option:
        payment_info = PaymentInfo(
            student = student,
            payment_option = payment_option,
            trx_id = "Cash Paid"
        )
        payment_info.save()
    else :
        payment_info = PaymentInfo(
            student = student,
            payment_option = payment_option,
            trx_id = post_data['trx_id']
        )
        payment_info.save()

    qual_value = post_data['qualification']

    if 'O' in qual_value:
        subjects = post_data.getlist('oLevel')
        for sub in subjects:
            subject = Subject.objects.get(id=sub)
            qualfication = QualificationSubject(
                student = student,
                subjects = subject,
            )
            qualfication.save()
    elif 'A' in qual_value:
        a2 = post_data.getlist('a2Level')
        aS = post_data.getlist('aSLevel')

        for sub in a2:
            subject = Subject.objects.get(id=sub)
            qualfication = QualificationSubject(
                student = student,
                subjects = subject,
            )
            qualfication.save()

        for sub in aS:
            subject = Subject.objects.get(id=sub)
            qualfication = QualificationSubject(
                student = student,
                subjects = subject,
                
            )
            qualfication.save()

    return redirect('success')

def studentForm(request):
    data = ""
    return render(request, 'studentForm.html', {'data': data})


def saveStudent(request):
    print("printing post data")
    print(request.POST)
    post_data = request.POST
    password = "edbase2020"
    user = User.objects.create_user(post_data['mobile'], post_data['email'], password)
    student = Student(
        user = user,
        name = post_data['name'],
        mobile = post_data['mobile'],
        guardian_mobile = post_data['guardian_mobile'],
        email = post_data['email'],
        school = post_data['school'],
        status= True,
        user_type = "Student",
        qualification = post_data['qualification']
    )
    student.save()
    session = Session.objects.get(id=1)
    batch = Batch.objects.get(id=1)
    tracker = StudentSessionBatchTracker(
        students = student,
        session=session,
        batch=batch,
    )
    tracker.save()
    qual_value = post_data['qualification']

    if 'O' in qual_value:
        subjects = post_data.getlist('oLevel')
        for sub in subjects:
            qualfication = Qualification(
                student = student,
                title = sub,
                level = "O level"
            )
            qualfication.save()
    elif 'A' in qual_value:
        a2 = post_data.getlist('a2Level')
        aS = post_data.getlist('aSLevel')

        for sub in a2:
            qualification = Qualification(
                student = student,
                title = sub,
                level = "A2"
            )
            qualification.save()

        for sub in aS:
            qualification = Qualification(
                student = student,
                title = sub,
                level = "AS"
            )
            qualification.save()

    subject = 'Admission success in Edbase'
    message = 'Congrats! You have been admitted into the edbase system. Please contact for further information'

    send_mail(subject, message, EMAIL_HOST_USER, [post_data['email']], fail_silently=False)
    
    return redirect('studentPanel')


def deleteStudent(request, sid):
    student = Student.objects.get(id=sid)
    user = User.objects.get(id=student.user_id)
    student.delete()
    user.delete()
    return redirect('dashboard')


def login(request):
    data = ""
    return render(request, 'login.html', {'data': data})


def verifyLogin(request):
    post_data = request.POST
    print(post_data)
    if 'user' and 'pass' in post_data:
        user = authenticate(
            request,
            username = post_data['user'],
            password = post_data['pass']
        )

        print(user)

        if user is None:
            if User.objects.filter(username=post_data['user']).exists():
                user = User.objects.get(username=post_data['user'])
                user_id = user.id
                student = Student.objects.get(user_id=user_id)
                print(student)
                status = student.status
                if student.status is True :
                    request.session['user'] = post_data['user']
                    request.session['type'] = "Student"
                    request.session['id'] = user_id
                    request.session['student'] = student.id
                    return redirect('studentpanel')
                else :
                    request.session['user'] = post_data['user']
                    request.session['type'] = "Student"
                    request.session['id'] = user_id
                    request.session['student'] = student.id
                    return redirect('studentpanelunverified')          
            else:                
                return redirect('login')
        elif user.is_superuser:
            auth_login(request, user)
            request.session['user'] = post_data['user']
            request.session['type'] = "Admin"
            request.session['id'] = user.id
            return redirect('dashboard')
        else:
            auth_login(request, user)
            print(user.id)
            user_id = user.id
            if Teacher.objects.filter(user_id=user_id).exists():
                teacher = Teacher.objects.get(user_id=user_id)
                request.session['user'] = teacher.user.username
                request.session['type'] = "Teacher"
                request.session['teacher_id'] = teacher.id
                request.session['id'] = user_id
                return redirect('teacherpanel')
            else:
                student = Student.objects.get(user_id=user_id)
                print(student)
                status = student.status
                if student.status is True :
                    request.session['user'] = post_data['user']
                    request.session['type'] = "Student"
                    request.session['id'] = user_id
                    request.session['student'] = student.id
                    return redirect('studentpanel')
                else :
                    request.session['user'] = post_data['user']
                    request.session['type'] = "Student"
                    request.session['id'] = user_id
                    request.session['student'] = student.id
                    return redirect('studentpanelunverified')            
    else:
        return redirect('login')


def verifyTeacher(tid):
    print(tid)
    return redirect('login')


def userLogout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def dashboard(request):
    all_students = Student.objects.all()
    if request.session.get('user'):        
        return render(request, 'dashboard.html', {'data': all_students, 'user': request.session.get('user')})
    else:
        user = "USER"
        return render(request, 'dashboard.html', {'data': all_students, 'user': user})


@login_required(login_url='/login/')
def studentDetail(request, sid):
    student = Student.objects.get(id=sid)    
    try:
        personal_info = PersonalInfo.objects.get(student_id=sid)
        payment_info = PaymentInfo.objects.get(student_id=sid)
        subjects = QualificationSubject.objects.filter(student__id__contains=sid)
        return render(request, 'studentDetail.html', {'data': student, 'subjects': subjects, 'payment': payment_info, 'personal': personal_info, 'media_url':settings.MEDIA_URL})
    except :
        subjects = QualificationSubject.objects.filter(student__id__contains=sid)
        return render(request, 'studentDetail.html', {'data': student, 'subjects': subjects})

@login_required(login_url='/login/')
def studentPanel(request):    
    sid = request.session['student']
    student = Student.objects.get(id=sid)
    try:
        personal_info = PersonalInfo.objects.get(student_id=sid)
        payment_info = PaymentInfo.objects.get(student_id=sid)
        subjects = QualificationSubject.objects.filter(student__id__contains=sid)
        return render(request, 'studentPanel.html', {'data': student, 'subjects': subjects, 'payment': payment_info, 'personal': personal_info, 'media_url':settings.MEDIA_URL})
    except :
        subjects = QualificationSubject.objects.filter(student__id__contains=sid)
        return render(request, 'studentPanel.html', {'data': student, 'subjects': subjects})

    
@login_required(login_url='/login/')
def teacherPanel(request):    
    tid = request.session['teacher_id']
    print(tid)
    teacher = Teacher.objects.get(id=tid)
    try:
        subjects = Subject.objects.filter(assigned_teacher_id=teacher.id)
        return render(request, 'teacherPanel.html', {'data': teacher, 'subjects': subjects})
    except :
        return render(request, 'teacherPanel.html', {'data': teacher})


@login_required(login_url='/login/')
def teacherDetail(request, tid):
    teacher = Teacher.objects.get(id=tid)
    try:
        subjects = Subject.objects.filter(assigned_teacher_id=teacher.id)
        return render(request, 'teacherDetail.html', {'data': teacher, 'subjects': subjects})
    except :
        return render(request, 'teacherDetail.html', {'data': teacher})


@login_required(login_url='/login/')
def changePasswordPage(request, uid):
    user = User.objects.get(id=uid)
    return render(request, 'changePassword.html', {'user': user})


def changePassword(request):
    post_data = request.POST
    uid = post_data['id']
    user = User.objects.get(id=uid)    
    if post_data['pass'] == post_data['conf_pass']:
        user.set_password(post_data['pass'])
        user.save()
        return redirect('studentpanel')
    else:
        return render(request, 'changePassword.html', {'user': user})
    


def studentPanelUnverified(request):
    data = ""
    return render(request, 'studentPanelUnverified.html', {'data': data})


def success(request):
    data = ""
    return render(request, 'success.html', {'data': data})


def successCreateAcccount(request):
    data = ""
    return render(request, 'successAccountCreate.html', {'data': data})


def uploadSpreadSheet(request):    
    files = StudentFile.objects.all()
    return render(request, 'uploadSpreadSheet.html', {'data': files})


def saveSpreadSheet(request):
    file = request.FILES['file']

    workBook = open_workbook(file_contents=file.read())

    workSheet = workBook.sheet_by_index(0)
    
    for row_id in range(1, workSheet.nrows):        
        if User.objects.filter(username=workSheet.cell_value(row_id, 1)).exists():
            print("Existis")            
        else:
            print("entering")
            user = User.objects.create_user(workSheet.cell_value(row_id, 1), workSheet.cell_value(row_id, 3), workSheet.cell_value(row_id, 2))
            student = Student(
                user = user,
                name = workSheet.cell_value(row_id,0),
                email = workSheet.cell_value(row_id,3),
                status= False,
                user_type = "Student",
            )
            student.save()

    print("process done")

    fileObj = StudentFile(file=file)
    fileObj.save()
    return redirect('upload')


def encapsulate(request, fid):
    print(fid)
    return redirect('upload')


def deleteFile(request, fid):
    file = StudentFile.objects.get(id=fid)
    file.delete()
    return redirect('upload')


def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers.html', {'data': teachers})


def addTeacher(request):
    data = ""
    return render(request, 'addTeacher.html', {'data': data})


def saveteacher(request):
    post_data = request.POST
    print(post_data)
    password = ""
    if 'pass' in post_data:
        passwd = post_data['pass']
        conf_pass = post_data['conf_pass']
        if passwd == conf_pass:
            password = passwd
            user = User.objects.create_user(post_data['username'], post_data['email'], password)
            teacher = Teacher(
                user = user,
                name = post_data['name'],
                status = True,
                level = post_data['qualification'],
            )
            teacher.save()
            return redirect('login')
    else:
        password = "edbaseteacher"
        user = User.objects.create_user(post_data['username'], post_data['email'], password)
        teacher = Teacher(
            user = user,
            name = post_data['name'],
            status = True,
            level = post_data['qualification'],
        )
        teacher.save()
        return redirect('teachers')


def signupTeacher(request):
    data = ""
    return render(request, 'teacherSignup.html', {'data': data})


def deleteteacher(request, tid):
    teacher = Teacher.objects.get(id=tid)
    user = User.objects.get(id=teacher.user_id)
    teacher.delete()
    user.delete()
    return redirect('teachers')


def subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects.html', {'data': subjects})


def addSubject(request):
    teachers = Teacher.objects.all()
    return render(request, 'addSubject.html', {'data': teachers})


def savesubject(request):
    post_data = request.POST
    if post_data['teacher']:
        teacher = Teacher.objects.get(id=post_data['teacher'])
        subject = Subject(
            title = post_data['name'],
            status = True,
            assigned = True,
            assigned_teacher = teacher,
            level = post_data['qualification'],
        )
        subject.save()
    else:
        subject = Subject(
            title = post_data['name'],
            status = True,
            assigned = False,
            level = post_data['qualification'],
        )
    return redirect('subjects')


def deletesubject(request, sid):
    student = Subject.objects.get(id=sid)    
    student.delete()
    return redirect('subjects')


def updateCode(request):
    post_data = request.POST
    subject = Subject.objects.get(id=post_data['subject_id'])
    subject.code = post_data['code']
    subject.save()
    return redirect('subjects')


def uploadMaterial(request):    
    print(request.session['id'])
    print(request.session['user'])
    uploader_id = request.session['id']
    user = User.objects.get(id=uploader_id)
    files = MaterialContent.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'materials.html', {'data': files, 'subjects': subjects, 'user': user})


def saveMaterial(request):
    post_data = request.POST
    files = request.FILES
    print(post_data)
    print(files)    
    print('done')
    subject_id = post_data['subject']
    subject = Subject.objects.get(id=subject_id)
    uploader_id = post_data['uploader']
    uploader = User.objects.get(id=uploader_id)
    material = SubjectMaterial(
        subject = subject,
        name = post_data['name'],
        level = post_data['qualification'],
        uploaded_by = uploader,
    )
    material.save()

    if 'file' in files:
        for f in files.getlist('file'):
            content = MaterialContent(
                material = material,
                file = f,
            )
            content.save()

    return redirect('uploadmaterial')


def deleteMaterial(request, fid):
    file = MaterialContent.objects.get(id=fid)
    file.delete()
    return redirect('uploadmaterial')


def contentDeashboard(request):    
    subjects = Subject.objects.all()
    return render(request, 'contentDashboard.html', {'data': subjects})


def contentDashboardDynamic(request):    
    user = request.session['type']
    user_id = "none"
    if user == "Student":
        print(request.session['student'])
        user_id = request.session['student']
        subjects = QualificationSubject.objects.filter(student__id__contains=user_id)
        return render(request, 'contentDashboardDynamic.html', {'data': subjects, 'user': user, 'user_id': user_id})
    elif user == "Teacher":
        user_id = request.session['teacher_id']
        subjects = Subject.objects.filter(assigned_teacher_id=user_id)
        return render(request, 'contentDashboardDynamic.html', {'data': subjects, 'user': user, 'user_id': user_id})
    subjects = Subject.objects.all()
    return render(request, 'contentDashboardDynamic.html', {'data': subjects, 'user': user, 'user_id': user_id})
    


def contentList(request, cid):
    data = ""
    print(cid)
    contents = MaterialContent.objects.filter(material__subject__id__contains=cid)    
    return render(request, 'contentList.html', {'data': contents})


def contentDetail(request, fid):
    data = MaterialContent.objects.get(id=fid)
    return render(request, 'contentDetail.html', {'data': data})


def help(request):
    data = ""
    return render(request, 'help.html', {'data': data})


def batchSession(request):
    students = StudentSessionBatchTracker.objects.all()
    session = Session.objects.all()
    batch = Batch.objects.all()

    return render(request, 'batchSessionDashboard.html', {'students': students, 'sessions': session, 'batchs': batch})


def batchSessionTeacher(request):
    user_id = request.session['teacher_id']
    students = QualificationSubject.objects.filter(subjects__assigned_teacher=user_id)    
    session = Session.objects.all()
    batch = Batch.objects.all()

    return render(request, 'batchSessionTeacher.html', {'students': students, 'sessions': session, 'batchs': batch})


def saveBatch(request):
    post_data = request.POST
    batch = Batch(
        batch = post_data['batch']
    )
    batch.save()
    if request.session['teacher_id']:
        return redirect('batchsessionteacher')
    else:
        return redirect('batchsession')


def deleteBatch(request, bid):
    batch = Batch.objects.get(id=bid)
    batch.delete()

    if request.session['teacher_id']:
        return redirect('batchsessionteacher')
    else:
        return redirect('batchsession')


def saveSession(request):
    post_data = request.POST
    session = Session(
        session = post_data['session']
    )
    session.save()

    if request.session['teacher_id']:
        return redirect('batchsessionteacher')
    else:
        return redirect('batchsession')


def deleteSession(request, sid):
    session = Session.objects.get(id=sid)
    session.delete()

    if request.session.teacher_id:
        return redirect('batchsessionteacher')
    else:
        return redirect('batchsession')


def generateStudentSessionBatchList(request):
    students = Student.objects.all()
    session = Session.objects.get(id=1)
    batch = Batch.objects.get(id=1)
    for student in students:
        tracker = StudentSessionBatchTracker(
            students = student,
            session=session,
            batch=batch,
        )
        tracker.save()

    return redirect('batchsession')

def deleteStudentSessionBatchList(request):
    tracker = StudentSessionBatchTracker.objects.all().delete()
    if request.session.teacher_id:
        return redirect('batchsessionteacher')
    else:
        return redirect('batchsession')


def assignStudentSessionBatch(request):
    print(request.POST)
    post_data = request.POST
    student_id = post_data['student_id']
    batch_id = post_data['student_batch']
    session_id = post_data['student_session']
    tracker = StudentSessionBatchTracker.objects.get(students__id=student_id)
    batch = Batch.objects.get(id=batch_id)
    session = Session.objects.get(id=session_id)
    tracker.batch = batch
    tracker.session = session
    tracker.save()    

    if request.session['teacher_id']:
        return redirect('batchsessionteacher')
    else:
        return redirect('batchsession')

# New Views Starting from here
# TODO: creating new views for new models
def addTeacherNext(request):
    locations = EdbaseLocation.objects.all()
    boards = EdbaseBoard.objects.all()
    qualifications = EdbaseQualification.objects.all()
    subjects = EdbaseSubject.objects.all()
    return render(request, 'addTeacher_next.html', {'locations': locations, 'boards': boards, 'qualifications': qualifications, 'subjects': subjects})

def addlocation(request):
    post_data = request.POST
    location = EdbaseLocation(
        name = post_data['location'],
    )
    location.save()
    return redirect('addteachernext')

def addboard(request):
    post_data = request.POST
    location = EdbaseBoard(
        name = post_data['board'],
    )
    location.save()
    return redirect('addteachernext')

def addqualifcation(request):
    post_data = request.POST
    location = EdbaseQualification(
        level = post_data['qualification'],
    )
    location.save()
    return redirect('addteachernext')

def addsubjecttosystem(request):
    post_data = request.POST
    boardId = post_data['board']
    board = EdbaseBoard.objects.get(id=boardId)
    location = EdbaseSubject(
        title = post_data['subject'],
        code = post_data['subject_code'],
        status = True,
        board = board,
    )
    location.save()
    return redirect('addteachernext')

def saveTeacherNext(request):
    post_data = request.POST
    print(post_data)
    teacherpass = "edbaseteacher"
    username = post_data['username']
    email = post_data['email']
    user = User.objects.create_user(username, email, teacherpass)
    teacher = EdbaseTeacher(
        user = user,
        name = post_data['name'],
        status = True,
    )
    teacher.save()

    location = EdbaseLocation.objects.get(id=post_data['location'])
    board = EdbaseBoard.objects.get(id=post_data['board'])
    qualification = EdbaseQualification.objects.get(id=post_data['qualification'])
    subject = EdbaseSubject.objects.get(id=post_data['subject'])

    teacherSubject = EdbaseTeacherSubject(
        teacher = teacher,
        location = location,
        board = board,
        qualification = qualification,
        subject = subject,
    )

    teacherSubject.save()

    return redirect('teacherlist')

def teacherlist(request):
    teachers = EdbaseTeacherSubject.objects.all()
    return render(request, 'teachersNew.html', {'teachers': teachers})

def teachernextdetail(request, tid):
    detail = EdbaseTeacherSubject.objects.get(id=tid)
    subjects = EdbaseTeacherSubject.objects.filter(id=tid)
    return render(request, 'teacherDetail.html', {'detail': detail, 'subjects': subjects})

def studentSignupAdmission(request):
    data = ''
    academy = EdbaseTeacherSubject.objects.all()
    qualifications = EdbaseQualification.objects.all()
    boards = EdbaseBoard.objects.all()
    locations = EdbaseLocation.objects.all()
    aslevel = Subject.objects.filter(level__contains="AS")
    a2level = Subject.objects.filter(level__contains="A2")
    olevel = Subject.objects.filter(level__contains="O")
    sessions = EdbaseSesssion.objects.all()
    return render(request, 'signuprework.html', 
        {'data': data, 'aslevel': aslevel, 'a2level': a2level, 'olevel': olevel, 'academy': academy, 'qualifications': qualifications, 'boards': boards, 'locations': locations, 'sessions': sessions})

def saveStudentSystem(request):
    print(request.POST)
    print(request.FILES)

    post_data = request.POST
    photo = request.FILES['photo']

    if post_data['pass'] == post_data['conf_pass']:
        user = User.objects.create_user(post_data['email'], post_data['email'], post_data['pass'])
        student = Student(
            user = user,
            name = post_data['name'],
            mobile = post_data['mobile'],
            email = post_data['email'],            
            school = post_data['school'],
            status = True,
            user_type = "student",            
        )
        student.save()
        personal_info = PersonalInfo(
            student = student,
            acceptance =True,
            passport = post_data['passnid'],
            parent_email = post_data['parent_email'],
            street_1 = post_data['street_1'],
            street_2 = post_data['street_2'],
            city = post_data['city'],
            zip_code = post_data['zip_code'],
            country = post_data['country'],
            dob = post_data['dob'],
            blood_group = post_data['blood_group'],            
            photo = photo
        )

        personal_info.save()

        location = EdbaseLocation.objects.get(id=post_data['location'])
        board = EdbaseBoard.objects.get(id=post_data['board'])

        location_board = EdbaseStudentLocationBoard(
            student = student,
            location = location,
            board = board
        )

        location_board.save()

        guardian = EdbaseStudentGuardian(
            student = student,
            guardian1 = post_data['guardian1'],
            guardian1relation = post_data['guardian1relation'],
            guardian2 = post_data['guardian2'],
            guardian2relation = post_data['guardian2relation'],
            parent_email = post_data['parent_email'],
            parent_phone = post_data['parent_phone']
        )

        guardian.save()

        qualifications = post_data.getlist('qualification')

        for qual in qualifications:
            edbqual = EdbaseQualification.objects.get(id=qual)
            studentqual = EdbaseStudentQualification(
                student = student,
                qualification = edbqual
            )
            studentqual.save()
        studentsubjects = []
        if 'olevel' in post_data:
            selected = post_data.getlist('olevel')
            for select in selected:
                edbsubject = EdbaseTeacherSubject.objects.get(id=select)
                subject = EdbaseStudentSubjects(
                    student = student,
                    subect = edbsubject
                )
                subject.save()
                studentsubjects.append(subject)
            
        if 'aslevel' in post_data:
            selected = post_data.getlist('aslevel')
            for select in selected:
                edbsubject = EdbaseTeacherSubject.objects.get(id=select)
                subject = EdbaseStudentSubjects(
                    student = student,
                    subect = edbsubject
                )
                subject.save()
                studentsubjects.append(subject)

        if 'a2level' in post_data:
            selected = post_data.getlist('a2level')
            for select in selected:
                edbsubject = EdbaseTeacherSubject.objects.get(id=select)
                subject = EdbaseStudentSubjects(
                    student = student,
                    subect = edbsubject
                )
                subject.save()
                studentsubjects.append(subject)

        batchs = post_data.getlist('batch')
        print(batchs)
        for batch in batchs:
            edbbatch = EdbaseBatchSubject.objects.get(id=batch)
            studentbatch = EdbaseStudentBatch(                    
                batch = edbbatch.batch,
                student =student,
                subject =edbbatch.subject
            )
            studentbatch.save()
        payment_option = post_data['payment_option']

        if 'Cash' in payment_option:
            payment_info = PaymentInfo(
                student = student,
                payment_option = payment_option,
                trx_id = "Cash Paid"
            )
            payment_info.save()
        else :
            payment_info = PaymentInfo(
                student = student,
                payment_option = payment_option,
                trx_id = post_data['trx_id']
            )
            payment_info.save()

        guardian_email = post_data['parent_email']

        if User.objects.filter(username=guardian_email).exists():
            guardianUser = User.objects.get(username=guardian_email)
            account = EdbaseGuardianAccount.objects.get(user_id=guardianUser.id)
            profile = EdbaseGuardianProfile(
                useracc = account,
                student = student,
                info = guardian,
                studentinfo = personal_info
            )
            profile.save()
        else:
            guardian_pass = "edbaseguardian"
            guardianUser = User.objects.create_user(guardian_email, password= guardian_pass, email=guardian_email)
            account = EdbaseGuardianAccount(
                user = guardianUser
            )
            account.save()
            profile = EdbaseGuardianProfile(
                useracc = account,
                student = student,
                info = guardian,
                studentinfo = personal_info
            )
            profile.save()

    return redirect('login')

def edbaseStudentList(request):
    students = Student.objects.all()
    return render(request, 'studentlist.html', {'students': students})

def edbaseStudentDetail(request, sid):
    detail = Student.objects.get(id=sid)
    personal_info = PersonalInfo.objects.get(student_id=sid)
    subjects = EdbaseStudentSubjects.objects.filter(student_id=sid)
    loc_board = EdbaseStudentLocationBoard.objects.get(student_id=sid)
    guardian = EdbaseStudentGuardian.objects.get(student_id=sid)
    qualification = EdbaseStudentQualification.objects.filter(student_id=sid)
    payment_info = PaymentInfo.objects.get(student_id=sid)
    batchs = EdbaseStudentBatch.objects.filter(student_id=sid)
    context = {'detail': detail, 'personal_info': personal_info, 'subjects': subjects, 'loc_board': loc_board, 'guardian': guardian, 'qualification': qualification, 'payment_info': payment_info, 'batchs': batchs}
    return render(request, 'studentdetailrework.html', context)


def edbaseStudentPortal(request):
    data = ""
    student = request.user.student
    subjects = EdbaseStudentSubjects.objects.filter(student_id=student.id)    
    batchs = EdbaseStudentBatch.objects.filter(student_id=student.id)
    return render(request, "portal/student/student.html", {"data": data, "subjects": subjects, "batchs": batchs})

def edbaseStudentContent(request, bid):
    info = EdbaseStudentBatch.objects.get(id=bid)
    contents = EdbaseSubjectContent.objects.filter(batch_id=info.batch.id)
    return render(request, "portal/student/contents.html", {"info": info, "contents": contents})

def edbaseTeacherPortal(request):
    data = ""
    locations = EdbaseLocation.objects.all()
    boards = EdbaseBoard.objects.all()
    qualifications = EdbaseQualification.objects.all()
    teacher = request.user.edbaseteacher    
    subjects = EdbaseTeacherSubject.objects.filter(teacher_id=teacher.id)    
    batchsubjects = EdbaseBatchSubject.objects.filter(subject__teacher_id=teacher.id)
    sessions = EdbaseSesssion.objects.all()    
    batchs = EdbaseBatch.objects.all()
    return render(request, "portal/teacher/teacher.html", {"data": data, 'subjects':subjects, 'locations': locations, 'boards': boards, 'qualifications': qualifications, 'sessions': sessions, 'batchs': batchs, 'batchsubjects': batchsubjects})

def teacherPortalDetail(request, tid):    
    detail = EdbaseTeacherSubject.objects.filter(teacher_id=tid).first()
    subjects = EdbaseTeacherSubject.objects.filter(teacher_id=tid)
    return render(request, 'teacherDetail.html', {'detail': detail, 'subjects': subjects})    

def sessionList(request, sid):
    sessions = EdbaseSesssion.objects.all()
    return render(request, "portal/teacher/sessionlist.html", {"sessions": sessions, "sid": sid})

def teacherBatchList(request, ssid, sid):
    print(sid)
    print(ssid)
    # batchs = EdbaseBatchSubject.objects.filter(subject_id=sid)
    session = EdbaseSesssion.objects.get(id=ssid)
    batchs = EdbaseBatchSubject.objects.filter(batch__session_id=ssid).filter(subject_id=sid)
    subject = EdbaseTeacherSubject.objects.get(id=sid)
    batchlist = EdbaseBatch.objects.all()
    sessionlist = EdbaseSesssion.objects.all()
    return render(request, "portal/teacher/batchlist.html", {"batchs" : batchs, "subject": subject, "batchlist": batchlist, "sessionlist": sessionlist, "sid": sid, "ssid": ssid, "session": session})    

def batchContent(request, bid, sid):
    batch = EdbaseBatch.objects.get(id=bid)
    return render(request, "portal/teacher/batchcontent.html", {"bid": bid, "sid": sid, "batch": batch})

def studentBatchList(request, bid):
    students = EdbaseStudentBatch.objects.filter(batch_id=bid)
    return render(request, "portal/teacher/batchstudentlist.html", {"students": students})

# THIS IS SUBJECT MATERIAL CONTENT VIEW
def content(request, bid, sid):    
    batch = EdbaseBatch.objects.get(id=bid)
    subject = EdbaseTeacherSubject.objects.get(id=sid)
    contents = EdbaseSubjectContent.objects.filter(subject_id=sid).filter(batch_id=bid)
    return render(request, "portal/teacher/subjectContent.html", {"batch" : batch, "subject": subject, "bid": bid, "sid": sid, "contents": contents})

def addContent(request):
    post_data = request.POST
    files = request.FILES
    sid = post_data['subject_id']
    bid = post_data['batch_id']
    subject = EdbaseTeacherSubject.objects.get(id=sid)
    batch = EdbaseBatch.objects.get(id=bid)
    user = request.user
    if 'file' in files:
        for f in files.getlist('file'):
            content = EdbaseSubjectContent(
                file = f,
                name = post_data['name'],
                uploader = user,
                subject = subject,
                batch = batch
            )
            content.save()
    
    return redirect('content', bid, sid)


def deleteContent(request, cid, sid, bid):
    content = EdbaseSubjectContent.objects.get(id=cid)
    content.delete()
    return redirect('content', bid, sid)

def subjectContentDetail(request, cid):    
    data = EdbaseSubjectContent.objects.get(id=cid)
    return render(request, 'portal/teacher/contentDetail.html', {'data': data})    

def assignBatchToSubject(request):
    post_data = request.POST
    sid = post_data['subject_id']
    ssid = post_data['session_id']
    subject = EdbaseTeacherSubject.objects.get(id=sid)
    batch = EdbaseBatch.objects.get(id=post_data['batch'])
    edbsubjectbatch = EdbaseBatchSubject(
        subject = subject,
        batch= batch
    )
    edbsubjectbatch.save()
    return redirect('teacherbatchlist',ssid, sid)

def teacherStudentList(request, sid):
    students = EdbaseStudentSubjects.objects.filter(subect_id=sid)
    main = EdbaseStudentSubjects.objects.filter(subect_id=sid).first()
    subject = main.subect.subject
    return render(request, "portal/teacher/studentlist.html", {"students": students, "subject": subject})

def teacherbatchandsession(request):
    data = ""
    teacher = request.user.edbaseteacher    
    subjects = EdbaseTeacherSubject.objects.filter(teacher_id=teacher.id)   
    return render(request, "portal/teacher/batchandsession.html", {"data": data, "subjects": subjects})

def addAnotherSubject(request):
    post_data = request.POST
    print(post_data)
    teacher = request.user.edbaseteacher
    location = EdbaseLocation.objects.get(id=post_data['location'])
    board = EdbaseBoard.objects.get(id=post_data['board'])
    qualification = EdbaseQualification.objects.get(id=post_data['qualification'])    

    subject = EdbaseSubject(
        title = post_data['subject'],
        code = post_data['subject_code'],
        status = True,
        board = board,
    )
    subject.save()

    teacherSubject = EdbaseTeacherSubject(
        teacher = teacher,
        location = location,
        board = board,
        qualification = qualification,
        subject = subject,
    )
    teacherSubject.save()

    batch = EdbaseBatch.objects.get(id=post_data['batch'])
    batchSubject = EdbaseBatchSubject(
        subject = teacherSubject,
        batch = batch
    )

    batchSubject.save()

    return redirect('teacherportal')

def removesubject(request, sid):
    subject = EdbaseTeacherSubject.objects.get(id=sid)
    batch = EdbaseBatchSubject.objects.filter(subject_id=subject.id)
    subjecttitle = EdbaseSubject.objects.get(id=subject.subject.id)
    print(subject.id)
    for b in batch:
        print(b.id)
    print(subjecttitle.id)
    subject.delete()
    for b in batch:
        b.delete()
    subjecttitle.delete()
    print("subject deleted")
    return redirect('teacherportal')

def veriyuser(request):
    post_data = request.POST
    print(post_data)
    if 'user' and 'pass' in post_data:
        user = authenticate(
            request,
            username = post_data['user'],
            password = post_data['pass']
        )
        print(user)
        if user is not None:
            if user.is_authenticated:            
                user_id = user.id
                if user.is_superuser:
                    auth_login(request, user)
                    return redirect('dashboard')
                else:
                    if Student.objects.filter(user_id=user_id):
                        auth_login(request, user)
                        return redirect('studentportal')
                    elif EdbaseGuardianAccount.objects.filter(user_id=user_id):
                        auth_login(request, user)
                        return redirect('guardianportal')
                    else:
                        auth_login(request, user)
                        teacher = user.edbaseteacher                        
                        return redirect('teacherportal')
            else:
                return redirect('login')
        else:
            return redirect('login')

def studentPasswordReset(request, uid):
    post_data = request.POST
    user = User.objects.get(id=uid)
    password = post_data['pass']
    user.set_password(password)
    user.save()
    return redirect('studentlist')        

def addSession(request):
    post_data = request.POST
    session = post_data['session']
    edbsession = EdbaseSesssion(
        session = session
    )
    edbsession.save()    
    print(edbsession.id)
    return redirect('teacherportal')

def addBatch(request):
    post_data = request.POST
    session = EdbaseSesssion.objects.get(id=post_data['session'])    
    batch = EdbaseBatch(
        session = session,
        batch = post_data['batch'],
        seat = post_data['seat']
    )   
    batch.save()    
    return redirect('teacherportal')
    
def edbaseremovestudent(request, sid):
    student = Student.objects.get(id=sid)
    user = User.objects.get(id=student.user_id)
    personalInfo = PersonalInfo.objects.get(student_id=sid)    
    student.delete()
    user.delete()
    personalInfo.delete()
    if PaymentInfo.objects.get(student_id=sid).exists():
        paymentinfo = PaymentInfo.objects.get(student_id=sid)
        paymentinfo.delete()
    return redirect('studentlist')

def edbaseGuardianPortal(request):
    user_id = request.user.id
    account = EdbaseGuardianAccount.objects.get(user_id=user_id)
    data = EdbaseGuardianProfile.objects.filter(useracc__user_id=user_id)
    return render(request, "portal/guardian/index.html", {"data": data})

def routineIndex(request):
    qualifications = EdbaseQualification.objects.all()
    # localhost id's
    # o_level = 1
    # as_level = 2
    # a2_level = 3
    
    # server id's
    o_level = 4
    as_level = 5
    a2_level = 6
    return render(request, "portal/admin/routineIndex.html", {"qualifications": qualifications, "o_level": o_level, "as_level": as_level, "a2_level": a2_level})

def routines(request, rid):
    routines = EdbaseRoutine.objects.filter(qualification_id=rid)
    return render(request, "portal/admin/routines.html", {"routines": routines})


def addRoutine(request):
    post_data = request.POST
    files = request.FILES
    name = post_data['name']
    session = post_data['session']
    qualification = post_data['qualification']
    qualObj = EdbaseQualification.objects.get(id=qualification)
    if 'file' in files:
        for f in files.getlist('file'):
            routine = EdbaseRoutine(
                file = f,
                name = name,
                session = session,
                qualification = qualObj
            )
            routine.save()
    
    return redirect('routine')

def removeRoutine(request, rid):

    routine = EdbaseRoutine.objects.get(id=rid)
    print(routine.file.path)
    os.remove(routine.file.path)
    routine.delete()
    return redirect('routine')

def studentRoutine(request):
    routines = EdbaseRoutine.objects.all()
    # localhost id'
    # o_level = 1
    # as_level = 2
    # a2_level = 3

    # server id's
    o_level = 4
    as_level = 5
    a2_level = 6
    return render(request, "portal/student/routineIndex.html", {"routines": routines, "o_level": o_level, "as_level": as_level, "a2_level": a2_level})

def studentRoutineIndex(request, rid):
    routines = EdbaseRoutine.objects.filter(qualification_id=rid)
    return render(request, "portal/student/routine.html", {"routines": routines})