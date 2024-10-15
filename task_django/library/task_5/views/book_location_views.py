from rest_framework import viewsets, filters

from task_django.library.lib_models.models import BookLocation
from task_django.library.task_5.serialasers.book_location_serializer import BookLocationSerializer


class BookLocationViewSet(viewsets.ModelViewSet):
    queryset = BookLocation.objects.all()
    serializer_class = BookLocationSerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = ['book']
    ordering_fields = ['book', 'id']
