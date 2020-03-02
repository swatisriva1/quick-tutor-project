from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import templates
from .models import Profile

class ProfileView(generic.ListView):
    model = Profile

    #for future, when we grab data from database, currently not functional
    def get_queryset(self):
        return Profile.objects.all()
    def register(request):
        form = UserCreationForm()
        return render(request, 'tutor/student.html', {'form': form})

    #renders the home landing page
    
def welcome(request):
        return render(request, 'tutor/welcome.html')

class TutorProfileView(generic.ListView):
    model = Profile
    template_name = 'tutor/tutorprofile.html'

    #for future, when we grab data from database, currently not functional
    def get_queryset(self):
        return Profile.objects.all()

    #renders the tutor profile page
    def tutorprofile(request):
        return render(request, template_name)
    

def index(request):
    return render(request, 'tutor/home.html')

