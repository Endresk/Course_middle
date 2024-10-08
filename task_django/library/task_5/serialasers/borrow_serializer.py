from rest_framework import serializers

from task_django.library.lib_models.models import Borrow
from task_django.library.task_5.serialasers.book_location_serializer import BookLocationSerializer
from task_django.library.task_5.serialasers.book_serializer import BookSerializer
from task_django.library.task_5.serialasers.reader_serializer import ReaderSerializer


class BorrowSerializer(serializers.HyperlinkedModelSerializer):
    book = BookSerializer()
    reader = ReaderSerializer()
    book_location = BookLocationSerializer()

    class Meta:
        model = Borrow
        fields = (
            'id',
            'url',
            'book',
            'reader',
            'book_location',
            'status',
            'date_borrowed',
            'date_returned',
        )
