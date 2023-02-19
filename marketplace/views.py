from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.db import transaction
from django.core.paginator import Paginator
from app_users.models import Account
import logging
from .models import Product, Basket


logger = logging.getLogger(__name__)


def main_page_view(request: HttpRequest) -> HttpResponse:
	if request.method == 'POST':
		product_id = request.POST.get(key='id_product')

		product = Product.objects.get(pk=product_id)
		user = User.objects.get(pk=request.user.pk)

		Basket.objects.create(
			user=user,
			product=product,
			product_price=product.price
		)

	product = Product.objects.prefetch_related('shop').only('name', 'price', 'shop__name').all()
	paginator = Paginator(object_list=product, per_page=4)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'page_obj': page_obj
	}
	return render(request, 'marketplace/main.html', context=context)


def basket_view(request: HttpRequest) -> HttpResponse:
	basket = Basket.objects.select_related('product').only('product__name', 'product__price').filter(user=request.user.pk)
	order_price = basket.aggregate(order_price=Sum('product_price'))

	if request.method == 'POST':
		balance_user = Account.objects.get(user=request.user.pk).balance

		if balance_user >= order_price.get('order_price'):
			with transaction.atomic():
				Account.objects.filter(user=request.user.pk).update(
					balance=F('balance') - order_price.get('order_price'),
					amount_purchases=F('amount_purchases') + order_price.get('order_price')
				)
				logger.info(f'У {request.user.username} списались баллы (- ${order_price.get("order_price")})')
				for product in basket:
					Product.objects.filter(pk=product.product.pk).update(
						product_count=F('product_count') - 1,
						quantity_sold=F('quantity_sold') + 1
					)
				Basket.objects.filter(user=request.user.pk).delete()
			logger.info(f'{request.user.username} оформил заказ на ${order_price.get("order_price")}')

			status_user = Account.objects.get(user=request.user.pk).status
			amount_purchases = Account.objects.get(user=request.user.pk).amount_purchases
			if status_user != 'advanced user':
				if amount_purchases >= 2000:
					Account.objects.filter(user=request.user.pk).update(status='advanced user')
					logger.info(f'{request.user.username} получил статус "advanced user"')
				elif amount_purchases >= 1000:
					Account.objects.filter(user=request.user.pk).update(status='average user')
					logger.info(f'{request.user.username} получил статус "average user"')

			return redirect('/')
		else:
			return HttpResponse('Insufficient funds!(')

	context = {
		'basket': basket,
		'order_price': order_price.get('order_price')
	}

	return render(request, 'marketplace/basket.html', context=context)


def sales_report(request: HttpRequest) -> HttpResponse:
	products = Product.objects.all().order_by('-quantity_sold')
	context = {
		'products': products,
	}
	return render(request, 'marketplace/sales_report.html', context=context)
