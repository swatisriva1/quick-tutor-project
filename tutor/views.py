from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from . import templates
from .models import Profile
from .forms import List, EditProfile

class StudentProfileView(generic.ListView):
    model = Profile

    #for future, when we grab data from database, currently not functional
    def get(self, request):
      return render(request, 'tutor/student.html')

class ProfileUpdate(generic.ListView):
    model = Profile
    def get(self, request):
        form = List
        return render(request, 'tutor/studentUpdate.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = EditProfile(request.POST, instance=request.user.profile)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your account has been updated')
            return redirect('/student/')
        else:
            form = EditProfile(instance=request.user.profile)
        return render(request, 'tutor/studentUpdate.html', {'form': form})

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

