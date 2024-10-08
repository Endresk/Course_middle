from rest_framework import viewsets

from task_django.library.lib_models.models import Shelve
from task_django.library.task_5.serialasers.shelve_serializer import ShelveSerializer


class ShelveViewSet(viewsets.ModelViewSet):
    queryset = Shelve.objects.all()
    serializer_class = ShelveSerializer
