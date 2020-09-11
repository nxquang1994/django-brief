from django.test import TestCase
from django.urls import reverse
from unittest import mock
from rest_framework.views import status
from brief_app.tests.common.utils import UtilTest
from common_app.models import RssFeedItem

class CreateItemTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse('createItem')

    def testShowCreateItem(self):
        response = UtilTest.callGet(self, self.url)
        self.assertTemplateUsed(response, 'items/create.html')

    def testCategoryReqquired(self):
        params = None

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>category<ul class="errorlist"><li>This field is required.</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/create.html')

    def testCategoryOver50Characters(self):
        category = ''
        for i in range(51):
            category += '1'

        params = {
            'category': category
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>category<ul class="errorlist"><li>Ensure this value has at most 50 characters (it has 51).</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/create.html')

    def testTitleReqquired(self):
        params = {
            'category': 'unit_test_category'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>title<ul class="errorlist"><li>This field is required.</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/create.html')

    def testTitleOver255Characters(self):
        title = ''
        for i in range(256):
            title += '1'

        params = {
            'category': 'unit_test_category',
            'title': title
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>title<ul class="errorlist"><li>Ensure this value has at most 255 characters (it has 256).</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/create.html')

    def testLinkReqquired(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>link<ul class="errorlist"><li>This field is required.</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/create.html')

    def testInvalidLink(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title',
            'link': 'invalid_link'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>link<ul class="errorlist"><li>Enter a valid URL.</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/create.html')

    def testPublishedDateReqquired(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title',
            'link': 'http://abc.com'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>published_date<ul class="errorlist"><li>This field is required.</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/create.html')

    def testPublishedDateInvalidFormat(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title',
            'link': 'http://abc.com',
            'published_date': 'Invalid format date'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>published_date<ul class="errorlist"><li>Enter a valid date/time.</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/create.html')

    def testSaveItemError(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title',
            'link': 'http://abc.com',
            'published_date': '2020-01-01 10:00:00'
        }

        with mock.patch('brief_app.forms.CreateItemForm.save') as mockMethod:
            mockMethod.side_effect = Exception('test error')

            response = UtilTest.callPost(self, self.url, params)

            messages = list(response.context['messages'])
            self.assertEqual(len(messages), 1)
            self.assertIn('Occurred system error. Please try again.', str(messages[0]))
            self.assertTemplateUsed(response, 'items/create.html')

    def testSaveItemSuccess(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title',
            'link': 'http://abc.com',
            'published_date': '2020-01-01 10:00:00'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('Created item successfully.', str(messages[0]))
        self.assertRedirects(response, reverse('itemList'))

        # Assert inserted data
        expectedItem = RssFeedItem.objects.last()
        UtilTest.assertItem(self, params, expectedItem)
