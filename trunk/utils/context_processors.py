from django.conf import settings

def context(request):
    return {"MEDIA_URL": settings.MEDIA_URL, }
