from django import template

register = template.Library()

@register.simple_tag
def queryTransform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)

    return updated.urlencode()

@register.simple_tag
def setVar(val=None):
    return val

@register.simple_tag
def getParamQuery(request, key, defaultValue=''):
    copyRequest = request.GET.copy()

    # Avoid exception in case of no key
    return copyRequest.get(key, defaultValue)
