from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.views import generic
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from bootstrap_modal_forms.generic import BSModalCreateView
from . import templates
from .models import Profile, Job, Subject
from .forms import List, EditProfile, RequestTutor

class AvailableJobs(generic.ListView):
    model = Job
    template_name = 'tutor/jobs_list.html'
    def get_queryset(self):
        current_user = self.request.user
        tutor_profile = Profile.objects.get(user=current_user)
        subjects_set = tutor_profile.subjects_can_help.all()
        matches = Q()
        for s in subjects_set:
            matches = matches | Q(subject=s.subject_name)
        return Job.objects.filter(matches)

class RequestTutorView(generic.ListView):
    model = Job
    #Job.objects.all().delete()
    def get(self, request):
        form = RequestTutor()
        return render(request, 'tutor/requestTutor.html', {'form': form})
    
    def post(self, request):
        form = RequestTutor(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                req = form.save(commit=False)
                req.user = self.request.user
                req.client = self.request.user.profile
                req.save()
                messages.success(request, 'Your request has been submitted')
                return redirect(reverse_lazy('tutor:index'))
            return render(request, 'tutor/requestTutor.html', {'form': form})


class StudentProfileView(generic.ListView):
    model = Profile
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

