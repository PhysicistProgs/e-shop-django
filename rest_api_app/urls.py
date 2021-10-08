from rest_framework import routers
from django.conf.urls import url, include

from .rest_classes.views import UserViewSet, ShoeViewSet

app_name = 'rest_api_app'

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('shoes', ShoeViewSet)

urlpatterns = [
    url('', include(router.urls))
]


