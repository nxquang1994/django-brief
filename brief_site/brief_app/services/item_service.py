from common_app.models import RssFeedItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

class ItemService():

    def searchItemWithPagination(category, page, perPage):
        try:
            # Get object items to paginate
            if category:
                items = RssFeedItem.objects.filter(category__contains=category)
            else:
                items = RssFeedItem.objects.all()
            # Get specified item and order by id desc
            items = items.only('category', 'title', 'link', 'published_date').order_by('-id')
            # Pagination
            paginator = Paginator(items, perPage)
            paginationItems = paginator.page(page)

        except PageNotAnInteger:
            # In case of page not integer, get page 1
            paginationItems = paginator.page(1)

        except EmptyPage:
            # In case of empty page, get last page
            paginationItems = paginator.page(paginator.num_pages)

        return paginationItems

    def getItemById(itemId):
        return get_object_or_404(RssFeedItem, pk=itemId)

    def deleteItem(itemId):
        RssFeedItem.objects.get(pk=itemId).delete()
