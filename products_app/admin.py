from django.contrib import admin

from .models import CategoryModel, ProductModel, OrderModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    search_fields = ("pk", "name")
    list_display_links = ("name", )


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "current_price", "last_price")
    search_fields = ("pk", "name", "current_price", "last_price")
    list_display_links = ("name", )


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "quantity")
    search_fields = ("pk", "quantity")
