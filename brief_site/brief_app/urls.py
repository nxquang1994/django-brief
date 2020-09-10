from django.urls import include, path
from brief_app import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# app_name = 'brief_app'    
urlpatterns = [
    path('', views.home, name='home'),
    path('ajax_data', views.response_item_data, name='site_data'),
    path('index', views.index, name='index'),
    path('<int:item_id>/detail', views.observe_item, name='observe_item'),
    path('create', views.create_item, name='create_item'),
    path('<int:item_id>/edit', views.edit_item, name='edit_item'),
]
