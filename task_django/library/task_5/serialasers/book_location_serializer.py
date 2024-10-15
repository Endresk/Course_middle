from django.db.models import Count
from rest_framework import serializers

from task_django.library.lib_models.models import BookLocation, Book, Shelve
from task_django.library.task_5.serialasers.shelve_serializer import ShelveSerializer


class BookLocationSerializer(serializers.HyperlinkedModelSerializer):
    shelve = ShelveSerializer()

    class Meta:
        model = BookLocation
        fields = (
            'id',
            'url',
            'book',
            'shelve',
            'status',
            'date_moved',
        )

    def create(self, validated_data: dict):
        """

        return:
        """
        book = Book.objects.get(id=validated_data.pop('book').get("id"))
        shelve = Shelve.objects.get(id=validated_data.pop('shelve').get("id"))

        return BookLocation.objects.create(
            book=book,
            shelve=shelve,
            status=validated_data["status"],
            date_moved=validated_data["date_moved"],
        )

    def update(self, instance, validated_data: dict):
        """

        return:
        """
        instance.book = Book.objects.get(id=validated_data.pop('book').get("id"))
        instance.shelve = Shelve.objects.get(id=validated_data.pop('shelve').get("id"))
        instance.status = validated_data.get("status", instance.status)
        instance.date_moved = validated_data.get("date_moved", instance.date_moved)
        instance.save()
        return instance
