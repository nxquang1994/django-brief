from django.test import TestCase
from django.urls import reverse
from rest_framework.views import status
from apis.models import RssFeedItem
from apis.tests.common.utils import UtilTest
from apis.common import Utils

# Create your tests here.
class RssFeedItemAPITest(TestCase):

    def setUp(self) -> None:
        self.url = reverse('analysisRssFeedItem')

    def testUrlsRequired(self):
        params = None

        responseJson = UtilTest.callAPIPost(self, self.url, params, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(responseJson, Utils.createErrorResponse('Urls is required'))

    def testErrorException(self):
        params = {
            'urls': 'https://'
        }

        responseJson = UtilTest.callAPIPost(self, self.url, params, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(responseJson, Utils.createErrorResponse('Error system'))

    def testEmptyFeedItem(self):
        params = {
            'urls': ','
        }

        responseJson = UtilTest.callAPIPost(self, self.url, params, status.HTTP_200_OK)
        self.assertEqual(len(responseJson['returnedValue']['itemList']), 0)
        self.assertEqual(RssFeedItem.objects.count(), 0)

    def testOneUrlFeedItem(self):
        params = {
            'urls': 'http://www.smartbrief.com/servlet/rss?b=ASCD'
        }

        responseJson = UtilTest.callAPIPost(self, self.url, params, status.HTTP_200_OK)
        self.assertEqual(len(responseJson['returnedValue']['itemList']), RssFeedItem.objects.count())

    def testDuplicateUrlFeedItem(self):
        urls = 'http://www.smartbrief.com/servlet/rss?b=ASCD'
        urls += ',http://www.smartbrief.com/servlet/rss?b=ASCD'

        params = {
            'urls': urls
        }

        responseJson = UtilTest.callAPIPost(self, self.url, params, status.HTTP_200_OK)
        self.assertEqual(len(responseJson['returnedValue']['itemList']), RssFeedItem.objects.count())

    def testListUrlWithHavingEmptyValue(self):
        params = {
            'urls': ',http://www.smartbrief.com/servlet/rss?b=ASCD'
        }

        responseJson = UtilTest.callAPIPost(self, self.url, params, status.HTTP_200_OK)
        self.assertEqual(len(responseJson['returnedValue']['itemList']), RssFeedItem.objects.count())

    def testMultiplesUrlFeedItem(self):
        params = {
            'urls': 'http://rss.cnn.com/rss/edition_motorsport.rss,http://www.smartbrief.com/servlet/rss?b=ASCD'
        }

        responseJson = UtilTest.callAPIPost(self, self.url, params, status.HTTP_200_OK)
        self.assertEqual(len(responseJson['returnedValue']['itemList']), RssFeedItem.objects.count())

    def testItemWithEmptyCategory(self):
        params = {
            'urls': 'http://rss.cnn.com/rss/edition_travel.rss'
        }

        responseJson = UtilTest.callAPIPost(self, self.url, params, status.HTTP_200_OK)
        self.assertEqual(len(responseJson['returnedValue']['itemList']), RssFeedItem.objects.count())

    def testItemWithEmptyPublishedDate(self):
        params = {
            'urls': 'http://www.reddit.com/r/python/.rss'
        }

        responseJson = UtilTest.callAPIPost(self, self.url, params, status.HTTP_200_OK)
        self.assertEqual(len(responseJson['returnedValue']['itemList']), RssFeedItem.objects.count())
