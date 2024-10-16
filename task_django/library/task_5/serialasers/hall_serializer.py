from rest_framework import serializers

from task_django.library.lib_models.models import Hall, Agent
from task_django.library.task_5.serialasers.agent_serializer import AgentSerializer


class HallSerializer(serializers.HyperlinkedModelSerializer):
    librarian = AgentSerializer()

    class Meta:
        model = Hall
        fields = (
            'id',
            'url',
            'name',
            'librarian',
        )

    @staticmethod
    def _rack(obj):
        return ', '.join(rack.number for rack in obj.racks.all())

    def create(self, validated_data: dict):
        """

        return:
        """
        return Hall.objects.create(
            name=validated_data["name"],
            librarian=Agent.objects.get(id=validated_data.pop('librarian').get("id")),
        )

    def update(self, instance, validated_data: dict):
        """

        return:
        """
        instance.name = validated_data.get("name", instance.name)
        instance.librarian = Agent.objects.get(id=validated_data.pop('librarian').get("id"))
        instance.save()
        return instance

