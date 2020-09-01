from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
import feedparser
import ssl
from apis.models import RssFeedItem
from apis.logs.log import logger
from apis.common import Utils
from time import mktime
from datetime import datetime
import pytz

class AnalysisRssFeedItem(generics.ListCreateAPIView):
    """
    POST feeds/analysisRssFeedItem
    """

    def post(self, request):

        # Return response
        returnedValue = None
        statusCode = status.HTTP_200_OK

        try:
            urls = request.data.get('urls', '')

            # Validate urls required
            if not urls:
                statusCode = status.HTTP_400_BAD_REQUEST
                returnedValue = Utils.createErrorResponse('Urls is required')
                raise

            # Split by comma
            urls = urls.split(',')
            # Remove unique value
            urls = set(urls)

            # Avoid error SSL CERTIFICATE_VERIFY_FAILED
            if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context

            # Use to insert item
            insertItemList = []
            itemListResponse = []
            for url in urls:
                # In case of empty url, skip
                if not url:
                    continue

                convertResult = feedparser.parse(url)

                # Check error parse
                if convertResult.bozo == 1:
                    raise convertResult.bozo_exception

                entries = convertResult.entries

                for item in entries:

                    # Get categories
                    # Init Null to return response
                    categories = None
                    if 'tags' in item:
                        categories = ''
                        tags = item.tags
                        for tag in tags:
                            if categories:
                                categories += ','

                            categories += tag.term

                    # Get published_date
                    publishedDate = None
                    if 'published_parsed' in item:
                        publishedDate = datetime.fromtimestamp(mktime(item.published_parsed), tz=pytz.utc)

                    insertItemList.append(RssFeedItem(
                        category=categories,
                        title=item.title,
                        link=item.link,
                        published_date=publishedDate
                    ))

                    # Convert format date
                    if publishedDate:
                        publishedDate = publishedDate.strftime('%Y-%m-%d %H:%M:%S')

                    itemListResponse.append({
                        'category': categories,
                        'title': item.title,
                        'link': item.link,
                        'publishedDate': publishedDate
                    })

            # Insert item every 1000 records
            if insertItemList:
                RssFeedItem.objects.bulk_create(insertItemList, batch_size=1000)
            
            # Return success response
            returnedValue = Utils.createSuccessResponse({
                'itemList': itemListResponse
            })

        except Exception as e:
            if not returnedValue:
                logger.error('Exception：%s, %s' % (type(e), e.args))

                statusCode = status.HTTP_500_INTERNAL_SERVER_ERROR
                returnedValue = Utils.createErrorResponse('Error system')
        finally:
            if statusCode == status.HTTP_200_OK:
                logger.info('request: %s, response: %s' % (request.data, returnedValue))
            elif statusCode == status.HTTP_500_INTERNAL_SERVER_ERROR:
                # System Error
                logger.error('request: %s, response: %s' % (request.data, returnedValue))
            else:
                logger.warning('request: %s, response: %s' % (request.data, returnedValue))

        return Response(returnedValue, status=statusCode)
