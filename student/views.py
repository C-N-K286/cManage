from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserForm,StudentForm
import datetime
from Class.models import Class
from student.models import Student

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from datetime import date

def check_class():
    act = Class.objects.filter(active_class=True)
    for i in act:
        if date.today() > i.end_date:
            i.active_class=False
            i.save()			

def dashboard(request):
    if not request.user.is_authenticated():
        return redirect('/student/login')
    else:
        try:
            print request.user.student.student_id
            check_class()
            clas = Class.objects.filter(active_class=True)  
            username = request.user.username
            return render(request,'student/dashboard/dashboard.html',{'class':clas,'username':username})
        except:
            logout(request)
            return redirect('/student/login') 

def search(request):
    if not request.user.is_authenticated():
        return redirect('/student/login')
    else:
        try:
            print request.user.student.student_id
            if request.method == "POST":
                qname = request.POST.get('qname',False)
            clas = Class.objects.filter(class_name__contains = qname)
            username = request.user.username
            return render(request,'student/dashboard/dashboard.html',{'class':clas,'username':username})
        except:
            logout(request)
            return redirect('/student/login') 

def login_user(request):
    if not request.user.is_authenticated():
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    try:  				
                        login(request, user)
                        print request.user.student.student_id
                        print 'logged in'
                        return redirect('/student/dashboard')
                    except:
                        logout(request)
                        return HttpResponse("<br><br><br><br><br><h1><center>Student Login Blocked!!<br> You own your student</center></h1>")
                else:
                    return render(request,'student/login.html')
            else:
	            return redirect('/student/register')
        else:
	        return render(request,'student/login.html')
    else:
	    return redirect('/student/dashboard')

def logout_user(request):
    logout(request)
    return redirect('/student/login')

def bUser(request):
    if not request.user.is_authenticated():
        return redirect('/student/login')
    else:
        try:
            print request.user.student.student_id
            return render(request,'student/dashboard/user.html',{'user':request.user})
        except:
            logout(request)
            return redirect('/student/login')
def register(request):
    if not request.user.is_authenticated():
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)
        print user_form
        print student_form
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            student = student_form.save(commit=False)
            student.user = user
            student.typeField = 'student'
            student.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Student account.'
            message = render_to_string('student/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('/student/login')
        return render(request,'student/Register.html')
    else:
        return redirect('/student/dashboard')



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('/student/dashboard')
    else:
        return HttpResponse('Activation link is invalid!')

def display(request):
    if not request.user.is_authenticated():
        return redirect('/student/login')
    else:
        try:
            print request.user.student.student_id 		
            enrol = []
            check_class() 			
            c = Class.objects.filter(active_class=True)
            for i in c:
                for j in i.student.all():
                    if j.student_id == request.user.student.student_id:
                        enrol.append(i)            			
         
            return render(request,'student/enroll.html',{'list':enrol})
        except:
            logout_user(requset)
		
def enroll(request,cid):
    if not request.user.is_authenticated():
        return redirect('/student/login') 
    else:
        try:
            print request.user.student.student_id 		
            if request.method == 'POST':
                p1 = Student.objects.get(student_id = request.user.student.student_id)
                a1 = Class.objects.get(class_id = cid)  
                a1.student.add(p1)
                a1.save()
                return redirect('/student/dashboard/')
        except:
            logout_user(requset)
        
def details(request,cid):
    if not request.user.is_authenticated():
        return redirect('/student/login') 
    else:
        try:
            print request.user.student.student_id 		
            classdetails = Class.objects.get(class_id = cid)
            return render(request,'student/details.html',{'list':classdetails})
        except:
            logout_user(request)

def parseJ(lis):
    qset = []
    for i in lis:
        var = i.get_date().split(",")
        qset.append(str({str('name'):str(var[0]),str('start_date'):str(var[1]),str('end_date'):str(var[2])}))
    print qset
    return qset

def calendar(request):
    if not request.user.is_authenticated():
        return redirect('/student/login')
    else:
        try:
            cur_id = request.user.student.student_id
        except:
            return redirect('/student/logout')
        try:
            print request.user.student.student_id 		
            cur_list = []  
            c = Class.objects.all()
            for i in c:
                for j in i.student.all():
                    if j.student_id == cur_id:
                        cur_list.append(i)            			
        except:
            cur_list=[]
        cList=parseJ(cur_list)
        return render(request,'student/selectable.html',{'list':cur_list})