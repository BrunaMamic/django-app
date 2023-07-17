from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.forms import UserCreationForm
from seminar.models import User
from .decorators import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def list_subjects(request):
    if request.user.uloga.naziv == 'PROF':
        subjects = Predmeti.objects.filter(nositelj=request.user)
        professors = User.objects.filter(pk=request.user.pk) 
    else:
        subjects = Predmeti.objects.all()
        professors = User.objects.filter(uloga__naziv='PROF')

    return render(request, 'list_subjects.html', {'subjects': subjects, 'professors': professors})


@admin_required
def add_subject(request):
    if request.method == 'GET':
        form = NewSubjectForm()
        return render(request, 'add_subject.html', {'form':form})
    elif request.method == 'POST':
        form = NewSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subjects')
        else:
            return HttpResponseNotAllowed()
    else:
            return HttpResponseNotAllowed()

@admin_required   
def edit_subject(request,id):
    subject = Predmeti.objects.get(pk=id)
    if request.method == 'GET':
         form = NewSubjectForm(instance=subject)
         return render(request, 'edit_subject.html', {'form':form})
    elif request.method == "POST":
         form = NewSubjectForm(request.POST, instance=subject)
         if form.is_valid():
              form.save()
              return redirect('subjects')
         else:
              return HttpResponseNotAllowed()     

@admin_or_professor_required
def list_students_per_subjects(request, id):
    subject = Predmeti.objects.get(pk=id)
    enrollments = Upisi.objects.filter(predmet=subject).select_related('student')

    #FILTERI ZA PROFESORA
    status = request.GET.get('status', 'all')
    if status != 'all':
        enrollments = enrollments.filter(status=status)

    students = [{'student': enrollment.student, 'status': enrollment.status} for enrollment in enrollments]

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        new_status = request.POST.get('new_status')
        student = User.objects.get(pk=student_id)
        enrollment = Upisi.objects.get(student=student, predmet=subject)
        enrollment.status = new_status
        enrollment.save()

        return redirect('enroled_students', id=id)


    return render(request, 'list_of_students_per_subject.html', {'subject': subject, 'students': students, 'status': status})


@admin_required
def update_professor(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        professor_id = request.POST.get('professor_id')
        subject = Predmeti.objects.get(pk=subject_id)
        professor = User.objects.get(pk=professor_id)
        subject.nositelj = professor
        subject.save()
        
        return redirect('subjects')

#NOVI PAGE SA BROJEM STUDENATA KOJI IMAJU STATUS POLOZENO
@admin_required
def list_polozeni(request):
    subjects = Predmeti.objects.all()
    students = User.objects.filter(uloga__naziv='STU')
    counts = count_polozeni()

    return render(request, 'list_polozeni.html', {'subjects': subjects, 'students':students, 'counts': counts})


def count_polozeni():
    counts = {}
    subjects = Predmeti.objects.all().distinct()

    for subject in subjects:
        students_polozen = Upisi.objects.filter(predmet=subject, status='polozen').count()
        students_izvanredno = Upisi.objects.filter(predmet=subject, student__status='izvanredni', status='polozen').count()
        students_redovni = Upisi.objects.filter(predmet=subject, student__status='redovni', status='polozen').count()

        counts[subject.naziv] = {
            'polozen': students_polozen,
            'izvanredno': students_izvanredno,
            'redovno': students_redovni,
        }

    return counts

#SVI POLOZENI PO PREDMETU
@admin_required
def list_all_polozeni(request,id):
    subject = Predmeti.objects.get(pk=id)
    enrollments = Upisi.objects.filter(predmet=subject).select_related('student')

    status = request.GET.get('status','polozen')

    students = [{'student': enrollment.student, 'status': enrollment.status} for enrollment in enrollments if enrollment.status == 'polozen']
    print(students)
    return render(request, 'polozeni.html', {'subject': subject, 'students': students, 'status': status})


#STUDENTI

@login_required
@admin_or_student_required
def students(request):
    if request.user.uloga.naziv == 'STU':
        student = request.user
        return render(request, 'list_all_students.html', {'students_list': [student]})
    elif request.user.uloga.naziv == 'ADMIN':
        students_list = User.objects.filter(uloga__naziv="STU")
        return render(request, 'list_all_students.html', {'students_list': students_list})

    return HttpResponseForbidden()

@admin_required
def add_students(request):
    if request.method == 'GET':
        form = NewStudentForm()
        return render(request, 'add_students.html', {'form': form})
    elif request.method == 'POST':
        form = NewStudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students_list')
        else:
            return render(request, 'add_students.html', {'form': form})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@admin_required
def edit_student(request,id):
    student = User.objects.get(pk=id)
    if request.method == 'GET':
         form = NewStudentForm(instance=student)
         return render(request, 'edit_student.html', {'form':form})
    elif request.method == "POST":
         form = NewStudentForm(request.POST, instance=student)
         if form.is_valid():
              form.save()
              return redirect('students_list')
         else:
              return render(request, 'edit_student.html', {'form': form})
         

#PROFESORI
@admin_required
def professors(request):
     professors_list = User.objects.filter(uloga__naziv="PROF")
     return render(request, 'list_professors.html', {'professors_list': professors_list})

@admin_required
def add_professor(request):
    if request.method == 'GET':
          form = NewProfessorForm()
          return render(request, 'add_professors.html', {'form':form})
    elif request.method == 'POST':
          form = NewProfessorForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('professors_list')
          else:
            return render(request, 'add_professors.html', {'form': form})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@admin_required    
def edit_professor(request,id):
    professor = User.objects.get(pk=id)
    if request.method == 'GET':
         form = NewProfessorForm(instance=professor)
         return render(request, 'edit_professor.html', {'form':form})
    elif request.method == "POST":
         form = NewProfessorForm(request.POST, instance=professor)
         if form.is_valid():
              form.save()
              return redirect('professors_list')
         else:
              return render(request, 'edit_professor.html', {'form': form})  
         

#REGISTER
@admin_required
def register(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'register.html', {"form":form})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return redirect('register')
        

#LOGOUT
def custom_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


#UPISNI LIST

def enrollment_list(request, id):
    student = User.objects.filter(pk=id).first()
    enrollments = Upisi.objects.filter(student=student).select_related('predmet')

    enrolled_subjects = Upisi.objects.filter(student=student).values('predmet')
    enrolled_subjects = Predmeti.objects.filter(pk__in=enrolled_subjects)

    all_subjects = Predmeti.objects.exclude(pk__in=enrolled_subjects)

    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        print(subject_id)
        subject = get_object_or_404(Predmeti, pk=subject_id)
        Upisi.objects.create(student=student, predmet=subject)
        return redirect('enrollment_list', id=id)

    return render(request, 'upisni_list.html', {'student': student, 'enrollments': enrollments, 'enrolled_subjects': enrolled_subjects, 'all_subjects': all_subjects})

def unenroll_subject(request, subject_id, student_id):
    subject = Predmeti.objects.filter(pk=subject_id).first()
    student = User.objects.filter(pk=student_id).first()

    if request.method == 'POST':
        enrollment = Upisi.objects.get(student=student, predmet=subject)
        if enrollment.status == 'upisan':
            enrollment.delete()

    return redirect('enrollment_list', id=student_id)




    







