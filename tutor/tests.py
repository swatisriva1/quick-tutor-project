from django.test import TestCase, Client
from tutor.models import Subject, Profile, Job
from django.contrib.auth.models import User
from tutor.forms import List, RequestTutor
from tutor import views
from django.urls import reverse
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
        self.assertEquals(max_length, 200)

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
        
    # Profile lacking the proper fields (subjects_can_help, first_name, last_name in this case) should return false
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
        sub = Subject(subject_name='math')
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

class StudentProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/student/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class AvailableJobsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/jobs/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class ProfileUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/updateinfo/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class RequestedJobsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/requests/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class AcceptedJobsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/acceptedjobs/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class RequestTutorViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    # If user is not authenicated, should be redirect to welcome page (index) where they can login
    def test_anonymous_user_redirect(self):
        response = self.client.get('/requesttutor/')
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse('tutor:index'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
