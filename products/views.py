from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from stores.models import Store
from stores.serializers import StoreSerializer
from .models import Product, ProductImages
from .serializers import ProductSerializer


class ProductApi(APIView):
	permission_classes = [permissions.IsAuthenticated]
	parser_classes = [MultiPartParser, FormParser, JSONParser]
	def get(self, request):
		products = Product.objects.all()
		products = ProductSerializer(products, many=True).data
		return Response(products)
	
	def post(self, request):
		data = request.data
		store_id = data.get("store_id")
		title = data.get("title")
		description = data.get("description")
		price = data.get("price")
		images = request.FILES.getlist("images")
		
		if len(images) > 4:
			return Response({"status": False, "message": "So long images"})
		
		if not all([store_id, title, description, price, images]):
			return Response({"status": False, "message": "Invalid datas"})
		
		store = Store.objects.filter(id=store_id).first()
		if not store:
			return Response({"status": False, "message": "Store not found"})
		
		product = Product.objects.create(
		    store=store,
		    title=title,
		    description=description,
		    price=price
		)
		for image in images:
			ProductImages.objects.create(product=product, image=image)
		product = ProductSerializer(product).data
		return Response(product)
	
	def put(self, request):
		product_id = request.data.get("product_id")
		title = request.data.get("title")
		description = request.data.get("description")
		price = request.data.get("price")
		
		store = Store.objects.filter(id=request.user.id).first()
		product = Product.objects.filter(id=product_id, store=store).first()
		if not product:
			return Response({"status": False, "message": "Product not found"})
		
		product.title = title
		product.description = description
		product.price = price
		product.save()
		product = ProductSerializer(product).data
		return Response(product)

		 
	
	
	