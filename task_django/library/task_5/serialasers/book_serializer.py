from django.db.models import Count
from rest_framework import serializers

from task_django.library.lib_models.models import Book, Shelve, Author
from task_django.library.task_5.serialasers.agent_serializer import AgentSerializer
from task_django.library.task_5.serialasers.author_serializer import AuthorSerializer
from task_django.library.task_5.serialasers.shelve_serializer import ShelveSerializer


class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = AgentSerializer(many=True)
    shelve = ShelveSerializer()

    class Meta:
        model = Book
        fields = (
            'id',
            'url',
            'title',
            'author',
            'publication_type',
            'number',
            'page_count',
            'publication_date',
            'description',
            'shelve',
            'is_borrowed',
        )

    def create(self, validated_data: dict):
        """

        return:
        """
        author = self.get_author(validated_data)
        shelve = Shelve.objects.annotate(book_count=Count("book")).filter(book_count__lt=1).first()

        return Book.objects.create(
            title=validated_data["title"],
            author=author,
            publication_type=validated_data["publication_type"],
            number=validated_data["number"],
            page_count=validated_data["page_count"],
            publication_date=validated_data["publication_date"],
            description=validated_data["description"],
            shelve=shelve,
        )

    def update(self, instance, validated_data: dict):
        """

        return:
        """
        instance.author = self.get_author(validated_data)
        instance.publication_date = validated_data.get("publication_date", instance.publication_date)
        instance.description = validated_data.get("description", instance.description)
        instance.shelve = Shelve.objects.annotate(book_count=Count("book")).filter(book_count__lt=1).first()
        instance.save()
        return instance

    @staticmethod
    def get_author(data):
        """

        return:
        """
        authors = []
        for _author in data.pop('author'):
            author = Author.objects.annotate(
                author_count=Count("author").filter(book_count__lt=1).first()
            )
            if not author:
                author_serializer = AuthorSerializer(data=_author)
                author_serializer.is_valid()
                author = author_serializer.save()
            authors.append(author)
        return authors
