from django.shortcuts import render

# Create your views here.

def home(request):
    data = ""
    return render(request, 'index.html', {'data': data})


def dashboard(request):
    data = ""
    return render(request, 'dashboard.html', {'data': data})


def login(request):
    data = ""
    return render(request, 'login.html', {'data': data})


def studentDetail(request):
    data = ""
    return render(request, 'studentDetail.html', {'data': data})


def studentForm(request):
    data = ""
    return render(request, 'studentForm.html', {'data': data})


def studentPanel(request):
    data = ""
    return render(request, 'studentPanel.html', {'data': data})