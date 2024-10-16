from rest_framework import serializers

from task_django.library.lib_models.models import Rack, Hall
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

    @staticmethod
    def _shelve(obj):
        return ', '.join(shelve.number for shelve in obj.shelve.all())

    def create(self, validated_data: dict):
        """

        return:
        """
        hall = Hall.objects.get(id=validated_data.pop('hall').get("id"))

        return Rack.objects.create(
            number=validated_data["number"],
            hall=hall
        )

    def update(self, instance, validated_data: dict):
        """

        return:
        """
        instance.number = validated_data.get("number", instance.number)
        instance.hall = validated_data.get("hall", instance.hall)
        instance.save()
        return instance
