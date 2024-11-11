from email.policy import default

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    '''Профиль Usera'''
    user = models.CharField(max_length=50)
    access = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pay_counts = models.IntegerField(blank=True, default=0)

    def auto_bid(self):
        '''Автоставка'''
        pass

    def payments_count(self):
        '''Считаем кол-во проведённых оплат'''
        pass

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfile'

    def __str__(self):
        return self.user



class Lot(models.Model):
    '''Создание лота'''
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name_lot = models.CharField(max_length=100)
    link_seller = models.URLField(max_length=60)
    address = models.CharField(max_length=40)
    description = models.TextField()
    date_of_create = models.DateTimeField(auto_now_add=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    start_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    end_date_auction = models.DateTimeField()
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='auctionsite/lots_image')

    class Meta:
        verbose_name = 'Lot'
        verbose_name_plural = 'Lot'

    def __str__(self):
        return str(self.id)

class AdminProfile(models.Model):
    '''Создание модели администратора'''
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status_buying = models.BooleanField(default=False)
    active_lot = models.BooleanField(default=True)
    rules = models.CharField(max_length=100, blank=True)
    step_bid = models.IntegerField(blank=True, default=10)
    scheduled_time = models.DateTimeField(blank=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user_name_bid = models.CharField(max_length=100, blank=True)



class AuctionHistory(models.Model):
    '''Создание истории торгов'''
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)


class Ban(models.Model):
    '''Бан'''
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    count_ban = models.IntegerField(default=0)
    def add_ban(self):
        '''Добавление бана по условиям'''
        pass

