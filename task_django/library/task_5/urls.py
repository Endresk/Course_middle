from django.urls import path, include
from rest_framework import routers

from task_django.library.task_5.views.agent_views import AgentViewSet
from task_django.library.task_5.views.author_views import AuthorViewSet
from task_django.library.task_5.views.book_location_views import BookLocationViewSet
from task_django.library.task_5.views.book_views import BookViewSet
from task_django.library.task_5.views.borrow_views import BorrowViewSet
from task_django.library.task_5.views.hall_views import HallViewSet
from task_django.library.task_5.views.rack_views import RackViewSet
from task_django.library.task_5.views.reader_views import ReaderViewSet
from task_django.library.task_5.views.shelve_views import ShelveViewSet

router = routers.DefaultRouter()
router.register(r'agent', AgentViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'hall', HallViewSet)
router.register(r'rack', RackViewSet)
router.register(r'shelve', ShelveViewSet)
router.register(r'book', BookViewSet)
router.register(r'reader', ReaderViewSet)
router.register(r'book-location', BookLocationViewSet)
router.register(r'borrow', BorrowViewSet)

drf_urlpatterns = [
    path('', include(router.urls))
]
