from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from applicant import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('verifylogin/', views.verifyLogin, name='verifylogin'),
    path('logout/', views.userLogout, name='logout'),
    path('studentdetail/<int:sid>/', views.studentDetail, name='studentdetail'),
    path('studentform/', views.studentForm, name='studentform'),
    path('success/', views.success, name='success'),
    path('savestudent/', views.saveStudent, name='savestudent'),
    path('studentpanel/', views.studentPanel, name='studentpanel'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)