from django.urls import path
from .views import main_page_view, basket_view, sales_report


app_name = 'marketplace'

urlpatterns = [
	path('', main_page_view, name='main'),
	path('basket/', basket_view, name='basket'),
	path('sales_report/', sales_report, name='sales_report'),
]
