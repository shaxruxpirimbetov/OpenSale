from django.contrib.auth.models import User
from django.db import models


class Store(models.Model):
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	logo = models.ImageField(upload_to="logos/")
	title = models.CharField(max_length=24)
	description = models.TextField()
	email = models.EmailField()
	
	def __str__(self, request):
		return f"Store {self.title}"
	
	class Meta:
		verbose_name = "Store"
		verbose_name_plural = "Stores"



