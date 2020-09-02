from django.urls import path

from . import views

app_name = 'brief_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax_data', views.response_site_data, name='site_data')
]