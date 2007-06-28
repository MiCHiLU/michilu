from django.http import Http404
from django.views.generic.simple import direct_to_template
from django.contrib.markup.templatetags.markup import textile, markdown, restructuredtext
from django.contrib.auth.decorators import permission_required
import os.path

def get_source_file(file_path):
    try:
        f = open(file_path)
    except IOError:
        return None
    return f.read()

def markup_dispatch(file_path, markup=None, **argv):
    try:
        extension = os.path.basename(file_path).split(".")[-1]
    except IndexError:
        extension = None
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
    template_name = template_name or "helpdoc/base_site.html"

    file_path = (file_path_pattern or "%s/docs/%s.txt") % (app, doc)
    content = get_source_file(file_path)
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
index = permission_required("is_staff")(index)
