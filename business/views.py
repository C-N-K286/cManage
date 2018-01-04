# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import UserForm,BusinessForm,ClassForm,InstructorForm
from Class.models import Class
from business.models import Business,Instructor
import datetime
from student.models import Student
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


def checkClass(request,cid):
    cla = Class.objects.get(class_id=cid)
    print cla.business_id
    print request.user.business
    if cla.business_id==request.user.business:
        print 'working'
        return 1
    else:
        return 0
        
def checkStudent(request,cid,student):
    x = checkClass(request,cid)
    if x==1:
        cla = Class.objects.get(class_id=cid)
        try:
            cla.student.get(student_id=student)
            return 1
        except:
            return 0

def dashboard(request):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        try:
            print request.user.business.business_id
            return render(request,'business/dashboard/dashboard.html',{'username':request.user.username})
        except:
            logout(request)
            return redirect('/business/login')
def bUser(request):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        try:
            print request.user.business.business_id
            return render(request,'business/dashboard/user.html',{'user':request.user})
        except:
            logout(request)
            return redirect('/business/login')
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
                        print 'logged in'
                        print request.user.business.business_id 						
                        return redirect('/business/dashboard')
                    except:
                        logout(request)
                        return HttpResponse("<br><br><br><br><br><h1><center>Business Login Blocked!!<br> You are a student</center></h1>")
                else:
                    return render(request, 'business/login.html')
            else:
	            return redirect('/business/register')
        else:
	        return render(request, 'business/login.html')
    else:
	    return redirect('/business/dashboard')

def logout_user(request):
    logout(request)
    return redirect('/business/login')

def mClass(request):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        print "Its working"
        try:
            cur_id = request.user.business.business_id
        except:
            return redirect('/business/logout')
        try:
            cur_list = Class.objects.filter(business_id = cur_id)
        except:
            cur_list=[]
        return render(request,'business/classes.html',{'list':cur_list})

def csearch(request):
    if not request.user.is_authenticated():
        return redirect('/student/login')
    else:
        if request.method == "POST":
            qname = request.POST.get('qname',False)
        try:
            cur_id = request.user.business.business_id
        except:
            return redirect('/business/logout')
        try:
            ori = qname.split(" ")
            cur_list = []
            for i in ori:    
                cur_list += Class.objects.filter(business_id = cur_id,class_name__contains = i)
            cur_list = list(set(cur_list))
        except:
            cur_list=[]
        return render(request,'business/classes.html',{'list':cur_list})
        
def mInstructor(request):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        try:
            cur_id = request.user.business.business_id
        except:
            return redirect('/business/logout')
        try:
            cur_list = Instructor.objects.filter(business_id=cur_id)
        except:
            cur_list=[]
        return render(request,'business/instructors.html',{'list':cur_list})

def msearch(request):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        if request.method == "POST":
            qname = request.POST.get('qname',False)
        try:
            cur_id = request.user.business.business_id
        except:
            return redirect('/business/logout')
        try:
            ori = qname.split(" ")
            cur_list = []
            for k in ori:
                cur_list1 = Instructor.objects.filter(business_id=cur_id,first_name__contains = k)
                cur_list2 = Instructor.objects.filter(business_id=cur_id,middle_name__contains = k)
                cur_list3 = Instructor.objects.filter(business_id=cur_id,last_name__contains = k)
                cur_list4 = []
                for i in cur_list1:
                    cur_list4.append(i)
                for i in cur_list2:
                    cur_list4.append(i)
                for i in cur_list3:
                    cur_list4.append(i)
                cur_list +=cur_list4
            cur_list = list(set(cur_list))
        except:
            cur_list=[]
        return render(request,'business/instructors.html',{'list':cur_list})

