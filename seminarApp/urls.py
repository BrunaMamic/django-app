"""
URL configuration for seminarApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView

from seminar import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('list_subjects/', views.list_subjects,name='subjects'),
    path('add_subject/', views.add_subject,name="add_subject"),
    path('edit_subject/<int:id>', views.edit_subject, name='edit_subject'),
    path('list_subjects/<int:id>/list_of_students_per_subject/', views.list_students_per_subjects, name='enroled_students'),

    path('update_professor/', views.update_professor, name='update_professor'),
    path('list_all_students/', views.students, name="students_list"),
    path('add_students/', views.add_students, name="add_students"),
    path('edit_student/<int:id>/', views.edit_student, name='edit_student'),

    path('list_professors/', views.professors,name='professors_list'),
    path('add_professors/', views.add_professor,name="add_professors"),
    path('edit_professor/<int:id>', views.edit_professor, name='edit_professor'),

    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', views.custom_logout, name='logout'),
    
    path('enrollment_list/<int:id>/', views.enrollment_list, name='enrollment_list'),
    path('unenroll/<int:subject_id>/<int:student_id>/', views.unenroll_subject, name='unenroll_subject'),

    path('list_polozeni/', views.list_polozeni, name='list_polozeni'),
    path('polozeni/<int:id>/', views.list_all_polozeni, name='polozeni'),


]
