import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=150, verbose_name='Логин', unique=True, blank=False)
    first_name = models.CharField(max_length=150, verbose_name='Имя', blank=False)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', blank=False)
    avatar = models.ImageField(blank=False, null=False, verbose_name='Аватар')


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
