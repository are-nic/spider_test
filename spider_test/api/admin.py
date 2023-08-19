from django.contrib import admin
from .models import *


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'network',
    )


@admin.register(OrganizationItem)
class OrganizationItemAdmin(admin.ModelAdmin):

    list_display = (
        'item',
        'company',
        'price',
    )

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
    )

admin.site.register(District)
admin.site.register(Network)
admin.site.register(Category)