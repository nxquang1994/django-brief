from django.shortcuts import render, resolve_url, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from brief_app.forms import ItemForm
from common_app.logs.log import logger

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

                messages.success(request, 'Created item successfully.')
                # TODO: Return item list screen
                return HttpResponseRedirect(resolve_url('itemList'))
            else:
                errors = createItemForm.errors

                logger.warning('Request Param Validation Error [%s]' %  (errors))

                messages.error(request, errors)
        else:
            createItemForm = ItemForm()

    except Exception as e:
        logger.error('Exception：%s, %s' % (type(e), e.args))
        # Display error msg on the screen
        messages.error(request, 'Occurred system error. Please try again.')

    return render(request, 'items/create.html', {'form': createItemForm})
