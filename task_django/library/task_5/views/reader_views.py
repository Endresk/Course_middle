from rest_framework import viewsets, filters

from task_django.library.lib_models.models import Reader
from task_django.library.task_5.serialasers.reader_serializer import ReaderSerializer


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__fio', 'id']
    ordering_fields = ['user__fio', 'id']
