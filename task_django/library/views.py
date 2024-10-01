
from django.http import HttpResponse

from task_django.library.task_4.models import Report4


def my_view(request):

    return HttpResponse(Report4().get_output_list_book())
