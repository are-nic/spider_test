from api.models import *
from django.core.management.base import BaseCommand
from django.contrib.postgres.search import TrigramSimilarity

class Command(BaseCommand):
    help = "Fill DB by data"

    def handle(self, *args, **options):
        cat_1 = Category.objects.create(name='Продукты')
        cat_2 = Category.objects.create(name='Инструменты')

        district_1 = District.objects.create(name='Южный район')
        district_2 = District.objects.create(name='Северный район')

        network_1 = Network.objects.create(name='ДомоСтрой')
        network_2 = Network.objects.create(name='Danone')

        company_1 = Organization.objects.create(name='Простоквашино', network=network_2,)
        company_1.districts.add(district_1)
        company_1.districts.add(district_2)
        company_1.save()

        company_2 = Organization.objects.create(name='Nestle', network=network_2)
        company_2.districts.add(district_2)
        company_2.save()

        company_3 = Organization.objects.create(name='Toolsы', network=network_1)
        company_3.districts.add(district_1)
        company_3.districts.add(district_2)
        company_3.save()

        company_4 = Organization.objects.create(name='Мой сад', network=network_1)
        company_4.districts.add(district_1)
        company_4.save()

        item_1 = Item.objects.create(name='Творог', category=cat_1)
        item_2 = Item.objects.create(name='Йогурт', category=cat_1)
        item_3 = Item.objects.create(name='Хлопья', category=cat_1)
        item_4 = Item.objects.create(name='Грабли', category=cat_2)
        item_5 = Item.objects.create(name='Пила', category=cat_2)
        item_6 = Item.objects.create(name='Гвозди', category=cat_2)

        OrganizationItem.objects.create(item=item_1, company=company_1, price=100)
        OrganizationItem.objects.create(item=item_1, company=company_2, price=80)
        OrganizationItem.objects.create(item=item_3, company=company_2, price=150)
        OrganizationItem.objects.create(item=item_4, company=company_4, price=1000)
        OrganizationItem.objects.create(item=item_5, company=company_3, price=300)
        OrganizationItem.objects.create(item=item_6, company=company_3, price=10)