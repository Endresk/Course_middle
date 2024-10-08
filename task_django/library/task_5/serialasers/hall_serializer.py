from rest_framework import serializers

from task_django.library.lib_models.models import Hall
from task_django.library.task_5.serialasers.agent_serializer import AgentSerializer


class HallSerializer(serializers.HyperlinkedModelSerializer):
    librarian = AgentSerializer()

    class Meta:
        model = Hall
        fields = (
            'id',
            'url',
            'name',
            'librarian',
        )
