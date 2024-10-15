from rest_framework import serializers

from task_django.library.lib_models.models import Agent


class AgentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agent
        fields = (
            'id',
            'url',
            'fio',
            'birth_date',
            'sex',
        )
