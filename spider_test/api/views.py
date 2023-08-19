from rest_framework import viewsets, mixins, generics, filters
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


class OrganizationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ Вывод деталей Организации """
    queryset = Organization.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationDetailSerializer

    def get_serializer_class(self):
        """выбор сериализатора в зависимости от применяемого метода"""
        if self.action == 'list':
            return OrganizationListSerializer
        else:
            return OrganizationDetailSerializer


class OrganizationListDistrictView(generics.ListAPIView):
    """ Вывод списка Организаций по Району """
    serializer_class = OrganizationListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        district_id = self.kwargs['district_id']
        category_id = self.request.query_params.get('category_id')

        queryset = Organization.objects.filter(districts__id=district_id)

        if category_id:
            queryset = queryset.filter(items__item__category=category_id).distinct()    # получаем кникальные значения Организаций 

        return queryset
    
    def list(self, request, *args, **kwargs):
        """ переопределение метода для добавления в ответ названия Района """
        response = super().list(request, *args, **kwargs)
        district_name = District.objects.get(id=kwargs['district_id']).name
        response.data = [
            {
                'district_name': district_name,
                'organizations': response.data
            }
        ]
        return response
    

class ItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ GET, POST Товара/Услуги """
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """выбор сериализатора в зависимости от применяемого метода"""
        if self.action == 'create':
            return ItemPostSerializer
        else:
            return ItemSerializer
        
