class UtilTest():
    """
    Common call api post
    """
    def callAPIPost(testModule, url, params, statusCode):
        response = {}

        try:
            response = testModule.client.post(url, data=params, format='json')
        except Exception as e:
            # Use for debug error
            print(e)
        finally:
            testModule.assertEqual(response.status_code, statusCode)

        return response.json()
