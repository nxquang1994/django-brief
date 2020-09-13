from django.shortcuts import render, resolve_url, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, HttpResponseServerError
from brief_app.forms import ItemForm
from common_app.logs.log import logger
from common_app.models import RssFeedItem

def flashMessage(form):
    listErrors = []
    for field, errors in form.errors.items:
        for currentErr in errors:
            errorText = field + ' ' + currentErr
            listErrors.append(errorText)
            pass
        pass
    return listErrors

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

                errorList = flashMessage(createItemForm)
                messages.error(request, errorList)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                # messages.error(request, errors)
        else:
            createItemForm = ItemForm()

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

                # messages.error(request, errors)
                errorList = flashMessage(editItemForm)
                messages.error(request, errorList)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            editItemForm = ItemForm(instance=item)

        return render(request, 'items/edit.html', {'form': editItemForm, 'editItem': item})

    except Http404:
        logger.warning('Item not found target_item_id[%s]' %  (itemId))
        # In case of item do not exists
        raise Http404
    except Exception as e:
        logger.error('Exception：%s, %s' % (type(e), e.args))
        # In case of abnormal error, raise error page 500
        return HttpResponseServerError(str(e))
