from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


User = settings.AUTH_USER_MODEL



class Subject(models.Model):
    """Модель для предметов (информатика, математика, русский язык и тд)"""
    name = models.CharField(max_length=255,unique=True, verbose_name="Наименование предмета",default="Не указано")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")

    class Meta:
        verbose_name = "Школа"
        verbose_name_plural = "Школы"

    def __str__(self):
        return self.name


class CustmoUser(AbstractUser):
        fio = models.CharField(max_length=255, verbose_name="ФИО",null=True)
        school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers', verbose_name="Школа",null=True)

        groups = models.ManyToManyField(
            'auth.Group',
            verbose_name='groups',
            blank=True,
            help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
            related_name="custom_user_set",
            related_query_name="custom_user",
        )
        user_permissions = models.ManyToManyField(
            'auth.Permission',
            verbose_name='user permissions',
            blank=True,
            null=True,
            help_text='Specific permissions for this user.',
            related_name="custom_user_set",
            related_query_name="custom_user",
        )

class Record(models.Model):
    """Модель для публикации (методические материалы, нормативные документы)"""
    headline = models.CharField(max_length=255, verbose_name="Заголовок")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарии к публикации")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время публикации")
    author = models.ForeignKey(CustmoUser, on_delete=models.CASCADE, related_name='records',null=True,verbose_name="Автор публикации")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='records', blank=True, null=True, verbose_name="Предмет")
    is_published = models.BooleanField(default=False, verbose_name="Статус публикации")  

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.headline


class File(models.Model):
    """Модель для файлов, прикрепленных к публикации"""
    records_FK = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='files', verbose_name="Публикация")
    file = models.FileField(upload_to='uploads/', verbose_name="Файл") 

    class Meta:
       verbose_name = "Файл"
       verbose_name_plural = "Файлы"


class Feedback(models.Model):
    """Модель для обратной связи (комментарии модератора)"""
    content = models.TextField(verbose_name="Содержание")
    records_FK = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='feedbacks',null=True, verbose_name="Публикация")
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks',null=True, verbose_name="Модератор")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"


class Review(models.Model):
    """Модель для рецензий учителей"""
    content = models.TextField(verbose_name="Содержание")
    records_FK = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='reviews',null=True, verbose_name="Публикация")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', null=True, verbose_name="Автор рецензии")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"


class Document(models.Model):
    """Модель для нормативных документов"""
    headline = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    ref = models.TextField(verbose_name="Ссылка")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Нормативный документ"
        verbose_name_plural = "Нормативные документы"
"""  
class Event(models.Model):
    #Модель для мероприятий
    name=models.CharField(max_length=255, verbose_name="Наименование мероприятия")
    description=models.TextField(blank=True, null=True, verbose_name="Описание")
    date=models.DateField(verbose_name="Дата")
    time=models.TimeField(verbose_name="Время")
    location = models.CharField(max_length=500, blank=True, null=True, verbose_name="Место проведения")
    registration_link = models.URLField(blank=True,null=True, verbose_name="Ссылка на регистрацию")

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
    
class Contest(models.Model):
    #Модель для конкурсов
    name=models.CharField(max_length=255, verbose_name="Наименование конкурса")
    description=models.TextField(blank=True, null=True, verbose_name="Описание")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    rules = models.TextField(blank=True,null=True, verbose_name="Правила")

    class Meta:
       verbose_name = "Конкурс"
       verbose_name_plural = "Конкурсы"
"""