def register(request):
    if not request.user.is_authenticated():
        user_form = UserForm(request.POST)
        business_form = BusinessForm(request.POST)
        print user_form.is_valid()
        print business_form.is_valid()
        if user_form.is_valid() and business_form.is_valid():
            print "working"
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user.set_password(password)
            user.is_active=False
            user.save()
            
            #user = authenticate(username=username, password=password)
            print user
            business = business_form.save(commit=False)
            business.user = user
            business.typeField = 'business'
            business.duration = datetime.timedelta(days=10)
            business.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Business account.'
            message = render_to_string('business/acc_active_email.html', {
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
            #return HttpResponse('Please confirm your email address to complete the registration')
            return redirect('/business/login',{'message':'Please Confirm Your email and login'})
        return render(request,'business/register.html')
    else:
        return redirect('/business/dashboard')

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
        return redirect('/business/dashboard')
    else:
        return HttpResponse('Activation link is invalid!')
def addClass(request):
    if not request.user.is_authenticated():
        return login_user(request)
    else:
        try:
            print request.user.business.business_id
            form = ClassForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.corse_duration = datetime.timedelta(hours=60)
                obj.duration = datetime.timedelta(days=10)
                obj.business_id = Business.objects.get(business_id = request.user.business.business_id)
                obj.save()
                return mClass(request)
            return render(request , 'business/CreateClass.html')
        except:
            logout_user(request)

def clone(request,cid):
    if not request.user.is_authenticated():
        return login_user(request)
    else:
        try:
            print request.user.business.business_id
            form = ClassForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.corse_duration = datetime.timedelta(hours=60)
                obj.duration = datetime.timedelta(days=10)
                obj.business_id = Business.objects.get(business_id = request.user.business.business_id)
                obj.save()
                return redirect('/business/manage')
            return render(request, 'business/cloneClass.html' , {'obj':Class.objects.get(class_id = cid)})
        except:
            logout_user(request)


def addInstructor(request):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        try:
            print request.user.business.business_id
            if request.method=="POST":
                '''email = request.POST.get('email')
                subject, from_email, to = 'hello',email, email
                text_content = 'Registration'
                html_content = str(get_current_site(request))+"/business/regInstructor/"+str(request.user.pk)+"/"
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect('/business/emails/manageInstructor')'''
                username = request.POST.get('username')
                email = request.POST.get('toEmail')
                subject = request.POST.get('subject')
                matter = request.POST.get('matter') 
                current_site = get_current_site(request)
                mail_subject = 'Activate your Business account.'
                message = render_to_string('business/emails/notification.html',{
                    'username':username,
                    'domain':current_site.domain,
                    'matter':matter,
                    'user' :request.user.pk
                })
                email = EmailMessage(
                            subject, message,request.user.email,[email]
                )
                email.send()
                return redirect('/business/manageInstructor')
            else:
                return render(request,'business/emails/mailInst.html')
        except:
            logout_user(request)		
def RegInstructor(request,uid):
    form = InstructorForm(request.POST)
    print form
    if form.is_valid():
        ins = form.save(commit=False)
        user = User.objects.get(pk=uid)
        obj = Business.objects.get(business_id = user.business.business_id)
        ins.business_id=obj
        ins.save()
        return HttpResponse('Thank You')
    return render(request,'business/addInstructor.html')


def details(request,cid):
    if not request.user.is_authenticated():
        return login_user(request)
    else:
        try:
            print request.user.business.business_id
            classdetails = Class.objects.get(class_id = cid)
            return render(request,'business/details.html',{'list':classdetails})
        except:
            logout_user(request)

def instructordetails(request,iid):
    if not request.user.is_authenticated():
        return login_user(request)
    else:
        try:
            print request.user.business.business_id
            instructordetails = Instructor.objects.get(instructor_id = iid)
            if request.method == "POST":
                subject = request.POST.get('subject')
                matter = request.POST.get('matter')
                mail = request.POST.get('toEmail')
                email = EmailMessage(
                    subject,matter,'krishnakarthik.g16@iiits.in',[mail]
                )
                email.send()
            return render(request,'business/instructordetails.html',{'list':instructordetails,'user':request.user})
        except:
            logout_user(request)


def update(request,cid):
    if not request.user.is_authenticated():
        return login_user(request)
    else:
        try:
            print request.user.business.business_id
            if request.method == 'POST':
                name = request.POST['class_name']
                sdate = request.POST['start']
                edate = request.POST['end']		
                location = request.POST['clocation']
                room = request.POST['croom']
                ins = request.POST['instructor']
                des = request.POST['desp']
                c_vari = request.POST['class_variable']
                s_vari = request.POST['start_variable']
                e_vari = request.POST['end_variable']		
                loc_vari = request.POST['location_variable']
                room_vari = request.POST['room_variable']
                ins_vari = request.POST['instructor_variable']
                des_vari = request.POST['description_variable']
        
                a = Class.objects.get( class_id = cid)
                temp =	a
                if name!= '' :
                    temp.class_name = name
                if sdate!= '':
                    temp.start_date = sdate
                if edate != '':
                    temp.end_date = edate 
                if location != '':
                    temp.class_location = location
                if room != '':
                    temp.allocated_room = room
                if ins != '':
                    temp.instructor = ins
                if des != '':
                    temp.description = des

                if c_vari!= '' :
                    temp.class_name_variable = c_vari
                if s_vari!= '':
                    temp.start_date_variable = s_vari
                if e_vari != '':
                    temp.end_date_variable = e_vari
                if loc_vari != '':
                    temp.class_location_variable = loc_vari
                if room_vari != '':
                    temp.allocated_room_variable = room_vari
                if ins_vari != '':
                    temp.instructor_variable = ins_vari
                if des_vari != '':
                    temp.description_variable = des_vari

                temp.save()
                return render(request,'business/details.html',{'list':temp})			
            else:
                basic = Class.objects.get( class_id = cid )
                temp1 = basic
                return render(request,'business/update.html', {'list':temp1})		
        except:
            logout_user(request)

def delete(request,cid):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        try:
            print request.user.business.business_id           		
            a = Class.objects.get( class_id = cid)
            a.delete()
            return redirect('/business/manage')
        except:
            logout_user(request)
         
        a = Class.objects.get( class_id = cid)
        a.delete()
        return redirect('/business/manage')
   
def deleteInstructor(request,iid):
    a = Instructor.objects.get(instructor_id = iid)
    a.delete()
    return redirect('/business/manageInstructor')

def mStudent(request):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        try:
            cur_id = request.user.business.business_id
        except:
            return redirect('/business/logout')
        try:
            cur_list = Class.objects.filter(business_id = cur_id)
            student_list={}
            lis=[]
            for i in cur_list:
                x = i.student.all()
                z=[]
                for j in x:
                    z.append(j.user)
                student_list[i] = z
        except:
            cur_list=[]
            student_list=[]
        print student_list
        return render(request,'business/mStudent.html',{'list':student_list})

def search(request):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        try:
            cur_id = request.user.business.business_id
            if request.method == "POST":
                qname = request.POST.get('qname', False)
        except:
            return redirect('/business/logout')
        try:
            '''qset = Q()
            for term in qname.split():
                qset |= Q(class_name__contains=term)'''
            cur_list = Class.objects.filter(business_id = cur_id, class_name__contains = qname)
            student_list={}
            lis=[]
            for i in cur_list:
                x = i.student.all()
                z=[]
                for j in x:
                    z.append(j.user)
                student_list[i] = z
        except:
            cur_list=[]
            student_list=[]
        print student_list
        return render(request,'business/mStudent.html',{'list':student_list})


def sDetails(request,studentid,cid):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        try:
            print request.user.business.business_id
            x= checkClass(request,cid)
            y = checkStudent(request,cid,studentid)
            if x ==1 and y==1:
                print 'working'
                student = Student.objects.get(student_id=studentid)
                clas = Class.objects.get(class_id = cid)
                user =student.user
                return render(request,'business/sDetails.html',{'user':user,'class':clas})
            else:
                return redirect('/business/manageStudents/')
        except:
            logout_user(request)		

def sDelete(request,studentid,cid):
    if not request.user.is_authenticated():
        return redirect('/business/login')
    else:
        try:
            print request.user.business.business_id
            x= checkClass(request,cid)
            y = checkStudent(request,cid,studentid)
            if x ==1 and y==1:
                print studentid,cid
                student = Student.objects.get(student_id=studentid)
                clas = Class.objects.get(class_id = cid)
                clas.student.remove(student)
                clas.save()
                return redirect('/business/manageStudents')
            else:
                return redirect('/business/manageStudents/')
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
        return redirect('/business/login')
    else:
        try:
            cur_id = request.user.business.business_id
        except:
            return redirect('/business/logout')
        try:
           cur_list = Class.objects.filter(business_id = cur_id)
        except:
            cur_list=[]
        cList=parseJ(cur_list)
        #print list[cur_list]
        #cList = serializers.serialize('json',cur_list,fields=('class_name','start_date','end_date'))
        #print cList
        return render(request,'business/selectable.html',{'list':cur_list})