from rest_framework import serializers
from .models import *


class DistrictSerializer(serializers.ModelSerializer):
    """ Районы """
    class Meta:
        model = District
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """ Категории Товаров/Услуг """
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    """ Товар/Услуга """
    category = CategorySerializer()
    class Meta:
        model = Item
        fields = '__all__'


class OrganizationItemSerializer(serializers.ModelSerializer):
    """ Товар/Услуга Организации """
    item = ItemSerializer()
    class Meta:
        model = OrganizationItem
        fields = ['id', 'item', 'price']


class ItemPostSerializer(serializers.ModelSerializer):
    """ Товар/Услуга для Добавления """
    class Meta:
        model = Item
        fields = '__all__'


class OrganizationListSerializer(serializers.ModelSerializer):
    """ Список Товаров/Услуг """
    class Meta:
        model = Organization
        fields = ['id', 'name']


class OrganizationDetailSerializer(serializers.ModelSerializer):
    """ Для деталей Организации """
    network = serializers.StringRelatedField()
    districts = serializers.StringRelatedField(many=True)
    items = OrganizationItemSerializer(many=True, read_only=True)
    class Meta:
        model = Organization
        fields = ['id', 'name', 'network', 'districts', 'items']