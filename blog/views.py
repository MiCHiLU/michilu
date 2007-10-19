from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404
from django.core import serializers
from michilu.blog.models import Entry
from michilu.utils.utils import mimetype


def search(request):
    keyword = request.GET.get("q")
    if not keyword:
        return None, None
    entry_list = Entry.objects.filter(content__contains=keyword).order_by("-add_date")
    return keyword, entry_list

def search_html(request):
    keyword, entry_list = search(request)
    if not keyword:
        return render_to_response('bbs/search.html', {}, context_instance=RequestContext(request));
    numbers = entry_list.count()
    return direct_to_template(request, 'bbs/search.html', {
        'keyword': keyword,
        'numbers': numbers,
        'entry_list': entry_list,
    })


model_dict = dict(
    entry = Entry,
)

def to_jsonp(callback, result):
    return "%s(%s)" % (callback, result)

def serialized_response(objects, callback=None):
    result = serializers.serialize("json", objects)
    if callback:
        result = to_jsonp(callback, result)
    return HttpResponse(result, mimetype=mimetype("json"))

def get_latest(request):
    objects = list()
    callback = request.GET.get("callback", None)
    for key, model in model_dict.items():
        try:
            objects.extend(get_list_or_404(model))
        except Http404:
            continue
    return serialized_response(objects, callback)

def get_item(request):
    objects = list()
    callback = request.GET.get("callback", None)
    model = request.POST.get("model", None)
    if model in model_dict.keys():
        try:
            objects.extend(get_list_or_404(model_dict[model], id=object_id))
        except Http404:
            pass
    return serialized_response(objects, callback)
