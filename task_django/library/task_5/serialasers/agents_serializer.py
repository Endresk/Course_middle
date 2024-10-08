from rest_framework import serializers

from task_django.library.lib_models.models import Agents


class AgentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agents
        fields = (
            'id',
            'url',
            'fio',
            'birth_date',
            'sex',
        )
