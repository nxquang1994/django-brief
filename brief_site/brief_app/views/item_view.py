from django.shortcuts import render, resolve_url, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponseServerError
from brief_app.forms import ItemForm
from common_app.logs.log import logger
from common_app.models import RssFeedItem

def createItem(request):
    try:
        if request.method == 'POST':
            createItemForm = ItemForm(request.POST)

            logger.info('request[%s]' %  (request.POST))

            # Validation request param
            if createItemForm.is_valid():
                # Save item
                insertItem = createItemForm.save()

                logger.info('Create item successfully target_item_id[%s]' %  (insertItem.id))

                messages.success(request, 'Created item successfully id[%s].' % (insertItem.id))

                return HttpResponseRedirect(resolve_url('listItem'))
            else:
                errors = createItemForm.errors

                logger.warning('Request Param Validation Error [%s]' %  (errors))

                messages.error(request, 'There are errors in typing form')

                request.session['old-form-data'] = request.POST
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            # Check session & Check Update form data 
            createItemForm = ItemForm()
            if request.session.has_key('old-form-data'):
                createItemForm = ItemForm(request.session['old-form-data'])
                request.session.flush()
                pass

        return render(request, 'items/create.html', {'form': createItemForm})

    except Exception as e:
        logger.error('Exception：%s, %s' % (type(e), e.args))
        # In case of abnormal error, raise error page 500
        return HttpResponseServerError(str(e))

def editItem(request, itemId):
    try:
        item = get_object_or_404(RssFeedItem, pk=itemId)

        if request.method == 'POST':
            editItemForm = ItemForm(request.POST, instance=item)

            logger.info('request[%s]' %  (request.POST))

            # Validation request param
            if editItemForm.is_valid():
                # Save item
                editItem = editItemForm.save()

                logger.info('Edit item successfully target_item_id[%s]' %  (editItem.id))

                messages.success(request, 'Edit item successfully id[%s].' % (editItem.id))

                return HttpResponseRedirect(resolve_url('listItem'))
            else:
                errors = editItemForm.errors

                logger.warning('Request Param Validation Error [%s]' %  (errors))

                messages.error(request, 'There are errors in typing form')
                
                request.session['old-form-data'] = request.POST
        else:
            editItemForm = ItemForm(instance=item)
            # Check session & Check Update form data 
            if request.session.has_key('old-form-data'):
                editItemForm = ItemForm(request.session['old-form-data'])
                request.session.flush()
                pass

        return render(request, 'items/edit.html', {'form': editItemForm, 'editItem': item})

    except Http404:
        logger.warning('Item not found target_item_id[%s]' %  (itemId))
        # In case of item do not exists
        raise Http404
    except Exception as e:
        logger.error('Exception：%s, %s' % (type(e), e.args))
        # In case of abnormal error, raise error page 500
        return HttpResponseServerError(str(e))
