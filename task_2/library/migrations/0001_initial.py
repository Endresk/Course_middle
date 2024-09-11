# Generated by Django 5.1.1 on 2024-09-10 09:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название книги')),
                ('publication_type', models.CharField(max_length=50, verbose_name='Вид издания')),
                ('number', models.PositiveIntegerField(verbose_name='Номер издания')),
                ('page_count', models.PositiveSmallIntegerField(verbose_name='Количество страниц')),
                ('publication_date', models.DateField(verbose_name='Дата издания')),
                ('description', models.TextField(verbose_name='Описание')),
                ('authors', models.ManyToManyField(max_length=100, to=settings.AUTH_USER_MODEL, verbose_name='Авторы книги')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='BookLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('hall', 'В зале'), ('outside', 'Вне библиотеки')], default='hall', max_length=20, verbose_name='Статус')),
                ('date_moved', models.DateTimeField(auto_now_add=True, verbose_name='Дата перемещения')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book', verbose_name='Книга')),
            ],
            options={
                'verbose_name': 'Местоположение книги',
                'verbose_name_plural': 'Местоположения книг',
            },
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название зала')),
                ('librarian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Библиотекарь')),
            ],
            options={
                'verbose_name': 'Зал',
                'verbose_name_plural': 'Залы',
            },
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер стеллажа')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.hall', verbose_name='Зал')),
            ],
            options={
                'verbose_name': 'Стеллаж',
                'verbose_name_plural': 'Стеллажи',
                'unique_together': {('number', 'hall')},
            },
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрация читателя')),
                ('borrowed_books', models.ManyToManyField(to='library.book')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Читатель',
                'verbose_name_plural': 'Читатели',
            },
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('on_your_hands', 'На руках'), ('returned', 'Возвращена')], default='on_your_hands', max_length=20, verbose_name='Статус')),
                ('date_borrowed', models.DateTimeField(auto_now_add=True, verbose_name='Дата взятия книги')),
                ('date_returned', models.DateTimeField(blank=True, null=True, verbose_name='Дата возвращения книги')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book', verbose_name='Книга')),
                ('book_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.booklocation', verbose_name='Местоположение книги')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.reader', verbose_name='Читатель')),
            ],
            options={
                'verbose_name': 'Аренда',
                'verbose_name_plural': 'Аренды',
            },
        ),
        migrations.CreateModel(
            name='Shelve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер полки')),
                ('rack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.rack', verbose_name='Стеллаж')),
            ],
            options={
                'verbose_name': 'Полка',
                'verbose_name_plural': 'Полки',
                'unique_together': {('number', 'rack')},
            },
        ),
        migrations.AddField(
            model_name='booklocation',
            name='shelve',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.shelve', verbose_name='Полка'),
        ),
        migrations.AddField(
            model_name='book',
            name='shelve',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.shelve', verbose_name='Полка'),
        ),
    ]
