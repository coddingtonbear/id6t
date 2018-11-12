from django.conf.urls import url
from channels.http import AsgiHandler

from .consumers import MaxwellConsumer


urlpatterns = [
    url(
        r'^events/',
        MaxwellConsumer
    ),
    url(r'', AsgiHandler),
]
