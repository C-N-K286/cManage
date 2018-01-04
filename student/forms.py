from django import forms
from django.contrib.auth.models import User
from student.models import Student
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',]

class StudentForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = [ 'phone_no',]
