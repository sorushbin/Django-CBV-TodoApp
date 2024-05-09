from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import requests
from .serializers import TodoSerializer
from .permissions import IsOwnerOrReadOnly
from ...models import Task


class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["done"]


class WeatherApiView(APIView):
    @method_decorator(cache_page(20*60))
    def get(self, request,*args, **kwargs ):
        city_name = kwargs.get("city_name")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=e1176c2224faec7d17373814500b2fa7"
        response = requests.get(url)
        return JsonResponse(response.json())