
from django.http import HttpResponse

from task_django.library.task_4.models import Borrow


def my_view(request):

    return HttpResponse(Borrow().get_output_list_book(True, True))
