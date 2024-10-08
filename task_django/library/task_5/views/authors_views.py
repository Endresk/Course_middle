from rest_framework import viewsets

from task_django.library.lib_models.models import Authors
from task_django.library.task_5.serialasers.authors_serializer import AuthorsSerializer


class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer
