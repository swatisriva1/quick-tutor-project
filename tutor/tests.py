from django.test import TestCase, Client
from tutor.models import Subject, Profile, Job
from django.contrib.auth.models import User
from . import signals

# Create your tests here.

class DummyTestCase(TestCase):
    def setUp(self):
        x = 2

    def test_dummy_test_case(self):
        self.assertEqual(2, 2)

class SubjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_subject = Subject.objects.create(subject_name='test')

    def test_subject_name_max_length(self):
        self.max_length = self.test_subject._meta.get_field('subject_name').max_length
        self.assertEquals(self.max_length, 30)