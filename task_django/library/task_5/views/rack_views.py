from rest_framework import viewsets

from task_django.library.lib_models.models import Rack
from task_django.library.task_5.serialasers.rack_serializer import RackSerializer


class RackViewSet(viewsets.ModelViewSet):
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
