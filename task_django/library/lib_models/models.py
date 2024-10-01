from django.db import models
from django.core.exceptions import ValidationError
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
        db_table = 'authors'
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
            shelve=shelve_new
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

    @classmethod
    def sort_books(cls):
        return Book.objects.all().order_by('publication_type', 'title', 'publication_date', 'page_count')

    def return_book(self):
        self.status = 'returned'
        self.date_returned = timezone.now()
        self.book.is_borrowed = False
        self.book.save()
        self.save()
