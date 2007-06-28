from django.conf import settings

def helpdoc(request):
    if hasattr(settings, "HELPDOC_BASE_URL"):
        base_url = settings.HELPDOC_BASE_URL
    else:
        base_url = "/helpdoc/"
    return dict(
        helpdoc_base_url = base_url,
    )
