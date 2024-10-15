from rest_framework import serializers

from task_django.library.lib_models.models import Author
from task_django.library.task_5.serialasers.agent_serializer import AgentSerializer


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = AgentSerializer()

    class Meta:
        model = Author
        fields = (
            'id',
            'url',
            'user',
            'biography',
        )
