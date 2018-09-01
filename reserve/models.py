import sys, os
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

sys.path.append('../')
from home.models import User

class Activate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, unique=True)
    expiration_date = models.DateTimeField(blank=True, null=True)

class Artist(models.Model):
    name = models.CharField(max_length=100, verbose_name="アーティスト名", primary_key=True)
    url = models.URLField(blank=True, null=True, verbose_name="ホームページ等URL")
    Twitter = models.CharField(max_length=50, blank=True, null=True, verbose_name="Twitter ID")

    def __str__(self):
        return self.name


class Live(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="公演名")
    artists = models.ManyToManyField(Artist)
    place = models.CharField(max_length=100, blank=True, null=True, verbose_name="会場")
    url = models.URLField(blank=True, null=True, verbose_name="詳細URL")
    date = models.DateField(blank=True, null=True, verbose_name="公演日")
    open_time = models.TimeField(blank=True, null=True, verbose_name="開場")
    start_time = models.TimeField(blank=True, null=True, verbose_name="開演")
    adv = models.IntegerField(default=0, blank=True, null=True, verbose_name="予約料金")
    door = models.IntegerField(default=0, blank=True, null=True, verbose_name="当日料金")
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="公開日時")
    
    def __str__(self):
        return self.name


class Audience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    live = models.ForeignKey(Live, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, verbose_name="お名前")
    ticket = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)] ,null=True, verbose_name="枚数")

    def __str__(self):
        return self.name

    
