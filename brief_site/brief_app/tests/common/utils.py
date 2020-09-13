from datetime import datetime
from common_app.models import RssFeedItem
import pytz

class UtilTest():
    """
    Common call post
    """
    def callPost(testModule, url, params=None, statusCode = 200):
        response = {}

        try:
            response = testModule.client.post(url, data=params, follow=True)
        except Exception as e:
            # Use for debug error
            print(e)
        finally:
            testModule.assertEqual(response.status_code, statusCode)

        return response

    """
    Common call get
    """
    def callGet(testModule, url, params = None, statusCode = 200):
        response = {}

        try:
            response = testModule.client.get(url, params)
        except Exception as e:
            # Use for debug error
            print(e)
        finally:
            testModule.assertEqual(response.status_code, statusCode)

        return response

    """
    Common call put
    """
    def callPut(testModule, url, params, statusCode = 200):
        response = {}

        try:
            response = testModule.client.put(url, data=params)
        except Exception as e:
            # Use for debug error
            print(e)
        finally:
            testModule.assertEqual(response.status_code, statusCode)

        return response

    """
    Assert item
    """
    def assertItem(testModule, actualItem, expectedItem, formatDate=None):
        actualPublishedDate = actualItem['published_date']
        expectedPublishedDate = expectedItem.published_date
        if formatDate:
            actualPublishedDate = datetime.strftime(actualPublishedDate, formatDate)
            expectedPublishedDate = datetime.strftime(expectedPublishedDate, formatDate)
        else:
            expectedPublishedDate = datetime.strftime(expectedPublishedDate, '%Y-%m-%d %H:%M:%S')

        testModule.assertEqual(expectedItem.title, actualItem['title'])
        testModule.assertEqual(expectedItem.category, actualItem['category'])
        testModule.assertEqual(expectedItem.link, actualItem['link'])
        testModule.assertEqual(expectedPublishedDate, actualPublishedDate)

    """
    Create data item test
    """
    def createDataItemTest():
        item = RssFeedItem(
            category='unit_test_category',
            title='unit_test_title',
            link='http://abc.com',
            published_date=datetime.now(tz=pytz.utc)
        )

        item.save()

        return item

    """
    Assert item list
    """
    def assertItemList(testModule, dataList, actualItems, expectedTotalPage, expectedCurrentPage):
        # Assert pagination
        testModule.assertEqual(dataList.paginator.num_pages, expectedTotalPage)
        testModule.assertEqual(dataList.number, expectedCurrentPage)
        # Assert data
        count = 0
        for expectedItem in dataList:
            actualItem = actualItems[count]
            UtilTest.assertItem(testModule, actualItem, expectedItem, '%Y-%m-%d %H:%M:%S')
