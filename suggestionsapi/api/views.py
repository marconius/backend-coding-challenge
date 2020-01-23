from django.http import HttpResponseNotAllowed
from django.shortcuts import HttpResponse

from .apps import search_manager


def suggest(request):
    if request.method in ['GET', 'POST']:
        results = search_manager.search(request.GET['q'])
        # return HttpResponse(serialize(results), status=200)
        return HttpResponse(results, content_type='application/json', status=200)

    return HttpResponseNotAllowed(['GET', 'POST'])
