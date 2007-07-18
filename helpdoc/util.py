import os.path
from datetime import datetime

class HelpdocSitemap(object):
    info_dict = dict(
        changefreq = "weekly",
        priority = 0.6,
    )
    target_dir = None
    location = None

    def get_urls(self):
        result = []
        sep = "."
        target_files = os.listdir(self.target_dir)
        for target_file in target_files:
            target_path = self.target_dir + target_file
            if not os.path.isfile(target_path):
                continue
            info_dict = self.info_dict.copy()
            info_dict.update({
                "lastmod": datetime.fromtimestamp(os.path.getmtime(target_path)),
                "location": self.location % sep.join(target_file.split(sep)[:-1]),
            })
            result.append(info_dict)
        return result
