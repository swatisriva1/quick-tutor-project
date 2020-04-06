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
from django_tables2 import SingleTableView
from .tables import tutorJobs
from bootstrap_modal_forms.generic import BSModalCreateView
from . import templates
from .models import Profile, Job, Subject
from .forms import List, PicForm, EditProfile, RequestTutor, AvailableJobsForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required(redirect_field_name=''), name='dispatch')

class SessionInfo(generic.DetailView):
    model=Job
    template_name = 'tutor/session.html'



@method_decorator(login_required(redirect_field_name=''), name='dispatch')

class AcceptedJobs(SingleTableView):
    model = Job

    def get(self, request):
        jobs = Job.objects.filter(tutor_user=self.request.user)
        table = tutorJobs(jobs)
        return render(request, 'tutor/acceptedjobs.html', {
            "table":table, 
            "job": jobs,
        })

    def post(self, request):
        if 'begin-btn' in request.POST:
            begin_job = request.POST.get("id", False)
            b = Job.objects.get(id=begin_job)
            b.started = True
            b.save()
            messages.success(request, 'Your session has begun!')
            return redirect(reverse('tutor:session', args=(Job.id,)))


@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class AvailableJobs(generic.ListView):
    model = Job
    template_name = 'tutor/jobs_list.html'

    def get_queryset(self):
        current_user = self.request.user

        tutor_profile = Profile.objects.get(user=current_user)
        subjects_set = tutor_profile.subjects_can_help.all()
        matches = Q()
        available = Q()
        selves = Q()
        for s in subjects_set:
            matches = matches | Q(subject=s.subject_name)
            available = available | Q(isConfirmed=False)
            selves = selves | Q(customer_user=current_user)
        return Job.objects.filter(matches).filter(available).exclude(selves)

    def post(self, request):
        if request.method == 'POST':
            accepted_jobs = request.POST.getlist('selected_job')
            if not accepted_jobs:
                messages.warning(request, 'No job was selected.')
                return redirect(reverse_lazy('tutor:job_list'))
            else:
                for j in accepted_jobs:
                    match = Job.objects.get(id=j)
                    match.tutor_user = self.request.user
                    match.tutor_profile = self.request.user.profile
                    match.isConfirmed = True
                    match.save()
                    messages.success(request, 'Your job(s) have been confirmed!')
                return redirect(reverse_lazy('tutor:accepted'))
        return redirect(reverse_lazy('tutor:job_list'))

@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class RequestedJobs(generic.ListView):
    model = Job

    template_name = 'tutor/requested_jobs_list.html'
    context_object_name = 'job_list'
    def get_queryset(self):
        current_user = self.request.user
        return Job.objects.filter(customer_user=current_user)


    def post(self, request):
        if request.method == 'POST':
            return redirect(reverse('tutor:session', args=(Job.id,)))


@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class RequestTutorView(generic.ListView):
    model = Job
    # Job.objects.all().delete()

    def get(self, request):
        form = RequestTutor()
        if 'paid'  not in request.session:
            request.session['paid']='true'
        if (request.session.get('paid') != 'true'):
            return redirect('/payment')
        return render(request, 'tutor/requestTutor.html', {'form': form})

    def post(self, request):
        form = RequestTutor(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                req = form.save(commit=False)
                req.customer_user = self.request.user
                req.customer_profile = self.request.user.profile
                req.save()
                request.session['paid']='false'
                messages.success(request, 'Your request has been submitted')
                return redirect(reverse_lazy('tutor:index'))
            return render(request, 'tutor/requestTutor.html', {'form': form})

@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class StudentProfileView(generic.ListView):
    model = Profile

    def get(self, request):
        return render(request, 'tutor/student.html')

@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class ProfileUpdate(generic.ListView):
    model = Profile

    def get(self, request):
        current_user = request.user
        if 'paid'  not in request.session:
            request.session['paid']='true'
        if (request.session.get('paid') != 'true'):
            return redirect('/payment')
        try:
            prof = Profile.objects.get(user=current_user)
            form = List(instance=prof)
            pic_form = PicForm(instance=prof)
            context = {
                'form': form, 
                'pic_form': pic_form
            }

        except ObjectDoesNotExist:
            form = List()
            pic_form = PicForm() 
            context = {
                'form': form, 
                'pic_form': pic_form
            }
        return render(request, 'tutor/studentUpdate.html', context)

    def post(self, request):
        if request.method == 'POST':
            form = List(request.POST, instance=request.user.profile)
            pic_form = PicForm(request.POST, request.FILES, instance=request.user.profile)
            context = {
                'form': form, 
                'pic_form': pic_form
            }
            if form.is_valid() and pic_form.is_valid():
                # handle file
                form.save()
                pic_form.save()
                messages.success(request, f'Your account has been updated')
                return redirect('/student')

            else:
                messages.warning(request, 'Input not valid')
                return redirect('/updateinfo/')
        else:
            form = List(instance=request.user.profile)
            messages.error(request, 'Something went wrong. Please try again.')
        return render(request, 'tutor/studentUpdate.html', context)

# renders the home landing page

@login_required(redirect_field_name='')
def welcome(request):
    if 'paid' not in request.session:
        request.session['paid'] = 'true'
    if (request.session.get('paid') != 'true'):
        return redirect('/payment')
    return render(request, 'tutor/welcome.html')

@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class TutorProfileView(generic.ListView):
    model = Profile
    template_name = 'tutor/tutorprofile.html'

    # for future, when we grab data from database, currently not functional
    def get_queryset(self):
        return Profile.objects.all()

    # renders the tutor profile page
    def tutorprofile(request):
        return render(request, template_name)


def index(request):
    if 'paid' not in request.session:
        request.session['paid'] = 'true'
    if (request.session.get('paid') != 'true'):
        return redirect('/payment')
    return render(request, 'tutor/home.html')

@login_required(redirect_field_name='')
def payment(request):
    return render(request, 'tutor/payment.html')
def paymentConfirmation(request):
    request.session['paid'] = 'true'
    return render(request, 'tutor/paymentConfirmation.html')