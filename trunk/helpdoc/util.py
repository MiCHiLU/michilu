import os.path
from datetime import datetime

markup_extensions = ("txt","rst","markdown","textile","html")

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


def get_timestamp(target, extension=None, utc=False, raw=False):
    if utc:
        fromtimestamp = datetime.utcfromtimestamp
    else:
        fromtimestamp = datetime.fromtimestamp
    if raw:
        timestamp = lambda x: os.path.getmtime(x)
    else:
        timestamp = lambda x: fromtimestamp(os.path.getmtime(x))
    if not os.path.isdir(target):
        return timestamp(target)
    result = dict()
    target_files = os.listdir(target)
    for target_file in target_files:
        target_path = target + target_file
        if extension and not target_path.endswith(extension):
            continue
        if not os.path.isfile(target_path):
            continue
        result[target_file] = timestamp(target_path)
    return result
