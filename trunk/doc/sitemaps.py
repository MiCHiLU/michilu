from django.conf import settings
import os.path
from datetime import datetime

class DocJaSitemap(object):
    base_dict = {
        "changefreq":   "weekly",
        "priority":     0.7 ,
    }
    target_dir = settings.CUSTOM_DOC_JA_DIR
    location = settings.SERVER_DOMAIN + "/django/doc-ja/%s/"
    result = []

    def get_urls(self):
        target_files = os.listdir(self.target_dir)
        for target_file in target_files:
            target_path = self.target_dir + target_file
            if not os.path.isfile(target_path):
                continue
            info_dict = self.base_dict.copy()
            info_dict.update({
                "lastmod": datetime.fromtimestamp(os.path.getmtime(target_path)),
                "location": self.location % target_file.split(".")[0],
            })
            self.result.append(info_dict)
        return self.result

doc_sitemaps = {
    "doc-ja": DocJaSitemap(),
}
