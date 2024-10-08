# Generated by Django 5.1.1 on 2024-10-01 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255, verbose_name='ФИО')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('sex', models.BooleanField(verbose_name='Пол')),
            ],
            options={
                'verbose_name': 'Контрагент',
                'verbose_name_plural': 'Контрагенты',
                'db_table': 'agents',
            },
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biography', models.TextField(blank=True, verbose_name='Биография>')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='lib_models.agents', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
                'db_table': 'authors',
            },
        ),
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
                ('is_borrowed', models.BooleanField(default=False)),
                ('authors', models.ManyToManyField(max_length=100, to='lib_models.agents', verbose_name='Авторы книги')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'db_table': 'book',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='BookLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('hall', 'В зале'), ('outside', 'Вне библиотеки')], default='hall', max_length=20, verbose_name='Статус')),
                ('date_moved', models.DateTimeField(auto_now_add=True, verbose_name='Дата перемещения')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lib_models.book', verbose_name='Книга')),
            ],
            options={
                'verbose_name': 'Местоположение книги',
                'verbose_name_plural': 'Местоположения книг',
                'db_table': 'book_location',
            },
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название зала')),
                ('librarian', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lib_models.agents', verbose_name='Библиотекарь')),
            ],
            options={
                'verbose_name': 'Зал',
                'verbose_name_plural': 'Залы',
                'db_table': 'hall',
            },
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер стеллажа')),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lib_models.hall', verbose_name='Зал')),
            ],
            options={
                'verbose_name': 'Стеллаж',
                'verbose_name_plural': 'Стеллажи',
                'db_table': 'rack',
                'unique_together': {('number', 'hall')},
            },
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрация читателя')),
                ('borrowed_books', models.ManyToManyField(to='lib_models.book')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='lib_models.agents')),
            ],
            options={
                'verbose_name': 'Читатель',
                'verbose_name_plural': 'Читатели',
                'db_table': 'reader',
            },
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('on_your_hands', 'На руках'), ('returned', 'Возвращена')], default='on_your_hands', max_length=20, verbose_name='Статус')),
                ('date_borrowed', models.DateTimeField(auto_now_add=True, verbose_name='Дата взятия книги')),
                ('date_returned', models.DateTimeField(blank=True, null=True, verbose_name='Дата возвращения книги')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lib_models.book', verbose_name='Книга')),
                ('book_location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lib_models.booklocation', verbose_name='Местоположение книги')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lib_models.reader', verbose_name='Читатель')),
            ],
            options={
                'verbose_name': 'Аренда',
                'verbose_name_plural': 'Аренды',
                'db_table': 'borrow',
            },
        ),
        migrations.CreateModel(
            name='Shelve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер полки')),
                ('rack', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lib_models.rack', verbose_name='Стеллаж')),
            ],
            options={
                'verbose_name': 'Полка',
                'verbose_name_plural': 'Полки',
                'db_table': 'shelve',
                'unique_together': {('number', 'rack')},
            },
        ),
        migrations.AddField(
            model_name='booklocation',
            name='shelve',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lib_models.shelve', verbose_name='Полка'),
        ),
        migrations.AddField(
            model_name='book',
            name='shelve',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lib_models.shelve', verbose_name='Полка'),
        ),
    ]
