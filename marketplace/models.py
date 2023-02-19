from django.db import models
from django.contrib.auth.models import User


class Shop(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	shop = models.ManyToManyField(Shop)
	name = models.CharField(max_length=100, null=False, blank=False)
	price = models.IntegerField(null=False, blank=False)
	product_count = models.IntegerField(null=False, blank=False)
	quantity_sold = models.IntegerField(default=0)

	def __str__(self):
		return f'Name: {self.name}, price: {self.price}'


class Basket(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	product_price = models.IntegerField()



