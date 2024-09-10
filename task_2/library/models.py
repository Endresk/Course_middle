from django.contrib.auth.models import User
from django.db import models


class Hall(models.Model):
    name = models.CharField('Название зала', max_length=100)
    librarian = models.ForeignKey(User, verbose_name="Библиотекарь", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'


class Rack(models.Model):
    number = models.IntegerField('Номер стеллажа')
    hall = models.ForeignKey(Hall, verbose_name="Зал", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Стеллаж'
        verbose_name_plural = 'Стеллажи'
        unique_together = ('number', 'hall')


class Shelve(models.Model):
    number = models.IntegerField('Номер полки')
    rack = models.ForeignKey(Rack, verbose_name="Стеллаж", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Полка'
        verbose_name_plural = 'Полки'
        unique_together = ('number', 'rack')


class Book(models.Model):
    title = models.CharField('Название книги', max_length=200)
    authors = models.ManyToManyField(User, related_name='books', verbose_name='Авторы книги', max_length=100)
    publication_type = models.CharField('Вид издания', max_length=50)
    number = models.PositiveIntegerField("Номер издания")
    page_count = models.PositiveSmallIntegerField('Количество страниц')
    publication_date = models.DateField("Дата издания")
    description = models.TextField("Описание")
    shelve = models.ForeignKey(Shelve, verbose_name="Полка", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    borrowed_books = models.ManyToManyField(Book)
    registration_date = models.DateTimeField("Дата регистрация читателя", auto_now_add=True)

    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'


class BookLocation(models.Model):
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)
    shelve = models.ForeignKey(Shelve, verbose_name="Полка", on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=20,
                              choices=[('hall', 'В зале'), ('outside', 'Вне библиотеки')],
                              default='hall')
    date_moved = models.DateTimeField('Дата перемещения', auto_now_add=True)

    class Meta:
        verbose_name = 'Местоположение книги'
        verbose_name_plural = 'Местоположения книг'


class Borrow(models.Model):
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, verbose_name="Читатель", on_delete=models.CASCADE)
    book_location = models.ForeignKey(BookLocation, verbose_name="Местоположение книги", on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=20,
                              choices=[('on_your_hands', 'На руках'), ('returned', 'Возвращена')],
                              default='on_your_hands')
    date_borrowed = models.DateTimeField("Дата взятия книги", auto_now_add=True)
    date_returned = models.DateTimeField("Дата возвращения книги", null=True, blank=True)

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
