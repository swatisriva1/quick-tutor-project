from django.test import TestCase


# Create your tests here.

class DummyTestCase(TestCase):
    def setUp(self):
        x = 3

    def test_dummy_test_case(self):
        self.assertEqual(3, 3)