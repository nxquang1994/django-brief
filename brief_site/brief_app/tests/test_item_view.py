from django.test import TestCase
from django.urls import reverse
from unittest import mock
from brief_app.tests.common.utils import UtilTest
from common_app.models import RssFeedItem

"""
[Test list item]
"""
class ListItemTest(TestCase):

    def setUp(self) -> None:
        self.url = reverse('listItem')

    def testInvalidHttpMethod(self):
        UtilTest.callPost(self, self.url, None, 405)

    def testExceptionError(self):
        with mock.patch('common_app.models.RssFeedItem.objects.all') as mockMethod:
            mockMethod.side_effect = Exception('test error')

            UtilTest.callGet(self, self.url, None, 500)

    def testPageNotInteger(self):
        # Prepare data
        for i in range(2):
            UtilTest.createDataItemTest()

        params = {
            'page': 'invalidPage'
        }

        response = UtilTest.callGet(self, self.url, params)
        self.assertTemplateUsed(response, 'items/index.html')
        # Assert items
        actualItems = RssFeedItem.objects.all().order_by('-id')
        actualItems = actualItems.values()
        UtilTest.assertItemList(self, response.context['dataList'], actualItems, 1, 1)

    def testEmptyPage(self):
        # Prepare data
        for i in range(2):
            UtilTest.createDataItemTest()

        params = {
            'page': 2
        }

        response = UtilTest.callGet(self, self.url, params)
        self.assertTemplateUsed(response, 'items/index.html')
        # Assert items
        actualItems = RssFeedItem.objects.all().order_by('-id')
        actualItems = actualItems.values()
        UtilTest.assertItemList(self, response.context['dataList'], actualItems, 1, 1)

    def testMultiplesPage(self):
        # Prepare data
        for i in range(2):
            UtilTest.createDataItemTest()

        params = {
            'page': 1,
            'perPage': 1
        }

        response = UtilTest.callGet(self, self.url, params)
        self.assertTemplateUsed(response, 'items/index.html')
        # Assert items
        actualItems = RssFeedItem.objects.all().order_by('-id')[:1]
        actualItems = actualItems.values()
        # actualItems = actualItems.values()
        UtilTest.assertItemList(self, response.context['dataList'], actualItems, 2, 1)

    def testMultiplesPage(self):
        # Prepare data
        for i in range(2):
            UtilTest.createDataItemTest()

        params = {
            'page': 1,
            'perPage': 1
        }

        response = UtilTest.callGet(self, self.url, params)
        self.assertTemplateUsed(response, 'items/index.html')
        # Assert items
        actualItems = RssFeedItem.objects.all().order_by('-id')[:1]
        actualItems = actualItems.values()
        UtilTest.assertItemList(self, response.context['dataList'], actualItems, 2, 1)

    def testPageAndPerPageEmpty(self):
        # Prepare data
        for i in range(10):
            UtilTest.createDataItemTest()

        response = UtilTest.callGet(self, self.url)
        self.assertTemplateUsed(response, 'items/index.html')
        # Assert items
        actualItems = RssFeedItem.objects.all().order_by('-id')
        actualItems = actualItems.values()
        UtilTest.assertItemList(self, response.context['dataList'], actualItems, 1, 1)

    def testSpecifyPageWithoutOne(self):
        # Prepare data
        for i in range(2):
            UtilTest.createDataItemTest()

        params = {
            'page': 2,
            'perPage': 1
        }

        response = UtilTest.callGet(self, self.url, params)
        self.assertTemplateUsed(response, 'items/index.html')
        # Assert items
        actualItems = RssFeedItem.objects.all().order_by('id')[:1]
        actualItems = actualItems.values()
        UtilTest.assertItemList(self, response.context['dataList'], actualItems, 2, 2)

    def testSearchCategoryWithEmptyRecord(self):
        # Prepare data
        for i in range(2):
            UtilTest.createDataItemTest()

        params = {
            'category': 'NotFound'
        }

        response = UtilTest.callGet(self, self.url, params)
        self.assertTemplateUsed(response, 'items/index.html')
        UtilTest.assertItemList(self, response.context['dataList'], [], 1, 1)

    def testSearchCategoryWithHavingRecord(self):
        # Prepare data
        for i in range(2):
            UtilTest.createDataItemTest()

        params = {
            'category': 'u'
        }

        response = UtilTest.callGet(self, self.url, params)
        self.assertTemplateUsed(response, 'items/index.html')
        # Assert items
        actualItems = RssFeedItem.objects.all().order_by('id')[:1]
        actualItems = actualItems.values()
        UtilTest.assertItemList(self, response.context['dataList'], actualItems, 1, 1)

