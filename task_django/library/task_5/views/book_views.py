from rest_framework import viewsets

from task_django.library.lib_models.models import Book
from task_django.library.task_5.serialasers.book_serializer import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
