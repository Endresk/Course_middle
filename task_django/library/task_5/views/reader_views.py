from rest_framework import viewsets

from task_django.library.lib_models.models import Reader
from task_django.library.task_5.serialasers.reader_serializer import ReaderSerializer


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
