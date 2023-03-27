from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User


class AdminRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password1', 'password2','gender','birthDate','salary','address','landmark','city', 'state','profile_pic')
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()
        return user    

class ManagerRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password1', 'password2','gender','birthDate','salary','address','landmark','city', 'state','profile_pic')
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_manager = True
        user.save()
        return user    


class DeveloperRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password1', 'password2','gender','birthDate','salary','address','landmark','city', 'state','profile_pic')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_developer = True
        user.save()
        return user