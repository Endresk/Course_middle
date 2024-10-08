from rest_framework import serializers

from task_django.library.lib_models.models import BookLocation
from task_django.library.task_5.serialasers.book_serializer import BookSerializer
from task_django.library.task_5.serialasers.shelve_serializer import ShelveSerializer


class BookLocationSerializer(serializers.HyperlinkedModelSerializer):
    book = BookSerializer()
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
