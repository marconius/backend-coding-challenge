from django.http import HttpResponseNotAllowed
from django.shortcuts import HttpResponse

from .apps import SEARCH_MANAGER


def suggest(request):
    if request.method in ['GET', 'POST']:
        results = SEARCH_MANAGER.search(request.GET['q'])

        content = [serialize_result(hit, results.max_score) for hit in results.hits]
        return HttpResponse(content, content_type='application/json', status=200)

    return HttpResponseNotAllowed(['GET', 'POST'])


def serialize_result(hit, max_score):
    doc = hit['doc']
    canada_regions = {
        '01': 'AL',
        '02': 'BC',
        '03': 'MT',
        '04': 'NB',
        '13': 'NT',
        '07': 'NS',
        '14': 'NU',
        '08': 'ON',
        '09': 'PE',
        '10': 'QC',
        '11': 'SK',
        '12': 'YT',
        '05': 'NL',
    }

    country = 'Canada' if doc['country'] == 'CA' else 'USA'
    region = canada_regions[doc['admin1']] if doc['country'] == 'CA' else doc['admin1']

    return {
        'name': '{}, {}, {}'.format(doc['name'], region, country),
        'latitude': doc['lat'],
        'longitude': doc['long'],
        'score': hit['score'] / max_score,
    }
