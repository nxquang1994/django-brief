from django.conf import settings

def global_settings(request):
    # Return any necessary values
    return {
        'LANGUAGE': settings.LANGUAGE,
        'APP_NAME': settings.APP_NAME
    }
