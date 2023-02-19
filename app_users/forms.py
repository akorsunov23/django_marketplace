from django.contrib.auth.forms import forms, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = 'username', 'first_name', 'last_name', 'email', 'password1'


class BalanceReplForm(forms.Form):
	balance = forms.IntegerField()
