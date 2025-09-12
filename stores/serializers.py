from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Store
		fields = "__all__"

