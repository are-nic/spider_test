from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.models import *
from api.serializers import *
from django.http import QueryDict


User = get_user_model()


class SpiderApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test', is_staff=True)

    def setUp(self):
        """
        Создать суперпользователя и передать его данные в заголовок запроса API клиента.

        """
        self.client = APIClient()
        self.user = User.objects.get(username='test')
        url_token_auth = reverse('token')
        request_data = {"username": "test", "password": "test"}
        response = self.client.post(url_token_auth, request_data, format='json')
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        self.unauthorized_client = APIClient()

        self.cat_1 = Category.objects.create(name='Продукты')
        self.cat_2 = Category.objects.create(name='Инструменты')

        self.district_1 = District.objects.create(name='Южный район')
        self.district_2 = District.objects.create(name='Северный район')

        network_1 = Network.objects.create(name='ДомоСтрой')
        network_2 = Network.objects.create(name='Danone')

        company_1 = Organization.objects.create(name='Простоквашино', network=network_2,)
        company_1.districts.add(self.district_1)
        company_1.districts.add(self.district_2)
        company_1.save()
        self.company_1 = company_1

        company_2 = Organization.objects.create(name='Nestle', network=network_2)
        company_2.districts.add(self.district_2)
        company_2.save()
        self.company_2 = company_2

        company_3 = Organization.objects.create(name='Toolsы', network=network_1)
        company_3.districts.add(self.district_1)
        company_3.districts.add(self.district_2)
        company_3.save()
        self.company_3 = company_3

        company_4 = Organization.objects.create(name='Мой сад', network=network_1)
        company_4.districts.add(self.district_1)
        company_4.save()
        self.company_4 = company_4

        self.item_1 = Item.objects.create(name='Творог', category=self.cat_1)
        self.item_2 = Item.objects.create(name='Йогурт', category=self.cat_1)
        self.item_3 = Item.objects.create(name='Хлопья', category=self.cat_1)
        self.item_4 = Item.objects.create(name='Грабли', category=self.cat_2)
        self.item_5 = Item.objects.create(name='Пила', category=self.cat_2)
        self.item_6 = Item.objects.create(name='Гвозди', category=self.cat_2)

        OrganizationItem.objects.create(item=self.item_1, company=company_1, price=100)
        OrganizationItem.objects.create(item=self.item_1, company=company_2, price=80)
        OrganizationItem.objects.create(item=self.item_3, company=company_2, price=150)
        OrganizationItem.objects.create(item=self.item_4, company=company_4, price=1000)
        OrganizationItem.objects.create(item=self.item_5, company=company_3, price=300)
        OrganizationItem.objects.create(item=self.item_6, company=company_3, price=10)

    def test_get_districts(self):
        """ Тест получения Районов """
        url = reverse('districts-list')
        response = self.client.get(url)
        serializer_data = DistrictSerializer([self.district_2, self.district_1], many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_organization_list(self):
        """ Тест получения списка всех Организаций """
        url = reverse('organization-list')
        response = self.client.get(url)
        serializer_data = OrganizationListSerializer([self.company_2, self.company_3, self.company_4, self.company_1], many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_organization(self):
        company_id = self.company_1.id

        url = reverse('organization-detail', args=[company_id])

        response = self.client.get(url)
        serializer_data = OrganizationDetailSerializer(self.company_1).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)
        
        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_district_organization_list(self):
        """ Тест получения списка Организаций в определенном районе"""
        district_id = self.district_1.id
        url = reverse('organizations_district-list', args=[district_id])
        response = self.client.get(url)
        serializer_data = OrganizationListSerializer([self.company_3, self.company_4, self.company_1], many=True).data
        serializer_data = [
            {
                "district_name": self.district_1.name,
                "organizations": serializer_data
            }
        ]

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)
        
        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_district_organization_list_by_category_id(self):
        """ Тест получения списка Организаций в определенном районе, используя параметр id Категории Товаров/Услуг """
        district_id = self.district_1.id
        url = reverse('organizations_district-list', args=[district_id])
        query_params = QueryDict(mutable=True)
        query_params['category_id'] = self.cat_1.id
        url_with_category = f'{url}?{query_params.urlencode()}'
        response = self.client.get(url_with_category)
        serializer_data = OrganizationListSerializer([self.company_1], many=True).data
        serializer_data = [
            {
                "district_name": self.district_1.name,
                "organizations": serializer_data
            }
        ]
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)
        
        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_district_organization_list_by_item_seach(self):
        """ Тест получения списка Организаций в определенном районе, используя неточный поиск по Товарам/Услугам """
        district_id = self.district_1.id
        url = reverse('organizations_district-list', args=[district_id])
        query_params = QueryDict(mutable=True)
        query_params['search'] = 'пилы'
        url_with_search = f'{url}?{query_params.urlencode()}'
        response = self.client.get(url_with_search)
        serializer_data = OrganizationListSerializer([self.company_3], many=True).data
        serializer_data = [
            {
                "district_name": self.district_1.name,
                "organizations": serializer_data
            }
        ]
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)
        
        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item_list(self):
        """ Тест получения списка Товаров/Услуг """
        url = reverse('item-list')
        response = self.client.get(url)
        serializer_data = ItemSerializer([self.item_6, self.item_4, self.item_2, self.item_5, self.item_1, self.item_3], many=True).data

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item_detail(self):
        """ Тест получения деталей Товара/Услуги """
        item_id = self.item_3.id
        url = reverse('item-detail', args=[item_id])
        response = self.client.get(url)
        serializer_data = ItemSerializer(self.item_3).data

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_post_item(self):
        """ Тест создания Товара/Услуги """
        item_data = {
              "name": "Пивко",
              "category": self.cat_1.id
        }
        url = reverse('item-list')
        response = self.client.post(url, item_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.unauthorized_client.post(url, item_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)