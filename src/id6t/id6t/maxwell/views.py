import json

import redis

from django.conf import settings
from django.template.response import TemplateResponse


def main(request):
    connection = redis.Redis(
        settings.REDIS_HOST,
        settings.REDIS_PORT,
    )
    state = connection.get('maxwell.state').decode('utf-8')
    return TemplateResponse(
        request,
        "main.html",
        {
            "mapsApiKey": settings.GMAPS_API_KEY,
            "state": json.dumps(state)
        }
    )
