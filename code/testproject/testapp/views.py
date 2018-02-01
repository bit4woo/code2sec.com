# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    x= request.session
    print dir(x)
    print x.serializer
    print x['userid']
    return HttpResponse(x)