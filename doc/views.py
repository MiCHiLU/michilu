from django.http import HttpResponse
from django.utils import simplejson, dateformat, simplejson
from django.conf import settings
from michilu.helpdoc import util
from michilu.helpdoc import views as helpdoc_views
from michilu.blog.views import to_jsonp
from michilu.utils.utils import http_header_style_datetime, mimetype

exclude_list = ["writing-apps-guide-outline.txt"]

def doc_index_json(request, target_dir, base_url, callback="callback"):
    callback = request.GET.get(callback, None)
    result = dict()
    timestamp_dict = util.get_timestamp(target_dir, extension=".txt")
    for key,value in timestamp_dict.items():
        if key in exclude_list:
            continue
        key = base_url % key[:key.rindex(".")]
        result[key] = dateformat.DateFormat(value).format("r")
    result = "[%s]" % simplejson.dumps(result)
    if callback:
        result = to_jsonp(callback, result)
    return HttpResponse(result, mimetype=mimetype("json"))

def render(request, *args, **kwargs):
    response = helpdoc_views.render(request, *args, **kwargs)
    response['Last-Modified'] = http_header_style_datetime(
        util.get_timestamp(
            kwargs["file_path_pattern"] % ("", kwargs["doc"]),
            utc = True,
        ),
    )
    return response

def manifest(request):
    manifest_base = dict(
        betaManifestVersion = int(1),
        version = str(),
        entries = list(),
    )
    url_base = "/static/"
    filepath_base = "%sstatic/" % settings.PROJECT_PATH
    entry_base = (
        "lib/jQuery/jquery-1.1.2.pack.js",
        "google/gears/gears_init.js",
        "doc-ja/css/",
        "doc-ja/js/",
        "doc-ja/img/",
        "doc-ja/img/webicons/",
    )

    versions = list()
    entries = list()
    get_timestamp = lambda x: (x, util.get_timestamp(filepath_base + x, raw=True))
    for path, epochs in (get_timestamp(path) for path in entry_base):
        if isinstance(epochs, dict):
            path = [path + filename for filename in epochs.keys()]
            epochs = epochs.values()
        elif isinstance(epochs, int):
            path = (path,)
            epochs = (epochs,)
        entries.extend(list(path))
        versions.extend(list(epochs))
    entries = [url_base + entry for entry in entries]
    versions.sort()

    result = manifest_base
    result.update(dict(
        version = str(versions[-1]),
        entries = [dict(url=entry, src=entry) for entry in entries],
    ))
    return HttpResponse(simplejson.dumps(result), mimetype=mimetype("json"))
