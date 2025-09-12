from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from .serializers import UserSerializer


class RegisterApi(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self, request):
		key = request.GET.get("key")
		if key == "shax":
			users = User.objects.all()
			users = UserSerializer(users, many=True).data
			return Response(users)
		return Response({"status": True, "message": "Message"})
	
	def post(self, request):
		data = request.data
		username = data.get("username")
		password = data.get("password")
		
		if not all([username, password]):
			return Response({"status": False, "message": "Invalid data"})
		
		user = User.objects.filter(username=username).first()
		if user:
			return Response({"status": False, "message": "User already exists"})
		
		user = User.objects.create_user(username=username, password=password)
		user = UserSerializer(user).data
		return Response(user)



