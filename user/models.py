from django.contrib.auth.models import User
from django.db import models


class WaitUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	code = models.IntegerField()
	email = models.EmailField()
	
	def __str__(self):
		return f"User with {self.email}"
	
	class Meta:
		verbose_name = "Wait user"
		verbose_name_plural = "Wait users"


		