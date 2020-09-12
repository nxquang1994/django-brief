from django.test import TestCase
from django.urls import reverse
from unittest import mock
from rest_framework.views import status
from brief_app.tests.common.utils import UtilTest
from common_app.models import RssFeedItem

"""
[Test create item]
"""
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

    def testCreateItemError(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title',
            'link': 'http://abc.com',
            'published_date': '2020-01-01 10:00:00'
        }

        with mock.patch('brief_app.forms.ItemForm.save') as mockMethod:
            mockMethod.side_effect = Exception('test error')

            response = UtilTest.callPost(self, self.url, params, 500)

    def testCreateItemSuccess(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title',
            'link': 'http://abc.com',
            'published_date': '2020-01-01 10:00:00'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('Created item successfully', str(messages[0]))
        self.assertRedirects(response, reverse('listItem'))

        # Assert inserted data
        expectedItem = RssFeedItem.objects.last()
        UtilTest.assertItem(self, params, expectedItem)

"""
[Test edit item]
"""
class EditItemTest(TestCase):

    def setUp(self) -> None:
        self.item = UtilTest.createDataItemTest()
        self.url = reverse('editItem', args=[self.item.id])

    def testItemNotFound(self):
        UtilTest.callGet(self, reverse('editItem', args=[9999999]), None, 404)

    def testShowEditItem(self):
        response = UtilTest.callGet(self, self.url)
        self.assertTemplateUsed(response, 'items/edit.html')

    def testCategoryReqquired(self):
        params = None

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>category<ul class="errorlist"><li>This field is required.</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/edit.html')

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
        self.assertTemplateUsed(response, 'items/edit.html')

    def testTitleReqquired(self):
        params = {
            'category': 'unit_test_category'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>title<ul class="errorlist"><li>This field is required.</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/edit.html')

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
        self.assertTemplateUsed(response, 'items/edit.html')

    def testLinkReqquired(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('<ul class="errorlist"><li>link<ul class="errorlist"><li>This field is required.</li></ul>', str(messages[0]))
        self.assertTemplateUsed(response, 'items/edit.html')

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
        self.assertTemplateUsed(response, 'items/edit.html')

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
        self.assertTemplateUsed(response, 'items/edit.html')

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
        self.assertTemplateUsed(response, 'items/edit.html')

    def testEditItemError(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title',
            'link': 'http://abc.com',
            'published_date': '2020-01-01 10:00:00'
        }

        with mock.patch('brief_app.forms.ItemForm.save') as mockMethod:
            mockMethod.side_effect = Exception('test error')

            response = UtilTest.callPost(self, self.url, params, 500)

    def testEditItemSuccess(self):
        params = {
            'category': 'update_unit_test_category',
            'title': 'update_unit_test_title',
            'link': 'http://abc.com',
            'published_date': '2020-01-01 10:00:00'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('Edit item successfully', str(messages[0]))
        self.assertRedirects(response, reverse('listItem'))

        # Assert inserted data
        expectedItem = RssFeedItem.objects.get(pk=self.item.id)
        UtilTest.assertItem(self, params, expectedItem)
