from rest_framework import viewsets, filters

from task_django.library.lib_models.models import Author
from task_django.library.task_5.serialasers.author_serializer import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user']
    ordering_fields = ['user']
