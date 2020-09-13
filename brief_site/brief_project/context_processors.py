from django.conf import settings

def globalSettings(request):
    # Return any necessary values
    return {
        'LANGUAGE': settings.LANGUAGE,
        'APP_NAME': settings.APP_NAME,
        'PER_PAGE': settings.PER_PAGE,
    }
