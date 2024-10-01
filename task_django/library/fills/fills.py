from datetime import datetime

from task_django.library.lib_models.models import Borrow, Reader, BookLocation, Book, Shelve, Agents, Rack, Hall


class Fills:
    @classmethod
    def create(cls):
        for hall_number in range(1, 4):  # 3 зала

            librarian = Agents.objects.create(fio=f'librarian {hall_number}', sex=True)
            hall = Hall.objects.create(name=f'Зал {hall_number}', librarian=librarian)
            hall.save()

            for rack_number in range(1, 6):  # 5 стеллажей
                rack = Rack.objects.create(number=rack_number, hall=hall)
                rack.save()

                for shelve_number in range(1, 7):  # 6 полок на стеллаже
                    shelve = Shelve.objects.create(number=shelve_number, rack=rack)
                    shelve.save()

                    for book_number in range(1, 11):  # 10 книг на полке
                        agent = Agents.objects.create(fio=f'Автор {book_number}', sex=True)

                        book = Book.objects.create(
                            title=f'Книга {hall_number}.{rack_number}.{shelve_number}.{book_number}',
                            number=1,
                            page_count=1,
                            publication_date=datetime.now(),
                            shelve=shelve)

                        book.authors.add(agent)
                        book.save()

    @classmethod
    def get_book(cls):
        # Получаем книгу
        return Book.objects.get(id=1)

    @classmethod
    def get_shelve(cls):
        # Получаем полку
        return Shelve.objects.get(id=2)

    @classmethod
    def moving_book(cls, book, shelve):
        # Перемещаем книгу
        book.move_to(shelve)

    @classmethod
    def get_reader(cls, book):
        return Borrow(book=book,
                      reader=Reader.objects.get(user__fio='reader 1'),
                      book_location=BookLocation.objects.get(id=1))

    @classmethod
    def _sort_books(cls, borrow_record):
        # Сортировка книг
        sorted_books = borrow_record.sort_books()
        for book in sorted_books:
            print(book.title)

    @classmethod
    def take_book(cls, borrow_record, book):

        # Попытка взять книгу
        borrow_record.save()
        print(f'Книга "{book.title}" успешно взята.')

    @classmethod
    def _return_book(cls, borrow_record, book):
        # Возврат книги
        borrow_record.return_book()
        print(f'Книга "{book.title}" успешно возвращена.')
