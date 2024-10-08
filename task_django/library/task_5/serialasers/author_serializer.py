from rest_framework import serializers

from task_django.library.lib_models.models import Authors
from task_django.library.task_5.serialasers.agent_serializer import AgentSerializer


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = AgentSerializer()

    class Meta:
        model = Authors
        fields = (
            'id',
            'url',
            'user',
            'biography',
        )
