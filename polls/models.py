import datetime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from PIL import Image


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5) + '_' + filename])


def validate_image_size(img):
    filesize = img.file.size
    megabyte_max = 2.0
    if filesize > megabyte_max * 1024 * 1024:
        raise ValidationError("Максимальный размер %sMB" % str(megabyte_max))


class User(AbstractUser):
    username = models.CharField(max_length=200, verbose_name='Логин', unique=True, blank=False, validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]+$',
            message='Только латиница и цифры',
            code='invalid_username'
        ),
    ])
    first_name = models.CharField(max_length=200, verbose_name='Имя', blank=False, validators=[
        RegexValidator(
            regex='^[А-Яа-я -]*$',
            message='Только кириллица',
            code='invalid_username'
        ),
    ])
    last_name = models.CharField(max_length=200, verbose_name='Имя', blank=False, validators=[
        RegexValidator(
            regex='^[А-Яа-я -]*$',
            message='Только кириллица',
            code='invalid_username'
        ),
    ])
    avatar = models.ImageField(upload_to=get_name_file, blank=False,
                               validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
                                           validate_image_size])
    password = models.CharField(max_length=200, verbose_name='Пароль', null=False, blank=False)

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ['first_name']

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name) + ' | ' + str(self.username)


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='Текст вопроса')
    short_description = models.CharField(max_length=100, blank=True, verbose_name='Краткое описание')
    full_description = models.CharField(max_length=250, blank=True, verbose_name='Полное описание')
    pub_date = models.DateTimeField('date published')
    question_image = models.ImageField(upload_to=get_name_file, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
        validate_image_size], verbose_name='Изображение')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'Опросы'
        verbose_name_plural = 'Опросы'
        ordering = ['pub_date']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, validators=[
        RegexValidator(), ])
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    voter = models.ForeignKey('User', verbose_name='Пользователь', related_name='+', on_delete=models.CASCADE)
    question_vote = models.ForeignKey(Question, verbose_name='Опрос', on_delete=models.CASCADE)
