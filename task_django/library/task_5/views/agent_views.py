from rest_framework import viewsets

from task_django.library.lib_models.models import Agents
from task_django.library.task_5.serialasers.agents_serializer import AgentsSerializer


class AgentsViewSet(viewsets.ModelViewSet):
    queryset = Agents.objects.all()
    serializer_class = AgentsSerializer
