from rest_framework import serializers

from task_django.library.lib_models.models import Authors
from task_django.library.task_5.serialasers.agents_serializer import AgentsSerializer


class AuthorsSerializer(serializers.HyperlinkedModelSerializer):
    user = AgentsSerializer()

    class Meta:
        model = Authors
        fields = (
            'id',
            'url',
            'user',
            'biography',
        )
