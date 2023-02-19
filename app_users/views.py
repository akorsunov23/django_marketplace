from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import F
import logging
from .models import Account
from .forms import RegisterForm, BalanceReplForm


logger = logging.getLogger(__name__)


def register_user(request: HttpRequest, *args, **kwargs) -> HttpResponse:
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			Account.objects.create(
				user=user,
			)
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = RegisterForm()

	context = {
		'form': form
	}

	return render(request, 'app_users/register.html', context=context)


class LoginUserView(LoginView):
	template_name = 'app_users/login.html'

	def form_valid(self, form):
		login(self.request, form.get_user())
		logger.info(f'Пользователь {form.cleaned_data.get("username")} аутентифицировался на сайте')
		return HttpResponseRedirect(self.get_success_url())


class LogoutUserView(LogoutView):
	template_name = 'app_users/logout.html'


def account(request: HttpRequest) -> HttpResponse:
	model = Account.objects.select_related('user').only(
		'user__first_name', 'balance', 'status', 'amount_purchases'
	).get(user=request.user.pk)
	context = {
		'account': model
	}
	return render(request, 'app_users/account.html', context=context)


def balance_repl(request: HttpRequest) -> HttpResponse:
	if request.method == 'POST':
		form = BalanceReplForm(request.POST)
		if form.is_valid():
			balance = form.cleaned_data.get('balance')
			Account.objects.filter(user=request.user.pk).update(balance=F('balance') + balance)
			logger.info(f'Пользователь {request.user.username} пополнил баланс на ${balance}')
			return redirect('users:account')

	else:
		form = BalanceReplForm()

	context = {
		'form': form
	}
	return render(request, 'app_users/balance_replenishment.html', context=context)
