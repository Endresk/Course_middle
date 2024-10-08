from rest_framework import viewsets

from task_django.library.lib_models.models import Authors
from task_django.library.task_5.serialasers.author_serializer import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializer
