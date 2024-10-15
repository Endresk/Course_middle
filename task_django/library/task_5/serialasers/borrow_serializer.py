from rest_framework import serializers

from task_django.library.lib_models.models import Borrow, Book, Reader, BookLocation
from task_django.library.task_5.serialasers.book_location_serializer import BookLocationSerializer
from task_django.library.task_5.serialasers.book_serializer import BookSerializer
from task_django.library.task_5.serialasers.reader_serializer import ReaderSerializer


class BorrowSerializer(serializers.HyperlinkedModelSerializer):
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

    def create(self, validated_data: dict):
        """

        return:
        """
        book = Book.objects.get(id=validated_data.pop('book').get("id"))
        reader = Reader.objects.get(id=validated_data.pop('reader').get("id"))
        book_location = BookLocation.objects.get(id=validated_data.pop('book_location').get("id"))

        return Borrow.objects.create(
            book=book,
            reader=reader,
            book_location=book_location,
            status=validated_data["status"],
            date_borrowed=validated_data["date_borrowed"],
            date_returned=validated_data["date_returned"],
        )

    def update(self, instance, validated_data: dict):
        """

        return:
        """
        instance.book_location = BookLocation.objects.get(id=validated_data.pop('book_location').get("id"))
        instance.status = validated_data.get("status", instance.status)
        instance.date_borrowed = validated_data.get("date_borrowed", instance.date_borrowed)
        instance.date_returned = validated_data.get("date_returned", instance.date_returned)
        instance.save()
        return instance
