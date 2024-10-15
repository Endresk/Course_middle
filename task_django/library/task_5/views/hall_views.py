from rest_framework import viewsets, filters

from task_django.library.lib_models.models import Hall
from task_django.library.task_5.serialasers.hall_serializer import HallSerializer


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'id']