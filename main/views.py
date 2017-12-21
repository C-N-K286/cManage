# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

def home(request):
    return render(request,'main/index.html')