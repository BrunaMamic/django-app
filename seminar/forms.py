from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
from django import forms
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class NewSubjectForm(ModelForm):
    class Meta:
        model = Predmeti
        fields = '__all__'

class NewStudentForm(ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    uloga = forms.ModelChoiceField(queryset=Uloge.objects.filter(naziv='STU'), initial=Uloge.objects.get(naziv='STU'))
    
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'username', 'uloga', 'status']
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already taken. Choose a different one.")
        return username

    def clean_password2(self): #custom validation for the name field
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True): #save in database
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class NewProfessorForm(ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    uloga = forms.ModelChoiceField(queryset=Uloge.objects.filter(naziv='PROF'), initial=Uloge.objects.get(naziv='PROF'))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'uloga']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username is already taken. Choose a different one.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpisiForm(forms.ModelForm):
    class Meta:
        model = Upisi
        fields = ['status']
