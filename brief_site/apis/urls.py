from django.urls import path
from .views import AnalysisRssFeedItem

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('feeds/analysisRssFeedItem', AnalysisRssFeedItem.as_view(), name='analysisRssFeedItem'),
]
