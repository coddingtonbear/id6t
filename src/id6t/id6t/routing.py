from channels.routing import ProtocolTypeRouter, URLRouter
from .maxwell import routing

application = ProtocolTypeRouter({
    'http': URLRouter(routing.urlpatterns)
})
