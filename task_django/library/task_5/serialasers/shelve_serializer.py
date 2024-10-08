from rest_framework import serializers

from task_django.library.lib_models.models import Shelve
from task_django.library.task_5.serialasers.rack_serializer import RackSerializer


class ShelveSerializer(serializers.HyperlinkedModelSerializer):
    rack = RackSerializer()

    class Meta:
        model = Shelve
        fields = (
            'id',
            'url',
            'number',
            'rack',
        )
