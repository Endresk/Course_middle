from rest_framework import serializers

from task_django.library.lib_models.models import Reader
from task_django.library.task_5.serialasers.agent_serializer import AgentSerializer
from task_django.library.task_5.serialasers.book_serializer import BookSerializer


class ReaderSerializer(serializers.HyperlinkedModelSerializer):
    user = AgentSerializer()
    borrowed_books = BookSerializer()

    class Meta:
        model = Reader
        fields = (
            'id',
            'url',
            'user',
            'borrowed_books',
            'registration_date',
        )
