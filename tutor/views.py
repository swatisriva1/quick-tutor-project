from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.views import generic
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages

from django.urls import reverse_lazy, reverse

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
import decimal

@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class AccountHistory(generic.ListView):
    model = Job
    template_name = 'tutor/account_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        current_user = self.request.user
        as_tutor = Q(tutor_user = current_user) & Q(isComplete = True)
        as_student = Q(customer_user = current_user) & Q(isComplete = True) 
        context['as_tutor'] = Job.objects.filter(as_tutor)
        context['as_student'] = Job.objects.filter(as_student) 
        return context

"""     def get(self, request):
        if 'paid'  not in request.session:
            request.session['paid']='true'
        if (request.session.get('paid') != 'true'):
            return redirect('/payment')
        return render(request, 'tutor/account_history.html') """
    

@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class SessionInfo(generic.DetailView):
    model=Job
    template_name = 'tutor/session.html'


@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class AcceptedJobs(SingleTableView):
    model = Job
    template_name = 'tutor/acceptedjobs.html'
    context_object_name = 'job_list'
    def get_queryset(self):
        current_user = self.request.user
        return Job.objects.filter(tutor_user=current_user).filter(isComplete=False).filter(isCanceled=False)



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
        active = Q()
        for s in subjects_set:
            matches = matches | Q(subject=s.subject_name)
            available = available | Q(isConfirmed=False)
            selves = selves | Q(customer_user=current_user)
            active = active | Q(isCanceled=False)
        return Job.objects.filter(matches).filter(available).filter(active).exclude(selves)

    def post(self, request):
        if request.method == 'POST':
            if 'isTutor' not in request.session:
                request.session['isTutor'] = 'false'
            if 'paid' not in request.session:
                request.session['paid'] = 'true'
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
                request.session['isTutor']='true'
                return redirect(reverse_lazy('tutor:accepted'))
        return redirect(reverse_lazy('tutor:job_list'))

@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class RequestedJobs(generic.ListView):
    model = Job

    template_name = 'tutor/requested_jobs_list.html'
    context_object_name = 'job_list'

    def get_queryset(self):
        current_user = self.request.user
        return Job.objects.filter(customer_user=current_user).filter(isComplete=False).filter(isCanceled=False)


    def post(self, request):
        if 'begin-btn' in request.POST:
            begin_job = request.POST.get("id", False)
            b = Job.objects.get(id=begin_job)
            b.started = True
            b.save()
            messages.success(request, 'Your session has begun!')
            return redirect(reverse('tutor:session', args=(b.id,)))


@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class RequestTutorView(generic.ListView):
    model = Job

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
            if 'isTutor' not in request.session:
                request.session['isTutor'] = 'false'
            if form.is_valid():
                req = form.save(commit=False)
                req.customer_user = self.request.user
                req.customer_profile = self.request.user.profile
                req.save()
                request.session['isTutor']='false'
                messages.success(request, 'Your request has been submitted')
                return redirect(reverse_lazy('tutor:requests'))
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
                return redirect('/student/')

            else:
                messages.warning(request, 'Input not valid')
                return redirect('/updateinfo/')
        else:
            form = List(instance=request.user.profile)
            messages.error(request, 'Something went wrong. Please try again.')
        return render(request, 'tutor/studentUpdate.html', context)

@login_required(redirect_field_name='')
def welcome(request):
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

