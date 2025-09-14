from django.contrib.auth.models import User
from django.db import models
from products.models import Product


class WaitUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	code = models.IntegerField()
	email = models.EmailField()
	
	def __str__(self):
		return f"User with {self.email}"
	
	class Meta:
		verbose_name = "Wait user"
		verbose_name_plural = "Wait users"


class SavedProduct(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"Saved product {self.product.title}({self.user.username})"
	
	class Meta:
		verbose_name = "Saved product"
		verbose_name_plural = "Saved products"
	

		