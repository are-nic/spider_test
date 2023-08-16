from django.db import models


class District(models.Model):
    name = models.CharField(max_length=250, verbose_name='Район')

    class Meta:
        ordering = ['name']
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'
        db_table = 'districts'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Категория')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'

    def __str__(self):
        return self.name
    

class Network(models.Model):
    name = models.CharField(max_length=250, verbose_name='Сеть')

    class Meta:
        ordering = ['name']
        verbose_name = 'Сеть'
        verbose_name_plural = 'Сети'
        db_table = 'networks'

    def __str__(self):
        return self.name
    

class Company(models.Model):
    name = models.CharField(max_length=250, verbose_name='Компания')
    network = models.ForeignKey(Network, verbose_name='Сеть')
    districts = models.ManyToManyField(District, verbose_name='Районы', related_name='companies')

    class Meta:
        ordering = ['name']
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        db_table = 'companies'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=250, verbose_name='Товар/Услуга')
    companies = models.ManyToManyField(Company, verbose_name='Компании', related_name='items')

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары/Услуги'
        db_table = 'items'


class Price(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    item = models.OneToOneField(Item, verbose_name='Товар/Услуга')
    company = models.OneToOneField(Company, verbose_name='Компания')

    class Meta:
        ordering = ['item']
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        db_table = 'prices'