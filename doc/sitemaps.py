from django.conf import settings
from michilu.helpdoc.util import HelpdocSitemap

class DocJaSitemap(HelpdocSitemap):
    info_dict = dict(
        changefreq = "weekly",
        priority = 0.7,
    )
    target_dir = settings.CUSTOM_DOC_JA_DIR
    location = settings.SERVER_DOMAIN + "/django/doc-ja/%s/"

doc_sitemaps = {
    "doc-ja": DocJaSitemap(),
}
