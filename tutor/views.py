from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from . import templates
from .models import Profile

class ProfileView(generic.ListView):
    model = Profile
    template_name = 'tutor/welcome.html'

    #for future, when we grab data from database, currently not functional
    def get_queryset(self):
        return Profile.objects.all()

    #renders the home landing page
    def welcome(request):
        return render(request, template_name)