from rest_framework import serializers

from task_django.library.lib_models.models import Hall
from task_django.library.task_5.serialasers.agents_serializer import AgentsSerializer


class HallSerializer(serializers.HyperlinkedModelSerializer):
    librarian = AgentsSerializer()

    class Meta:
        model = Hall
        fields = (
            'id',
            'url',
            'name',
            'librarian',
        )
