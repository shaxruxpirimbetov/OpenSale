from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, ProductImages


class ProductImagesSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImages
		fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
	images = ProductImagesSerializer(many=True, source="productimages_set")
	class Meta:
		model = Product
		fields = "__all__"


