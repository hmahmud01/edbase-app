from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from applicant import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('studentdetail/', views.studentDetail, name='studentDetail'),
    path('studentform/', views.studentForm, name='studentForm'),
    path('studentpanel/', views.studentPanel, name='studentPanel'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)