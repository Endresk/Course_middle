from django.db.models import Count

from task_django.library.lib_models.models import Hall, Book

"""

Отчеты 4 задания:

"""


class Report4:
    def __init__(self):
        super().__init__()
        self.shelves_alphabet = True
        self.shelves_chronology = True

    @classmethod
    def get_halls_with_racks_and_shelves(cls):
        # Вывести список всех залов с наименованием всех связанных стеллажей и полок

        halls = Hall.objects.prefetch_related('rack_set__shelve_set').all()
        dict_all_halls, list_shelve = {}, []

        for hall in halls:
            dict_all_halls[hall.name] = {}

            for rack in hall.rack_set.all():
                dict_all_halls[hall.name][rack.number] = {}

                for shelve in rack.shelve_set.all():
                    list_shelve.append(shelve.number)

                dict_all_halls[hall.name][rack.number] = list_shelve
                list_shelve = []

        return list(dict_all_halls)

    @classmethod
    def get_un_borrowed_books_by_publication_type(cls):
        # Вывести список всех типов публикаций,
        # каждая из них должна содержать наименование книг, которые ни разу не брали читать

        return Book.objects.annotate(
            borrow_count=Count('borrow')).filter(
            borrow_count=0).values('publication_type', 'title')

    def get_output_list_book(self):
        # Вывести список всех книг, у каждой из книг должна быть история перемещения между полками с наименованием
        # каждой из них: один атрибут - полки в алфавитном порядке, второй атрибут - в хронологическом.

        books_movement_history = Book.objects.filter(booklocation__isnull=False).distinct()

        summary = {}

        for book in books_movement_history:
            summary[book.title] = {}
            if self.shelves_alphabet:
                summary[book.title].update(
                    {
                        'алфавитный': list(
                            map(
                                str,
                                sorted(book.booklocation_set.values_list('shelve__number', flat=True))
                            )
                        )
                    }
                )

            if self.shelves_chronology:
                summary[book.title].update(
                    {
                        'хронологический': list(
                            map(
                                str,
                                book.booklocation_set.order_by('date_moved').values_list('shelve__number', flat=True)
                            )
                        )
                    }
                )

        if summary:
            return [f"{k} {v}" for k, v in summary.items()]
        return []
