from rest_framework import viewsets

from task_django.library.lib_models.models import Agent
from task_django.library.task_5.serialasers.agent_serializer import AgentSerializer


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
