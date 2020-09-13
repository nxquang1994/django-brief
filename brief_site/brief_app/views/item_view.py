from django.shortcuts import render, resolve_url, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponseServerError
from brief_app.forms import ItemForm
from common_app.logs.log import logger
from common_app.models import RssFeedItem
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

@require_http_methods(['GET'])
def listItem(request):
    try:
        # Request param
        page = request.GET.get('page', 1)
        perPage = request.GET.get('perPage', settings.PER_PAGE)
        category = request.GET.get('category', '')
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

    except Exception as e:
        logger.error('Exception：%s, %s' % (type(e), e.args))
        # In case of abnormal error, raise error page 500
        return HttpResponseServerError(str(e))

    return render(request, 'items/index.html', {'dataList': paginationItems})

@require_http_methods(['GET', 'POST'])
def createItem(request):
    try:
        if request.method == 'POST':
            createItemForm = ItemForm(request.POST)

            logger.info('request[%s]' % request.POST)

            # Validation request param
            if createItemForm.is_valid():
                # Save item
                insertItem = createItemForm.save()

                logger.info('Created item successfully target_item_id[%s].' % insertItem.id)

                messages.success(request, 'Created item successfully item_id[%s].' % insertItem.id)

                return HttpResponseRedirect(resolve_url('listItem'))
            else:
                errors = createItemForm.errors

                logger.warning('Request Param Validation Error [%s]' % errors)

                messages.error(request, errors)
        else:
            createItemForm = ItemForm()

        return render(request, 'items/create.html', {'form': createItemForm})

    except Exception as e:
        logger.error('Exception：%s, %s' % (type(e), e.args))
        # In case of abnormal error, raise error page 500
        return HttpResponseServerError(str(e))

@require_http_methods(['GET', 'POST'])
def editItem(request, itemId):
    try:
        item = get_object_or_404(RssFeedItem, pk=itemId)

        if request.method == 'POST':
            editItemForm = ItemForm(request.POST, instance=item)

            logger.info('request[%s]' % request.POST)

            # Validation request param
            if editItemForm.is_valid():
                # Save item
                editItem = editItemForm.save()

                logger.info('Edited item successfully target_item_id[%s].' %  editItem.id)

                messages.success(request, 'Edited item successfully item_id[%s].' % editItem.id)

                return HttpResponseRedirect(resolve_url('listItem'))
            else:
                errors = editItemForm.errors

                logger.warning('Request Param Validation Error [%s]' % errors)

                messages.error(request, errors)
        else:
            editItemForm = ItemForm(instance=item)

        return render(request, 'items/edit.html', {'form': editItemForm, 'editItem': item})

    except Http404:
        logger.warning('Item not found target_item_id[%s]' % itemId)
        # In case of item do not exists
        raise Http404

    except Exception as e:
        logger.error('Exception：%s, %s' % (type(e), e.args))
        # In case of abnormal error, raise error page 500
        return HttpResponseServerError(str(e))

@require_http_methods(['POST'])
def deleteItem(request, itemId):
    try:
        item = get_object_or_404(RssFeedItem, pk=itemId)

        item.delete()

        logger.info('Deleted item successfully target_item_id[%s].' % itemId)

        messages.success(request, 'Deleted item successfully item_id[%s].' % itemId)

        return HttpResponseRedirect(resolve_url('listItem'))

    except Http404:
        logger.warning('Item not found target_item_id[%s]' % itemId)
        # In case of item do not exists
        raise Http404

    except Exception as e:
        logger.error('Exception：%s, %s' % (type(e), e.args))
        # In case of abnormal error, raise error page 500
        return HttpResponseServerError(str(e))
