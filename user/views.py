from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from django.contrib.auth.hashers import make_password
from django.views import View
from django.shortcuts import render
from .serializers import UserSerializer, SavedProductSerializer
from .models import SavedProduct
from products.models import Product
from products.serializers import ProductSerializer
from stores.models import Store
import os


class RegisterApi(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self, request):
		key = request.GET.get("key")
		if key == "shax":
			users = User.objects.all()
			users = UserSerializer(users, many=True).data
			return Response(users)
		
		store = Store.objects.filter(seller=request.user).first()
		if not store:
			return Response({"status": True, "message": "Success", "is_seller": False})
		return Response({"status": True, "message": "Message", "is_seller": True})
	
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
	
	def put(self, request):
		username = request.data.get("username")
		if not username:
			return Response({"status": False, "message": "Invalid datas"})
		
		user = User.objects.filter(username=username).first()
		if user:
			return Response({"status": False, "message": "Username already exists"})
		
		if not request.user.id:
			return Response({"status": False, "message": "Authorization error"})
		
		user = User.objects.filter(id=request.user.id).first()
		user.username = username
		user.save()
		user = UserSerializer(user).data
		return Response(user)


class ChangePasswordApi(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self, request):
		new_password = request.data.get("new_password")
		if not new_password:
			return Response({"status": False, "message": "Invalid datas"})
		
		request.user.password = make_password(new_password)
		request.user.save()
		user = UserSerializer(request.user).data
		return Response(user)


class GetMeApi(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		user = UserSerializer(request.user).data
		store = Store.objects.filter(seller=request.user.id).first()
		user["role"] = "Seller" if store else "Buyer"
		return Response(user)


class SavedProductApi(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		saved_products = SavedProduct.objects.filter(user=request.user).all()
		products = []
		for product in saved_products:
			product = Product.objects.filter(id=product.product_id).first()
			if product:
				products.append(product)
		
		products = ProductSerializer(products, many=True).data
		return Response(products)
	
	def post(self, request):
		product_id = request.data.get("product_id")
		if not product_id:
			return Response({"status": False, "message": "Invalid datas"})
		
		product = Product.objects.filter(id=product_id).first()
		if not product:
			return Response({"status": False, "message": "Product not found"})
		
		saved_product = SavedProduct.objects.filter(user=request.user, product=product).first()
		if saved_product:
			saved_product.delete()
			return Response({"status": True, "message": "Deleted"})
			
		saved_product = SavedProduct.objects.create(user=request.user, product=product)
		saved_product = SavedProductSerializer(saved_product).data
		return Response(saved_product)


class PageApi(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self, request):
		page = ""
		with open("templates/index.html", "r") as f:
			page = f.read()
		# return render(request, "index.html")
		return Response({"status": True, "message": "Page for some", "page": page})
	
	def post(self, request):
		page = request.data.get("page")
		if not page:
			return Response({"status": False, "message": "Page error"})
		
		with open("templates/index.html", "w") as f:
			f.write(str(page))
		
		with open("templates/index.html", "r") as f:
			page = f.read()
		# return render(request, "index.html")
		return Response({"status": True, "message": "Page for some", "page": page})
		
		
