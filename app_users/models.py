from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	balance = models.IntegerField(default=0)
	status = models.CharField(default='newbie', max_length=50)
	amount_purchases = models.IntegerField(default=0)

	def __str__(self):
		return self.user.username


# class Orders(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.PROTECT)
