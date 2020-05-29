from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from edbase.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from applicant.models import Student, Qualification

def home(request):
    data = ""
    return render(request, 'index.html', {'data': data})


def signUp(request):
    data = ""
    return render(request, 'signup.html', {'data': data})


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
    
    return redirect('success')


def deleteStudent(request, sid):
    instance = Student.objects.get(id=sid)
    instance.delete()
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
            request.session['user'] = post_data['user']
            request.session['type'] = "Student"
            return redirect('studentpanel')
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


def studentPanel(request):
    data = ""
    return render(request, 'studentPanel.html', {'data': data})


def success(request):
    data = ""
    return render(request, 'success.html', {'data': data})