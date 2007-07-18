from django.conf import settings
from michilu.helpdoc.util import HelpdocSitemap


class DocJaSitemap(HelpdocSitemap):
    info_dict = dict(
        changefreq = "weekly",
        priority = 0.7,
    )
    target_dir = settings.CUSTOM_DOC_JA_DIR % "trunk/"
    location = settings.SERVER_DOMAIN + "/django/doc-ja/%s/"


class DocJa096Sitemap(HelpdocSitemap):
    info_dict = dict(
        changefreq = "never",
        priority = 0.8,
    )
    target_dir = settings.CUSTOM_DOC_JA_DIR % "branches/docs_0.96/"
    location = settings.SERVER_DOMAIN + "/django/doc-ja-0.96/%s/"


doc_sitemaps = {
    "doc-ja": DocJaSitemap(),
    "doc-ja-0.96": DocJa096Sitemap(),
}
