from django.test import TestCase
from django.urls import reverse
from brief_app.tests.common.utils import UtilTest

"""
[Test home]
"""
class HomeTest(TestCase):

    def setUp(self) -> None:
        self.url = reverse('home')

    def testInvalidHttpMethod(self):
        UtilTest.callPost(self, self.url, None, 405)

    def testShowHomePage(self):
        response = UtilTest.callGet(self, self.url)
        self.assertTemplateUsed(response, 'home.html')
