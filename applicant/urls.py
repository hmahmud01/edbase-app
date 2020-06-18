from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from applicant import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signUp, name='signup'),
    path('activate/<int:sid>/', views.activateStudent, name='activate'),
    path('deactivate/<int:sid>/', views.deactivateStudent, name='deactivate'),
    path('createaccount/', views.createStudentAccount, name='createaccount'),
    path('login/', views.login, name='login'),
    path('verifylogin/', views.verifyLogin, name='verifylogin'),
    path('logout/', views.userLogout, name='logout'),
    path('studentdetail/<int:sid>/', views.studentDetail, name='studentdetail'),    
    path('studentform/', views.studentForm, name='studentform'),
    path('studentAdmissionForm/<int:sid>/', views.studentAdmissionForm, name='studentAdmissionForm'),
    path('savestudentdata/', views.saveStudentData, name='savestudentdata'),
    path('success/', views.success, name='success'),
    path('accountcreatesuccess/', views.successCreateAcccount, name="accountcreatesuccess"),
    path('savestudent/', views.saveStudent, name='savestudent'),    
    path('studentpanel/', views.studentPanel, name='studentpanel'),
    path('studentpanelunverified/', views.studentPanelUnverified, name='studentpanelunverified'),
    path('deletestudent/<int:sid>/', views.deleteStudent, name='deletestudent'),
    path('upload/', views.uploadSpreadSheet, name='upload'),
    path('savexl/', views.saveSpreadSheet, name='savexl'),
    path('encapsulate/<int:fid>', views.encapsulate, name='encapsulate'),
    path('deletefile/<int:fid>', views.deleteFile, name='deletefile'),
    path('changepassword/<int:uid>/', views.changePasswordPage, name='changePasswordPage'),
    path('passwordchange/', views.changePassword, name='changePassword'),
    path('teachers/', views.teachers, name='teachers'),
    path('subjects/', views.subjects, name='subjects'),
    path('addteacher/', views.addTeacher, name='addteacher'),
    path('saveteacher/', views.saveteacher, name='saveteacher'),
    path('deleteteacher/<int:tid>', views.deleteteacher, name='deleteteacher'),
    path('addsubject/', views.addSubject, name='addsubject'),
    path('savesubject/', views.savesubject, name='savesubject'),
    path('deletesubject/<int:sid>', views.deletesubject, name='deletesubject'),
    path('uploadmaterial/', views.uploadMaterial, name='uploadmaterial'),
    path('savematerial/', views.saveMaterial, name='savematerial'),
    path('deletematerial/', views.deleteMaterial, name='deletematerial'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)