from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from apis.models import RssFeedItem
from django.urls import reverse
from brief_app.forms import RssFeedItemForm
from brief_app.services import RssQuery
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def response_item_data(request):
    all_objects = RssFeedItem.objects.all().values()
    data = { 'data': list(all_objects) }
    return JsonResponse(data)

def observe_item(request, item_id):
    item = RssFeedItem.objects.get(pk=item_id)
    context = { 'item': item }
    return render(request, 'detail.html', context)


def create_item(request):
    if request.method == 'GET':
        form = RssFeedItemForm(initial={})
        return render(request, 'create_item.html', {'form' : form})
    form = RssFeedItemForm(request.POST)
    if form.is_valid():
        is_success, new_item_id = RssQuery.create_new_rss(request.POST)
        if is_success:
            messages.success(request, 'Create item successfully')
            return HttpResponseRedirect(reverse('observe_item', args=(new_item_id,)))
        messages.error('There are errors when create item')
        return render(request, 'create_item.html', {'form' : form})
    messages.error(request, 'There are errors when create item.')
    return render(request, 'create_item.html', {'form' : form})


def edit_item(request, item_id):
    if request.method == 'GET':
        item = get_object_or_404(RssFeedItem, pk=item_id)
        form = RssFeedItemForm(initial={
            'category' : item.category,
            'title' : item.title,
            'link' : item.link,
            'published_date' : item.published_date,
        })
        return render(request, 'edit.html', {'form' : form, 'item_id': item_id})
    form = RssFeedItemForm(request.POST)
    if form.is_valid():
        is_edit_success = RssQuery.edit_rss_item(item_id, request.POST)
        if is_edit_success:
            messages.success(request, 'Update item successfully')
            return HttpResponseRedirect(reverse('observe_item', args=(item_id,)))
    messages.error(request, 'There are errors when edit item.')
    return render(request, 'edit.html', {'form' : form, 'item_id': item_id})
    


