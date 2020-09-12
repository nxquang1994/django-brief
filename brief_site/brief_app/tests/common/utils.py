from datetime import datetime
from common_app.models import RssFeedItem
import pytz

class UtilTest():
    """
    Common call post
    """
    def callPost(testModule, url, params, statusCode = 200):
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
    Assert item
    """
    def assertItem(testModule, actualItem, expectedItem):
        testModule.assertEqual(expectedItem.title, actualItem['title'])
        testModule.assertEqual(expectedItem.category, actualItem['category'])
        testModule.assertEqual(expectedItem.link, actualItem['link'])
        testModule.assertEqual(
            datetime.strftime(expectedItem.published_date, '%Y-%m-%d %H:%M:%S'),
            actualItem['published_date']
        )

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
