from rest_framework import serializers

from task_django.library.lib_models.models import Shelve, Rack
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

    def create(self, validated_data: dict):
        """

        return:
        """
        return Shelve.objects.create(
            number=validated_data["number"],
            rack=Rack.objects.get(id=validated_data.pop('rack').get("id")),
        )

    def update(self, instance, validated_data: dict):
        """

        return:
        """
        instance.number = validated_data.get("number", instance.number)
        instance.rack = Rack.objects.get(id=validated_data.pop('rack').get("id"))
        instance.save()
        return instance
