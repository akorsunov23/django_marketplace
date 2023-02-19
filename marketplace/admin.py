from django.contrib import admin
from .models import Product, Shop


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = 'name', 'price', 'product_count'


class ProductInLines(admin.TabularInline):
	model = Product.shop.through


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
	inlines = [
		ProductInLines,
	]
	list_display = 'name',
