from django.contrib.auth.models import User
from django.db import models
from stores.models import Store


class Product(models.Model):
	store = models.ForeignKey(Store, on_delete=models.CASCADE)
	title = models.CharField(max_length=24)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"Product {self.title}"
	
	class Meta:
		verbose_name = "Product"
		verbose_name_plural = "Products"


class ProductImages(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="product_images/")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"Product {self.product.title} image"
	
	class Meta:
		verbose_name = "Product Image"
		verbose_name_plural = "Product Images"
		
