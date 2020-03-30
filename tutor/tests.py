from django.test import TestCase, Client
from tutor.models import Subject, Profile, Job
from django.contrib.auth.models import User

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
        #Profile.objects.create(user=test_user, phone_number='4797998232', first_name='test', last_name='user', email_addr='test@gmail.com', rating=4.59)

    # User should automatically have a profile when created due to signal
    def test_user_has_profile(self):
        self.assertTrue(hasattr(self.test_user, 'profile'))

    def test_first_name_max_length(self):
        profile = Profile.objects.get(user=self.test_user)
        max_length = profile._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 200)

    # ** figure out how to edit profile-specific fields

"""     def test_to_str(self):
        to_str = str(self.test_user)
        self.assertEquals(to_str, "First Last") """

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
