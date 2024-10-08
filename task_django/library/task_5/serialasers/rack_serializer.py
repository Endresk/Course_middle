from rest_framework import serializers

from task_django.library.lib_models.models import Rack
from task_django.library.task_5.serialasers.hall_serializer import HallSerializer


class RackSerializer(serializers.HyperlinkedModelSerializer):
    hall = HallSerializer()

    class Meta:
        model = Rack
        fields = (
            'id',
            'url',
            'number',
            'hall',
        )
