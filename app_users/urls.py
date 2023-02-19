from django.urls import path
from .views import register_user, account, balance_repl, LoginUserView, LogoutUserView


app_name = 'users'

urlpatterns = [
	path('register/', register_user, name='register'),
	path('login/', LoginUserView.as_view(), name='login'),
	path('logout/', LogoutUserView.as_view(), name='logout'),
	path('account/', account, name='account'),
	path('balance/', balance_repl, name='balance'),

]
