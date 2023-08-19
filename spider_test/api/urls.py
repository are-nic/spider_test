from rest_framework.routers import SimpleRouter
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

router = SimpleRouter(trailing_slash=False)
router.register('organization', OrganizationViewSet, basename='organization')
router.register('item', ItemViewSet, basename='item')

urlpatterns = [
    path('token/', obtain_auth_token, name='token'),
    path('organizations/<int:district_id>/', OrganizationListDistrictView.as_view(), name='organizations_district-list'),
]
urlpatterns += router.urls