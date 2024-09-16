from datetime import timedelta

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Count, Avg
from django.utils import timezone


class Agents(models.Model):
    fio = models.CharField("ФИО", max_length=255)
    birth_date = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    sex = models.BooleanField(verbose_name="Пол")

    def __str__(self):
        return f"{self.fio}"

    class Meta:
        db_table = "agents"
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class Authors(models.Model):
    user = models.OneToOneField(Agents, verbose_name="Автор", on_delete=models.PROTECT)
    biography = models.TextField(verbose_name="Биография>", blank=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        db_table = 'Authors'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Hall(models.Model):
    name = models.CharField('Название зала', max_length=100)
    librarian = models.ForeignKey(Agents, verbose_name="Библиотекарь", on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "hall"
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'


class Rack(models.Model):
    number = models.IntegerField('Номер стеллажа')
    hall = models.ForeignKey(Hall, verbose_name="Зал", on_delete=models.PROTECT)

    def __str__(self):
        return self.number

    class Meta:
        db_table = "rack"
        verbose_name = 'Стеллаж'
        verbose_name_plural = 'Стеллажи'
        unique_together = ('number', 'hall')


class Shelve(models.Model):
    number = models.IntegerField('Номер полки')
    rack = models.ForeignKey(Rack, verbose_name="Стеллаж", on_delete=models.PROTECT)

    def __str__(self):
        return self.number

    class Meta:
        db_table = "shelve"
        verbose_name = 'Полка'
        verbose_name_plural = 'Полки'
        unique_together = ('number', 'rack')


class Book(models.Model):
    title = models.CharField('Название книги', max_length=200)
    authors = models.ManyToManyField(Agents, verbose_name='Авторы книги', max_length=100)
    publication_type = models.CharField('Вид издания', max_length=50)
    number = models.PositiveIntegerField("Номер издания")
    page_count = models.PositiveSmallIntegerField('Количество страниц')
    publication_date = models.DateField("Дата издания")
    description = models.TextField("Описание")
    shelve = models.ForeignKey(Shelve, verbose_name="Полка", null=True, blank=True, on_delete=models.PROTECT)
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def move_to(self, shelve_new):
        BookLocation.objects.create(
            book=self,
            shelve=shelve_new.rack.hall
        )
        self.shelve = shelve_new
        self.save()

    class Meta:
        db_table = "book"
        ordering = ['title']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Reader(models.Model):
    user = models.OneToOneField(Agents, on_delete=models.PROTECT)
    borrowed_books = models.ManyToManyField(Book)
    registration_date = models.DateTimeField("Дата регистрация читателя", auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        db_table = "reader"
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'


class BookLocation(models.Model):
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.PROTECT)
    shelve = models.ForeignKey(Shelve, verbose_name="Полка", on_delete=models.PROTECT)
    status = models.CharField('Статус', max_length=20,
                              choices=[('hall', 'В зале'), ('outside', 'Вне библиотеки')],
                              default='hall')
    date_moved = models.DateTimeField('Дата перемещения', auto_now_add=True)

    def __str__(self):
        return self.book

    class Meta:
        db_table = "book_location"
        verbose_name = 'Местоположение книги'
        verbose_name_plural = 'Местоположения книг'


class Borrow(models.Model):
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.PROTECT)
    reader = models.ForeignKey(Reader, verbose_name="Читатель", on_delete=models.PROTECT)
    book_location = models.ForeignKey(BookLocation, verbose_name="Местоположение книги", on_delete=models.PROTECT)
    status = models.CharField('Статус', max_length=20,
                              choices=[('on_your_hands', 'На руках'), ('returned', 'Возвращена')],
                              default='on_your_hands')
    date_borrowed = models.DateTimeField("Дата взятия книги", auto_now_add=True)
    date_returned = models.DateTimeField("Дата возвращения книги", null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} - {self.reader.user.fio}"

    class Meta:
        db_table = "borrow"
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'

    def save(self, *args, **kwargs):
        if self.status == 'on_your_hands':
            if self.reader.borrow_set.filter(status='on_your_hands').count() >= 3:
                raise ValidationError("Читатель уже взял 3 книги, больше взять не может.")
            if self.book.is_borrowed:
                raise ValidationError("Книга уже взята другим читателем.")
            self.book.is_borrowed = True
            self.book.save()
        super().save(*args, **kwargs)

    # Ищем свободную полку по порядку и кладем туда книгу
    def first_available_shelve(self):
        halls = Hall.objects.all()
        for _hall in halls:
            racks = Rack.objects.filter(hall=_hall)
            for _rack in racks:
                _shelves = Shelve.objects.filter(rack=_rack)
                for _shelve in _shelves:
                    if not Book.objects.filter(shelve=_shelve).exists():
                        self.book.shelve = _shelve
                        self.book.save()
                        return

    @staticmethod
    def sort_books():
        return Book.objects.all().order_by('publication_type', 'title', 'publication_date', 'page_count')

    def return_book(self):
        self.status = 'returned'
        self.date_returned = timezone.now()
        self.book.is_borrowed = False
        self.book.save()
        self.save()


for hall_number in range(1, 4):  # 3 зала

    librarian = Agents.objects.create_user(username=f'librarian {hall_number}')
    hall = Hall.objects.create(name=f'Зал {hall_number}', librarian=librarian)
    hall.save()

    for rack_number in range(1, 6):  # 5 стеллажей
        rack = Rack.objects.create(number=rack_number, hall=hall)
        rack.save()

        for shelve_number in range(1, 7):  # 6 полок на стеллаже
            shelve = Shelve.objects.create(number=shelve_number, rack=rack)
            shelve.save()

            for book_number in range(1, 11):  # 10 книг на полке
                Book.objects.create(
                    title=f'Книга {hall_number}.{rack_number}.{shelve_number}.{book_number}',
                    author=f'Автор {book_number}',
                    shelve=shelve)
                Book.save()

# Получаем книгу
book = Book.objects.get(id=1)
# Получаем другую полку
_shelve = Shelve.objects.get(id=2)

# Перемещаем книгу
book.move_to(_shelve)

reader = Reader.objects.get(user__fio='reader 1')

book_location = BookLocation.objects.get(id=1)

borrow_record = Borrow(book=book, reader=reader, book_location=book_location)

# Сортировка книг
sorted_books = borrow_record.sort_books()
for book in sorted_books:
    print(book.title)

# Попытка взять книгу
try:
    borrow_record.save()
    print(f'Книга "{book.title}" успешно взята.')

    # Возврат книги
    borrow_record.return_book()
    print(f'Книга "{book.title}" успешно возвращена.')
except ValidationError as e:
    print(e)


# Количество книг определенного автора в библиотеке
Book.objects.filter(authors='Автор 1').count()

# Периодически библиотекарям требуется сборка следующих отчетов

thirty_day = timezone.now() - timedelta(days=30)
borrow = Borrow.objects.filter(date_borrowed__gte=thirty_day)

# 10 самых популярных книг за последний месяц
popular_books_ten = borrow.values('book').annotate(Count("book")).order_by('-count')[:10]

# Количество книг, которые сейчас находятся на руках в разрезе читателей
Borrow.objects.filter(status='on_your_hands').values('reader').annotate(Count("book"))

# Перечень читателей, которые просрочили возврат книг
Borrow.objects.filter(status='on_your_hands', date_borrowed__lt=thirty_day).values('reader').distinct()

# 10 самых активных читателей, которые взяли больше всего книг, за прошедший месяц
active_reader_ten = borrow.values('reader').annotate(Count("book")).order_by('-count')[:10]

# Среднее количество страниц в разрезе видов изданий, которые прочитали читатели за последний месяц
average_page_count = borrow.values('book__publication_type').annotate(Avg('book__page_count'))

# 10 самых перемещаемых книг за последний месяц
book_location = BookLocation.objects.filter(date_moved__gte=thirty_day)
moved_ten = book_location.values('book').annotate(Count("book")).order_by('-count')[:10]
