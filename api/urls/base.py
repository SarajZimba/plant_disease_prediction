from .user import urlpatterns as user_urlpatterns
from .image import urlpatterns as image_urlpatterns

urlpatterns = (
    [] + user_urlpatterns + image_urlpatterns
)