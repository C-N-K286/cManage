from django import forms
from django.contrib.auth.models import User
from business.models import Business,Instructor
from Class.models import Class
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',]

class BusinessForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Business
        fields = [ 'phone_no','business',]

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name','start_date','end_date','class_location','allocated_room','description']
class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields=['first_name','last_name','middle_name','address','ssn','email','telephone']