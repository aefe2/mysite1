import datetime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
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
    username = models.CharField(max_length=150, verbose_name='Логин', null=False, unique=True, blank=False)
    first_name = models.CharField(max_length=150, verbose_name='Имя', blank=False)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', blank=False)
    avatar = models.ImageField(upload_to=get_name_file, blank=False,
                               validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp']),
                                           validate_image_size])
    password = models.CharField(max_length=200, verbose_name='Пароль', null=False, blank=False)

    def __str__(self):
        return str(self.username)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
