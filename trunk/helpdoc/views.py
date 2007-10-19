from django.http import Http404
from django.views.generic.simple import direct_to_template
from django.contrib.markup.templatetags.markup import textile, markdown, restructuredtext
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os.path
import codecs
import util

def find_source_file(file_path):
    if os.path.exists(file_path):
        return file_path
    file_path = os.path.splitext(file_path)[0]
    for extension in util.markup_extensions:
        _file_path = "%s.%s" % (file_path, extension)
        if os.path.exists(_file_path):
            return _file_path
    return None

def get_source_file(file_path, encoding=None, **argv):
    _file_path = find_source_file(file_path)
    if not _file_path:
        return None, None
    try:
        if encoding:
            f = codecs.open(_file_path, mode="r", encoding=encoding)
        else:
            f = open(_file_path)
    except IOError:
        return None, None
    return f.read(), _file_path

def markup_dispatch(file_path, markup=None, **argv):
    extension = os.path.splitext(file_path)[1][1:]
    markup_dict = dict(
        textile = textile,
        markdown = markdown,
        rst = restructuredtext,
        html = None,
    )
    markup = markup or "rst"
    if extension in markup_dict.keys():
        return markup_dict[extension]
    elif markup in markup_dict.keys():
        return markup_dict[markup]
    else:
        return None

def render(request, doc, app=None, file_path_pattern=None, base_url=None,
            template_name=None, **argv):
    app = app or ""
    if not base_url:
        if hasattr(settings, "HELPDOC_BASE_URL"):
            base_url = settings.HELPDOC_BASE_URL
        else:
            base_url = ""
    template_name = template_name or "helpdoc/base_site.html"

    file_path = (file_path_pattern or "%s/docs/%s.txt") % (app, doc)
    content, file_path = get_source_file(file_path, **argv)
    if not content:
        raise Http404
    markup = markup_dispatch(file_path, **argv)
    if callable(markup):
        content = markup(content)
    return  direct_to_template(request, template_name, dict(
        content = content,
        base_url = base_url,
    ))

def index(request, base_url=None):
    extra_context = {}
    if base_url:
        extra_context.update(dict(base_url=base_url))
    return direct_to_template(request, "helpdoc/index.html", extra_context=extra_context)
index = login_required(index)

