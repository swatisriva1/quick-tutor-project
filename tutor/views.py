from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from . import templates

def welcome(request):
    #template_name = 'tutor/welcome.html'
    return render(request, 'tutor/welcome.html')