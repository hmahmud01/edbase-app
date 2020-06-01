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

from applicant.models import Student, Qualification, StudentFile

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
    return render(request, 'studentForm.html', {'data': student})


def saveStudentData(request):
    print(request.POST)
    post_data = request.POST
    sid = post_data['id']
    student = Student.objects.get(id=sid)
    student.mobile = post_data['mobile']
    student.guardian_mobile = post_data['guardian_mobile']
    student.school = post_data['school']
    student.qualification = post_data['qualification']
    student.save()
    
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
    print("printing post data")
    print(request.POST)
    post_data = request.POST
    if 'user' and 'pass' in post_data:
        user = authenticate(
            request,
            username = post_data['user'],
            password = post_data['pass']
        )

        if user is None:
            return redirect('login')
        elif user.is_superuser:
            auth_login(request, user)
            request.session['user'] = post_data['user']
            request.session['type'] = "Admin"
            return redirect('dashboard')
        else:
            auth_login(request, user)
            print(user.id)
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
    subjects = Qualification.objects.filter(student__id__contains=sid)

    return render(request, 'studentDetail.html', {'data': student, 'subjects': subjects})


@login_required(login_url='/login/')
def studentPanel(request):    
    sid = request.session['student']
    student = Student.objects.get(id=sid)
    subjects = Qualification.objects.filter(student__id__contains=sid)

    return render(request, 'studentPanel.html', {'data': student, 'subjects': subjects})


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

    print("processing xl file")
    for row_id in range(1, workSheet.nrows):
        print(workSheet.cell_value(row_id, 1))
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

    # print(sheet.cell(1, 3))
    # print(book)

    fileObj = StudentFile(file=file)
    fileObj.save()



    
    # path = default_storage.save('tmp/{}'.format(file), ContentFile(file.read()))
    # tmp_file = os.path.join(settings.MEDIA_ROOT, path)

    # print(path)
    # print(tmp_file)

    # xlfile = default_storage.open(path)
    # file_url = default_storage.url(tmp_file)
    # default_storage.delete(path)
    # book = open_workbook(file_url)
    # sheet = book.sheet_by_index(1)

    # print(sheet.cell(1, 0))
    return redirect('upload')


def encapsulate(request, fid):
    print(fid)
    return redirect('upload')


def deleteFile(request, fid):
    file = StudentFile.objects.get(id=fid)
    file.delete()
    return redirect('upload')