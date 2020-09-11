from datetime import datetime

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
