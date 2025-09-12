from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from stores.models import Store
from stores.serializers import StoreSerializer
from .models import Product
from .serializers import ProductSerializer


class ProductApi(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		store = Store.objects.filter(seller=request.user).first()
		if not store:
			return Response({"status": False, "message": "Store not found"})
		products = Product.objects.filter(store=store).all()
		products = ProductSerializer(products, many=True).data
		store = StoreSerializer(store).data
		return Response({"store": store, "products": products})
	
	def post(self, request):
		return Response({"status": True})
	