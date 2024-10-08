from rest_framework import viewsets

from task_django.library.lib_models.models import Agents
from task_django.library.task_5.serialasers.agent_serializer import AgentSerializer


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agents.objects.all()
    serializer_class = AgentSerializer
