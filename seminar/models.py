from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Uloge(models.Model):
    naziv = models.CharField(max_length=20, choices=(
        ('ADMIN', 'admin'),
        ('PROF', 'profesor'),
        ('STU', 'student'),
    ))

    def __str__(self):
        return self.naziv


class User(AbstractUser):
    uloga = models.ForeignKey(Uloge, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=(('none', 'None'),('redovni', 'Redovni'), ('izvanredni', 'Izvanredni')))
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username
    

class Predmeti(models.Model):
    naziv = models.CharField(max_length=255)
    nositelj = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profesor', limit_choices_to={'uloga__naziv': 'PROF'})
    kod = models.CharField(max_length=50)
    program = models.TextField()
    ects = models.IntegerField()
    sem_red = models.CharField(max_length=10)
    sem_izv = models.CharField(max_length=10)
    izborni = models.CharField(max_length=2, choices=(('da', 'Da'), ('ne', 'Ne')))

    def __str__(self):
        return '%s' %(self.naziv)

class Upisi(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=(('polozen', 'Položen'),('pad', 'Izgubio pravo'), ('upisan', 'Upisan')), default='upisan')

    def __str__(self):
        return '%s %s' %(self.student.username, self.predmet.naziv)