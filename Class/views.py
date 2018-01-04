# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render

def addClass(request):
    if not request.user.is_authenticated():
        return render(request,'business/login.html')
    else:
        return render(request,'Class/CreateClass.html')