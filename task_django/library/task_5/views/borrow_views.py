from rest_framework import viewsets, filters

from task_django.library.lib_models.models import Borrow
from task_django.library.task_5.serialasers.borrow_serializer import BorrowSerializer


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = ["date_borrowed"]
    ordering_fields = ['date_borrowed']
