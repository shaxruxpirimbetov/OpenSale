from rest_framework import serializers
from django.contrib.auth.models import User
from .models import WaitUser


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = "__all__"


class WaitUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = WaitUser
		fields = "__all__"

