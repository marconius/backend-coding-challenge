from django.http import HttpResponseNotAllowed, JsonResponse

from .apps import SEARCH_MANAGER


def suggest(request):
    if request.method in ['GET', 'POST']:
        lat = request.GET.get('latitude')
        lng = request.GET.get('longitude')
        latlng = (lat, lng) if lat and lng else None
        results = SEARCH_MANAGER.search(request.GET['q'], latlng)

        content = {'suggestions': [format_result(hit, results.max_score) for hit in results.hits]}
        return JsonResponse(content, content_type='application/json', status=200)

    return HttpResponseNotAllowed(['GET', 'POST'])


def format_result(hit, max_score):
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
        # Score definitely does _not_ reflect confidence. It is basically a dumb way to make the
        # API show a value between 0 and 1.
        'score': hit['score'] / max_score,
    }
