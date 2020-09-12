from django.urls import path, re_path
from brief_app import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.home, name='listItem'),
    path('items/create', views.createItem, name='createItem'),
    re_path('items/(?P<itemId>[0-9]+)/edit/$', views.editItem, name='editItem'),
]