"""
[Test show item]
"""
class ShowItemTest(TestCase):

    def setUp(self) -> None:
        self.item = UtilTest.createDataItemTest()
        self.url = reverse('showItem', args=[self.item.id])

    def testInvalidHttpMethod(self):
        UtilTest.callPut(self, self.url, None, 405)

    def testItemNotFound(self):
        UtilTest.callGet(self, reverse('showItem', args=[9999999]), None, 404)

    def testExceptionError(self):
        with mock.patch('brief_app.services.ItemService.getItemById') as mockMethod:
            mockMethod.side_effect = Exception('test error')

            UtilTest.callGet(self, self.url, None, 500)

    def testShowItem(self):
        response = UtilTest.callGet(self, self.url)
        self.assertTemplateUsed(response, 'items/show.html')

"""
[Test create item]
"""
class CreateItemTest(TestCase):

    def setUp(self) -> None:
        self.url = reverse('createItem')

    def testInvalidHttpMethod(self):
        UtilTest.callPut(self, self.url, None, 405)

    def testShowCreateItem(self):
        response = UtilTest.callGet(self, self.url)
        self.assertTemplateUsed(response, 'items/create.html')

    def testCategoryReqquired(self):
        response = UtilTest.callPost(self, self.url)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual('Category is required.', str(messages[0]))
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
        self.assertEqual('Category must be less than or equal to 50 characters.', str(messages[0]))
        self.assertTemplateUsed(response, 'items/create.html')

    def testTitleReqquired(self):
        params = {
            'category': 'unit_test_category'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual('Title is required.', str(messages[0]))
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
        self.assertEqual('Title must be less than or equal to 255 characters.', str(messages[0]))
        self.assertTemplateUsed(response, 'items/create.html')

    def testLinkReqquired(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual('Link is required.', str(messages[0]))
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
        self.assertEqual('Invalid link format.', str(messages[0]))
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
        self.assertEqual('Published date is required.', str(messages[0]))
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
        self.assertEqual('Invalid published date format.', str(messages[0]))
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

            UtilTest.callPost(self, self.url, params, 500)

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

    def testInvalidHttpMethod(self):
        UtilTest.callPut(self, self.url, None, 405)

    def testItemNotFound(self):
        UtilTest.callGet(self, reverse('editItem', args=[9999999]), None, 404)

    def testShowEditItem(self):
        response = UtilTest.callGet(self, self.url)
        self.assertTemplateUsed(response, 'items/edit.html')

    def testCategoryReqquired(self):
        response = UtilTest.callPost(self, self.url)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual('Category is required.', str(messages[0]))
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
        self.assertEqual('Category must be less than or equal to 50 characters.', str(messages[0]))
        self.assertTemplateUsed(response, 'items/edit.html')

    def testTitleReqquired(self):
        params = {
            'category': 'unit_test_category'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual('Title is required.', str(messages[0]))
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
        self.assertEqual('Title must be less than or equal to 255 characters.', str(messages[0]))
        self.assertTemplateUsed(response, 'items/edit.html')

    def testLinkReqquired(self):
        params = {
            'category': 'unit_test_category',
            'title': 'unit_test_title'
        }

        response = UtilTest.callPost(self, self.url, params)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual('Link is required.', str(messages[0]))
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
        self.assertEqual('Invalid link format.', str(messages[0]))
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
        self.assertEqual('Published date is required.', str(messages[0]))
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
        self.assertEqual('Invalid published date format.', str(messages[0]))
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

            UtilTest.callPost(self, self.url, params, 500)

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
        self.assertIn('Edited item successfully', str(messages[0]))
        self.assertRedirects(response, reverse('listItem'))

        # Assert inserted data
        expectedItem = RssFeedItem.objects.get(pk=self.item.id)
        UtilTest.assertItem(self, params, expectedItem)

"""
[Test delete item]
"""
class DeleteItemTest(TestCase):
    def setUp(self) -> None:
        self.item = UtilTest.createDataItemTest()
        self.url = reverse('deleteItem', args=[self.item.id])

    def testInvalidHttpMethod(self):
        UtilTest.callPut(self, self.url, None, 405)

    def testItemNotFound(self):
        UtilTest.callPost(self, reverse('deleteItem', args=[9999999]), None, 404)

    def testDeleteItemError(self):
        with mock.patch('brief_app.services.ItemService.deleteItem') as mockMethod:
            mockMethod.side_effect = Exception('test error')

            UtilTest.callPost(self, self.url, None, 500)

    def testDeleteItemSuccess(self):
        response = UtilTest.callPost(self, self.url)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('Deleted item successfully', str(messages[0]))
        self.assertRedirects(response, reverse('listItem'))

        # Assert inserted data
        countItem = RssFeedItem.objects.filter(id=self.item.id).count()
        self.assertEqual(countItem, 0)
