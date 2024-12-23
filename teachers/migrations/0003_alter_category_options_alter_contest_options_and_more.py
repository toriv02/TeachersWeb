# Generated by Django 5.1.4 on 2024-12-22 11:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_rename_name_subject_наименование'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={'verbose_name': 'Конкурс', 'verbose_name_plural': 'Конкурсы'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Мероприятие', 'verbose_name_plural': 'Мероприятия'},
        ),
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Обратная связь', 'verbose_name_plural': 'Обратная связь'},
        ),
        migrations.AlterModelOptions(
            name='file',
            options={'verbose_name': 'Файл', 'verbose_name_plural': 'Файлы'},
        ),
        migrations.AlterModelOptions(
            name='record',
            options={'verbose_name': 'Публикация', 'verbose_name_plural': 'Публикации'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Рецензия', 'verbose_name_plural': 'Рецензии'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'Предмет', 'verbose_name_plural': 'Предметы'},
        ),
        migrations.RemoveField(
            model_name='subject',
            name='Наименование',
        ),
        migrations.AddField(
            model_name='subject',
            name='name',
            field=models.CharField(default='Не указано', max_length=255, unique=True, verbose_name='Наименование предмета'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Наименование категории'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='end_date',
            field=models.DateField(verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование конкурса'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='rules',
            field=models.TextField(blank=True, null=True, verbose_name='Правила'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='start_date',
            field=models.DateField(verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Место проведения'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование мероприятия'),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на регистрацию'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(verbose_name='Время'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='content',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='moderator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL, verbose_name='Модератор'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='records_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='teachers.record', verbose_name='Публикация'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='uploads/', verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='file',
            name='records_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='teachers.record', verbose_name='Публикация'),
        ),
        migrations.AlterField(
            model_name='record',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации'),
        ),
        migrations.AlterField(
            model_name='record',
            name='author_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя автора'),
        ),
        migrations.AlterField(
            model_name='record',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='teachers.category', verbose_name='Категория публикации'),
        ),
        migrations.AlterField(
            model_name='record',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарии к публикации'),
        ),
        migrations.AlterField(
            model_name='record',
            name='headline',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='record',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Статус публикации'),
        ),
        migrations.AlterField(
            model_name='record',
            name='school',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Школа'),
        ),
        migrations.AlterField(
            model_name='record',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='records', to='teachers.subject', verbose_name='Предмет'),
        ),
        migrations.AlterField(
            model_name='record',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецензии'),
        ),
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='review',
            name='records_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='teachers.record', verbose_name='Публикация'),
        ),
        migrations.AlterField(
            model_name='review',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
    ]