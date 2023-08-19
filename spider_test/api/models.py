from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class District(models.Model):
    """ Район """
    name = models.CharField(max_length=250, verbose_name='Район')

    class Meta:
        ordering = ['name']
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'
        db_table = 'districts'

    def __str__(self):
        return self.name


class Category(models.Model):
    """ Категория Товаров/Услуг """
    name = models.CharField(max_length=250, verbose_name='Категория')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'

    def __str__(self):
        return self.name
    

class Network(models.Model):
    """ Сеть предприятий """
    name = models.CharField(max_length=250, verbose_name='Сеть')

    class Meta:
        ordering = ['name']
        verbose_name = 'Сеть'
        verbose_name_plural = 'Сети'
        db_table = 'networks'

    def __str__(self):
        return self.name
    

class Organization(models.Model):
    """ Организация """
    name = models.CharField(max_length=250, verbose_name='Компания')
    network = models.ForeignKey(Network, verbose_name='Сеть', on_delete=models.CASCADE)
    districts = models.ManyToManyField(District, verbose_name='Районы', related_name='organizations')

    class Meta:
        ordering = ['name']
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        db_table = 'organizations'

    def __str__(self):
        return self.name


class Item(models.Model):
    """ Товар/Услуга """
    name = models.CharField(max_length=250, verbose_name='Товар/Услуга')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары/Услуги'
        db_table = 'items'

    def __str__(self):
        return self.name


class OrganizationItem(models.Model):
    """ Продукт Организации со своей ценой """
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    item = models.ForeignKey(Item, verbose_name='Товар/Услуга', on_delete=models.CASCADE)
    company = models.ForeignKey(Organization, verbose_name='Компания', on_delete=models.CASCADE, related_name='items')

    class Meta:
        ordering = ['item']
        verbose_name = 'Товар/Услуга компании'
        verbose_name_plural = 'Товары/Услуги компаний'
        db_table = 'organization_items'

    def __str__(self):
        return self.item.name
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """ Создание токена при создании юзера """
    if created:
        Token.objects.create(user=instance)