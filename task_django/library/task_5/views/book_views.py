from rest_framework import viewsets, filters

from task_django.library.lib_models.models import Book
from task_django.library.task_5.serialasers.book_serializer import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "author",
        "title",
        "description",
        "publication_type__title",
        "publication_date",
    ]
    ordering_fields = ["author", "title", "publication_type__title", "publication_date"]
