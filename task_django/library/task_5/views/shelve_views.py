from rest_framework import viewsets, filters

from task_django.library.lib_models.models import Shelve
from task_django.library.task_5.serialasers.shelve_serializer import ShelveSerializer


class ShelveViewSet(viewsets.ModelViewSet):
    queryset = Shelve.objects.all()
    serializer_class = ShelveSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['number']
    ordering_fields = ['number', 'id']