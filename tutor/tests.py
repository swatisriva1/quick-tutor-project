from django.test import TestCase, Client
from tutor.models import Subject, Profile, Job
from django.contrib.auth.models import User
from tutor.forms import List, RequestTutor, PicForm
from tutor import views
from django.urls import reverse
from tutor.views import AvailableJobs
# Create your tests here.

class DummyTestCase(TestCase):
    def setUp(self):
        x = 2

    def test_dummy_test_case(self):
        self.assertEqual(2, 2)

class ProfileModelTest(TestCase):
    def setUp(self):
        # creates dummy user object, can be reused in other tests
        self.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')

    # User should automatically have a profile when created due to signal
    def test_user_has_profile(self):
        self.assertTrue(hasattr(self.test_user, 'profile'))

    def test_first_name_max_length(self):
        profile = Profile.objects.get(user=self.test_user)
        max_length = profile._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 30)

    # ** figure out how to edit profile-specific fields


class SubjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_subject = Subject.objects.create(subject_name='test')
        #cls.test_subject2 = Subject.objects.create(subject_name='math')
        #cls.test_subject3 = Subject.objects.create(subject_name='science')

    def test_subject_name_max_length(self):
        self.max_length = self.test_subject._meta.get_field('subject_name').max_length
        self.assertEquals(self.max_length, 30)

    def test_subject_name(self):
        name = str(self.test_subject)
        self.assertEquals(name, 'test')

    def test_ordering(self):
        Subject.objects.create(subject_name="math")
        Subject.objects.create(subject_name="science")
        all_subjects = Subject.objects.all()
        first_sub_name = all_subjects[0].subject_name
        self.assertEqual(first_sub_name, "math")

# Examples of form testing
class ListFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        
    # Profile lacking the proper fields (subjects_can_help, first_name, last_name, phone_number in this case) should return false
    def test_empty_profile(self):
        profile = Profile.objects.get(user=self.test_user)
        form = List(data={'first_name': profile.first_name, 'last_name': profile.last_name, 'email_addr': profile.email_addr, 
            'phone_number': profile.phone_number, 'subjects_can_help': profile.subjects_can_help.all()}, instance=profile)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    # Profile including all fields and proper format should return true
    def test_proper_profile(self):
        profile = Profile.objects.get(user=self.test_user)
        profile.first_name = 'Test'
        profile.last_name = 'User'
        profile.email_addr = 'test@gmail.com'
        profile.phone_number = '+5555555555'
        sub = Subject(subject_name='math')
        sub.save()
        profile.subjects_can_help.add(sub)
        profile.save()
        form = List(data={'first_name': profile.first_name, 'last_name': profile.last_name, 'email_addr': profile.email_addr, 
            'phone_number': profile.phone_number, 'subjects_can_help': profile.subjects_can_help.all()}, instance=profile)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        
    # Profile w/o a proper phone number should return false
    def test_improper_phone_number_profile(self):
        profile = Profile.objects.get(user=self.test_user)
        profile.first_name = 'Test'
        profile.last_name = 'User'
        profile.email_addr = 'test@gmail.com'
        profile.phone_number = 'improper input'
        sub = Subject(subject_name='math')
        sub.save()
        profile.subjects_can_help.add(sub)
        profile.save()
        form = List(data={'first_name': profile.first_name, 'last_name': profile.last_name, 'email_addr': profile.email_addr, 
            'phone_number': profile.phone_number, 'subjects_can_help': profile.subjects_can_help.all()}, instance=profile)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    # Profile w/o any subjects selected should return false
    def test_no_subjects_selected_profile(self):
        profile = Profile.objects.get(user=self.test_user)
        profile.first_name = 'Test'
        profile.last_name = 'User'
        profile.email_addr = 'test@gmail.com'
        profile.phone_number = '+5555555555'
        profile.save()
        form = List(data={'first_name': profile.first_name, 'last_name': profile.last_name, 'email_addr': profile.email_addr, 
            'phone_number': profile.phone_number, 'subjects_can_help': profile.subjects_can_help.all()}, instance=profile)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid()) 

     # Profile w/o a proper email should return false
    def test_improper_email_addr_profile(self):
        profile = Profile.objects.get(user=self.test_user)
        profile.first_name = 'Test'
        profile.last_name = 'User'
        profile.email_addr = 'improper input'
        profile.phone_number = '+5555555555'
        sub = Subject(subject_name='Mathematics')
        sub.save()
        profile.subjects_can_help.add(sub)
        profile.save()
        form = List(data={'first_name': profile.first_name, 'last_name': profile.last_name, 'email_addr': profile.email_addr, 
            'phone_number': profile.phone_number, 'subjects_can_help': profile.subjects_can_help.all()}, instance=profile)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

class RequestTutorFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        cls.profile = Profile.objects.get(user=cls.test_user)

    # Form should not be valid for job w/ all default fields (some default to empty)
    def test_default_job(self):
        test_job = Job.objects.create(customer_user=self.test_user, customer_profile=self.profile)
        form = RequestTutor(data={'subject': test_job.subject, 'course': test_job.course, 'location': test_job.location, 'notes': test_job.notes}, instance=test_job)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    # Form with required fields properly filled should be valid
    def test_proper_job(self):
        test_job = Job.objects.create(customer_user=self.test_user, customer_profile=self.profile, course='TEST 2020', notes='testing', location='Alderman Library in Charlottesville, Virginia')
        form = RequestTutor(data={'subject': test_job.subject, 'course': test_job.course, 'location': test_job.location, 'notes': test_job.notes}, instance=test_job)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    # Form with improper course name should not be valid, course subject code should be capitalized and there should be a space between it and course number
    def test_improper_course_job(self):
        test_job = Job.objects.create(customer_user=self.test_user, customer_profile=self.profile, course='test2020', notes='testing', location='Alderman Library')
        form = RequestTutor(data={'subject': test_job.subject, 'course': test_job.course, 'location': test_job.location, 'notes': test_job.notes}, instance=test_job)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

class StudentProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/student/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # logged in user is not redirected and shown proper template (student.html)
    def test_logged_in_user(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.client.force_login(self.test_user)
        response = self.client.get('/student/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='tutor/student.html')

class AvailableJobsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.test_user1 = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        cls.test_user2 = User.objects.create_user(username='testuser2', password='12345', email='test2@gmail.com')
        cls.profile = Profile.objects.get(user=cls.test_user1)

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/jobs/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # logged in user is not redirected and shown proper template (jobs_list.html)
    def test_logged_in_user(self):
        self.client.force_login(self.test_user1)
        response = self.client.get('/jobs/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='tutor/jobs_list.html')

    # If a user can tutor in a subject, then avaiable jobs in that shubject should be shown; those in other subjects should not be shown
    def test_queryset(self):
        self.client.force_login(self.test_user1)
        self.profile = Profile.objects.get(user=self.test_user1)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        sub2 = Subject(subject_name='Mathematics')
        sub2.save()
        customer = Profile.objects.get(user=self.test_user2)
        test_job1 = Job.objects.create(customer_user=self.test_user2, customer_profile=customer, course='TEST 2020', notes='testing', location='Alderman Library', subject=sub1)
        test_job2 = Job.objects.create(customer_user=self.test_user2, customer_profile=customer, course='TEST 2020', notes='testing', location='Alderman Library', subject=sub2)
        response = self.client.get('/jobs/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='tutor/jobs_list.html')
        self.assertListEqual(list(response.context['object_list']), list(Job.objects.filter(subject=sub1)))

    # if no job is selected, should redirect back to list of available jobs
    def test_post_no_selected_job(self):
        self.client.force_login(self.test_user1)
        self.profile = Profile.objects.get(user=self.test_user1)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        sub2 = Subject(subject_name='Mathematics')
        sub2.save()
        customer = Profile.objects.get(user=self.test_user2)
        test_job1 = Job.objects.create(customer_user=self.test_user2, customer_profile=customer, course='TEST 2020', notes='testing', location='Alderman Library', subject=sub1)
        test_job2 = Job.objects.create(customer_user=self.test_user2, customer_profile=customer, course='TEST 2020', notes='testing', location='Alderman Library', subject=sub2)
        response = self.client.post('/jobs/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:job_list'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # if a single job is selected, redirects to accepted jobs list
    def test_post_single_selected_job(self):
        self.client.force_login(self.test_user1)
        self.profile = Profile.objects.get(user=self.test_user1)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        customer = Profile.objects.get(user=self.test_user2)
        test_job1 = Job.objects.create(customer_user=self.test_user2, customer_profile=customer, course='TEST 2020', notes='testing', location='Alderman Library', subject=sub1)
        response = self.client.post('/jobs/', data={'selected_job': Job.objects.filter(subject=sub1).values_list('id', flat=True)})
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:accepted'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # if multiple jobs are selected, redirects to accepted jobs list
    def test_post_multiple_selected_jobs(self):
        self.client.force_login(self.test_user1)
        self.profile = Profile.objects.get(user=self.test_user1)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        customer = Profile.objects.get(user=self.test_user2)
        test_job1 = Job.objects.create(customer_user=self.test_user2, customer_profile=customer, course='TEST 2020', notes='testing', location='Alderman Library', subject=sub1)
        test_job2 = Job.objects.create(customer_user=self.test_user2, customer_profile=customer, course='TEST 3030', notes='testing second', location='Alderman Library', subject=sub1)
        response = self.client.post('/jobs/', data={'selected_job': Job.objects.filter(subject=sub1).values_list('id', flat=True)})
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:accepted'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class ProfileUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/updateinfo/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # logged in user is not redirected and shown proper template (studentUpdate.html)
    def test_logged_in_user(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/updateinfo/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='tutor/studentUpdate.html')

    # successful form submission should redirect to student profile page
    def test_successful_redirect(self):
        self.client.force_login(self.test_user)
        self.profile = Profile.objects.get(user=self.test_user)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        sub2 = Subject(subject_name='Mathematics')
        sub2.save()
        self.profile.subjects_can_help.add(sub2)
        self.profile.save()
        response = self.client.post('/updateinfo/', data={'first_name': self.profile.first_name, 'last_name': self.profile.last_name, 'email_addr': self.profile.email_addr, 
                'phone_number': self.profile.phone_number, 'subjects_can_help': self.profile.subjects_can_help.all().values_list('id', flat=True), 'pic': self.profile.pic})
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:student'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # unsuccessful form submission (improper phone number in this case) should redirect back to updateprofile page
    def test_unsuccessful_redirect(self):
        self.client.force_login(self.test_user)
        self.profile = Profile.objects.get(user=self.test_user)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = 'improper input'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        sub2 = Subject(subject_name='Mathematics')
        sub2.save()
        self.profile.subjects_can_help.add(sub2)
        self.profile.save()
        response = self.client.post('/updateinfo/', data={'first_name': self.profile.first_name, 'last_name': self.profile.last_name, 'email_addr': self.profile.email_addr, 
                'phone_number': self.profile.phone_number, 'subjects_can_help': self.profile.subjects_can_help.all().values_list('id', flat=True), 'pic': self.profile.pic})
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:updateinfo'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)


class RequestedJobsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/requests/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # logged in user is not redirected and shown proper template (requested_jobs_list.html)
    def test_logged_in_user(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.client.force_login(self.test_user)
        response = self.client.get('/requests/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='tutor/requested_jobs_list.html')

    # View not display any jobs if user has not requested any
    def test_queryset_with_no_jobs_requested(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.client.force_login(self.test_user)
        self.profile = Profile.objects.get(user=self.test_user)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        response = self.client.get('/requests/')
        self.assertEqual(200, response.status_code)
        self.assertListEqual(list(response.context['object_list']), list(Job.objects.filter(customer_user=self.test_user)))

    # View should display all requested jobs
    def test_queryset_with_multiple_jobs_requested(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.client.force_login(self.test_user)
        self.profile = Profile.objects.get(user=self.test_user)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        test_job1 = Job.objects.create(customer_user=self.test_user, customer_profile=self.profile, course='TEST 2020', notes='testing', location='Alderman Library', subject=sub1)
        test_job2 = Job.objects.create(customer_user=self.test_user, customer_profile=self.profile, course='TEST 3030', notes='testing second', location='Alderman Library', subject=sub1)
        response = self.client.get('/requests/')
        self.assertEqual(200, response.status_code)
        self.assertListEqual(list(response.context['object_list']), list(Job.objects.filter(customer_user=self.test_user)))
    
class AcceptedJobsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        cls.test_user2 = User.objects.create_user(username='testuser2', password='12345', email='test2@gmail.com')

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/acceptedjobs/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # logged in user is not redirected and shown proper template (acceptedjobs.html)
    def test_logged_in_user(self):
        self.client.force_login(self.test_user)
        response = self.client.get('/acceptedjobs/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='tutor/acceptedjobs.html')

    # Should return an empty list if no jobs have been accepted
    def test_get_no_accepted_jobs(self):
        self.client.force_login(self.test_user)
        self.profile = Profile.objects.get(user=self.test_user)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        test_job1 = Job.objects.create(customer_user=self.test_user, customer_profile=self.profile, course='TEST 2020', notes='testing', location='Alderman Library', subject=sub1)
        response = self.client.get('/acceptedjobs/')
        self.assertEqual(200, response.status_code)
        self.assertListEqual(list(response.context['job']), list(Job.objects.filter(tutor_user=self.test_user)))

    # Should return list of accepted jobs if a job has been accepted
    def test_get_accepted_jobs(self):
        self.client.force_login(self.test_user)
        self.profile = Profile.objects.get(user=self.test_user)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        customer = Profile.objects.get(user=self.test_user2)
        test_job1 = Job.objects.create(customer_user=self.test_user2, customer_profile=customer, tutor_user=self.test_user, tutor_profile=self.profile, course='TEST 2020', notes='testing', location='Alderman Library', subject=sub1)
        response = self.client.get('/acceptedjobs/')
        self.assertEqual(200, response.status_code)
        self.assertListEqual(list(response.context['job']), list(Job.objects.filter(tutor_user=self.test_user)))

    # Starting a job should change boolean value and redirect to the session page
    def test_post(self):
        self.client.force_login(self.test_user)
        self.profile = Profile.objects.get(user=self.test_user)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        customer = Profile.objects.get(user=self.test_user2)
        self.test_job1 = Job.objects.create(customer_user=self.test_user2, customer_profile=customer, course='TEST 2020', notes='testing', location='Alderman Library', subject=str(sub1))
        self.test_job1.tutor_user = self.test_user
        self.test_job1.tutor_profile = self.profile
        self.test_job1.save()
        response = self.client.post('/acceptedjobs/', data={'begin-btn': True, 'id': self.test_job1.id})
        url = reverse('tutor:session', args=(self.test_job1.id,))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)


class RequestTutorViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/requesttutor/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # logged in user is not redirected and shown proper template (acceptedjobs.html)
    def test_logged_in_user(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.client.force_login(self.test_user)
        response = self.client.get('/requesttutor/')
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='tutor/requestTutor.html')

    # Requesting a tutor with proper form input should redirect to requests view where new job should be found
    def test_request_proper_input(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.client.force_login(self.test_user)
        self.profile = Profile.objects.get(user=self.test_user)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        response = self.client.post('/requesttutor/', data={'customer_user': self.test_user, 'customer_profile': self.profile, 'course': 'TEST 2020', 'notes': 'testing', 'location': 'Alderman Library', 'subject': str(sub1)})
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:requests'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        redir_response = self.client.get('/requests/')
        self.assertListEqual(list(redir_response.context['object_list']), list(Job.objects.filter(customer_user=self.test_user)))
        self.assertEqual(len(list(redir_response.context['object_list'])), 1)

    # Requesting a tutor with improper form input should return RequestTutor view, no redirect occurs
    def test_request_improper_input(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.client.force_login(self.test_user)
        self.profile = Profile.objects.get(user=self.test_user)
        self.profile.first_name = 'Test'
        self.profile.last_name = 'User'
        self.profile.email_addr = 'test@gmail.com'
        self.profile.phone_number = '+5555555555'
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        self.profile.subjects_can_help.add(sub1)
        self.profile.save()
        response = self.client.post('/requesttutor/', data={'customer_user': self.test_user, 'customer_profile': self.profile, 'course': 'improper', 'notes': 'testing', 'location': 'Alderman Library', 'subject': str(sub1)})
        self.assertEqual(200, response.status_code)
        self.assertFormError(response, 'form', 'course', 'Enter a valid course code using following format: TEST 2010 (Make sure to capitalize the course subject!)')

class SessionInfoViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    # If user is not authenicated, should be redirected to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        self.test_user = User.objects.create_user(username='testuser', password='12345', email='test@gmail.com')
        self.profile = Profile.objects.get(user=self.test_user)
        sub1 = Subject(subject_name='Physics')
        sub1.save()
        test_job1 = Job.objects.create(customer_user=self.test_user, customer_profile=self.profile, course='TEST 2020', notes='testing', location='Alderman Library', subject=sub1)
        url = reverse('tutor:session', args=(test_job1.id,))
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
    