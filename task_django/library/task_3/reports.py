from datetime import timedelta
from django.db.models import Count, Avg
from django.utils import timezone

from task_django.library.lib_models.models import Borrow, BookLocation, Book

"""

Отчеты 3 задания:

"""


class Report3:

    @classmethod
    def thirty_day(cls):
        return timezone.now() - timedelta(days=30)

    def borrow(self):
        return Borrow.objects.filter(date_borrowed__gte=self.thirty_day())

    @classmethod
    def get_book_count_by_author(cls):
        # Количество книг определенного автора в библиотеке
        return Book.objects.filter(authors='Автор 1').count()

    def get_popular_books_last_month(self):
        # 10 самых популярных книг за последний месяц
        return self.borrow().values('book').annotate(book_count=Count("book")).order_by('-book_count')[:10]

    def get_books_on_hand_by_reader(self):
        # Количество книг, которые сейчас находятся на руках в разрезе читателей
        return self.borrow().objects.filter(status='on_your_hands').values(
            reader_book='reader').annotate(Count("reader_book"))

    def get_overdue_readers(self):
        # Перечень читателей, которые просрочили возврат книг
        return Borrow.objects.filter(
            status='on_your_hands',
            date_borrowed__lt=self.thirty_day()).values('reader').distinct()

    def get_most_active_readers_last_month(self):
        # 10 самых активных читателей, которые взяли больше всего книг, за прошедший месяц
        return self.borrow().values('reader').annotate(book_count=Count("book")).order_by('-book_count')[:10]

    def get_average_pages_by_publication_type_last_month(self):
        # Среднее количество страниц в разрезе видов изданий, которые прочитали читатели за последний месяц
        return self.borrow().values('book__publication_type').annotate(Avg('book__page_count'))

    def get_most_moved_books_last_month(self):
        # 10 самых перемещаемых книг за последний месяц
        book_location = BookLocation.objects.filter(date_moved__gte=self.thirty_day())
        return book_location.values('book').annotate(book_count=Count("book")).order_by('-book_count')[:10]