@login_required(redirect_field_name='')
def cancelSession(request, job_id=None):
    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        r = request.POST.get('button')
        last_tutor = Profile.objects.get(user=job.last_tutored_by)
        if(request.user == job.customer_user):
            current = float(last_tutor.rating)*last_tutor.jobinteractions
            last_tutor.jobinteractions += 1
            last_tutor.save()
            if(r == "1"):
                current += 1.0
                current = current/(last_tutor.jobinteractions)
                last_tutor.rating = decimal.Decimal(current)
            elif(r == "2"):
                current += 2.0
                current = current/(last_tutor.jobinteractions)
                last_tutor.rating = decimal.Decimal(current)
            elif(r == "3"):
                current += 3.0
                current = current/(last_tutor.jobinteractions)
                last_tutor.rating = decimal.Decimal(current)
            elif(r == "4"):
                current += 4.0
                current = current/(last_tutor.jobinteractions)
                last_tutor.rating = decimal.Decimal(current)    
            elif(r == "5"):
                current += 5.0
                current = current/(last_tutor.jobinteractions)
                last_tutor.rating = decimal.Decimal(current)
        if(request.user == job.last_tutored_by):
            current = float(job.customer_profile.rating)*job.customer_profile.jobinteractions
            job.customer_profile.jobinteractions += 1
            job.customer_profile.save()
            if(r == "1"):
                current += 1.0
                current = current/(job.customer_profile.jobinteractions)
                job.customer_profile.rating = decimal.Decimal(current)
            elif(r == "2"):
                current += 2.0
                current = current/(job.customer_profile.jobinteractions)
                job.customer_profile.rating = decimal.Decimal(current)
            elif(r == "3"):
                current += 3.0
                current = current/(job.customer_profile.jobinteractions)
                job.customer_profile.rating = decimal.Decimal(current)
            elif(r == "4"):
                current += 4.0
                current = current/(job.customer_profile.jobinteractions)
                job.customer_profile.rating = decimal.Decimal(current)    
            elif(r == "5"):
                current += 5.0
                current = current/(job.customer_profile.jobinteractions)
                job.cunstomer_profile.rating = decimal.Decimal(current)

        last_tutor.save()
        job.customer_profile.save()
    
    job.started = False
    job.isConfirmed = False
    job.tutor_user = None
    job.tutor_profile = None
    job.save()

    student = Profile.objects.get(user=job.customer_user)
    student.started = False
    student.save()
    messages.warning(request, 'Your session has been canceled.')
    if(request.session['isTutor']=="false"):
        return redirect(reverse_lazy('tutor:requests'))
    return redirect(reverse_lazy('tutor:accepted'))

@login_required(redirect_field_name='')
def cancelRequest(request, job_id=None):
    job = Job.objects.get(id=job_id)
    messages.warning(request, 'Your request has been canceled.')
    student = Profile.objects.get(user=job.customer_user)
    student.started = False
    student.save()
    job.isCanceled = True
    job.save()
    return redirect(reverse_lazy('tutor:requests'))

@login_required(redirect_field_name='')
def endSession(request, job_id=None):
    job = Job.objects.get(id=job_id)
    tutor = Profile.objects.get(user=job.last_tutored_by)
    current = float(tutor.rating)*tutor.jobinteractions
    tutor.jobinteractions += 1
    tutor.save()
    
    if request.method == 'POST':
        r = request.POST.get('button2')
        if(r == "1"):
            current += 1.0
            current = current/tutor.jobinteractions
            tutor.rating = decimal.Decimal(current)
        elif(r == "2"):
            current += 2.0
            current = current/tutor.jobinteractions
            tutor.rating = decimal.Decimal(current)
        elif(r == "3"):
            current += 3.0
            current = current/tutor.jobinteractions
            tutor.rating = decimal.Decimal(current)
        elif(r == "4"):
            current += 4.0
            current = current/tutor.jobinteractions
            tutor.rating = decimal.Decimal(current)    
        elif(r == "5"):
            current += 5.0
            current = current/tutor.jobinteractions
            tutor.rating = decimal.Decimal(current)
        tutor.save()

    job.save()
    messages.success(request, 'Your session has ended. Please provide your payment information below')
    return redirect(reverse_lazy('tutor:payment'))

@login_required(redirect_field_name='')
def beginSession(request, job_id=None):
    form = endSession
    job = Job.objects.get(id=job_id)
    job.last_tutored_by = job.tutor_user
    job.started = True
    job.save()
    if 'isTutor' not in request.session:
        request.session['isTutor'] = 'false'
    if request.session['isTutor'] =='false':
        student=Profile.objects.get(user=job.customer_user)
        student.started=True
        student.save()
    messages.success(request, 'Your session has begun!')
    return redirect(reverse_lazy('tutor:session', args=(job.id,)), {'form': form})

def index(request):
    return render(request, 'tutor/home.html')

@login_required(redirect_field_name='')
def payment(request):
    return render(request, 'tutor/payment.html')

def paymentConfirmation(request):
    request.session['paid'] = 'true'
    currentUser= Profile.objects.get(user=request.user)
    currentUser.started=False
    currentUser.save()
    for jobs in Job.objects.filter(customer_user = request.user):
        if jobs.started==True:
            jobs.isComplete=True
            jobs.save()
    # specify that the model is Job
    # access the current job instance (the one that you've paid for)
    # change that job's isComplete from false to true   
    return render(request, 'tutor/paymentConfirmation.html')