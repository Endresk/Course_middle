from rest_framework import serializers

from task_django.library.lib_models.models import Book
from task_django.library.task_5.serialasers.agent_serializer import AgentSerializer
from task_django.library.task_5.serialasers.shelve_serializer import ShelveSerializer


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = AgentSerializer()
    shelve = ShelveSerializer()

    class Meta:
        model = Book
        fields = (
            'id',
            'url',
            'title',
            'authors',
            'publication_type',
            'number',
            'page_count',
            'publication_date',
            'description',
            'shelve',
            'is_borrowed',
        )
