from .serializers import (
    UserSerializer,
    ShoeSerializer
)

from started_app.models import Shoe
from django.contrib.auth.models import User
from rest_framework import viewsets


class ShoeViewSet(viewsets.ModelViewSet):
    queryset = Shoe.available_shoes.all()
    serializer_class = ShoeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
