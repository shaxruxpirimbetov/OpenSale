from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from rest_framework import permissions
from .funcs import send_code_to_email
from .models import Store
from .serializers import StoreSerializer

from user.models import WaitUser
from user.serializers import WaitUserSerializer


class StoreApi(APIView):
	permission_classes = [permissions.IsAuthenticated]
	parser_classes = [MultiPartParser, JSONParser, FormParser]
	def get(self, request):
		store = Store.objects.filter(seller=request.user).all()
#		if not store:
#			return Response({"status": False, "message": "Store not found"})
		store = StoreSerializer(store, many=True).data
		return Response(store)
	
	def post(self, request):
		data = request.data
		title = data.get("title")
		description = data.get("description")
		code = data.get("code")
		logo = request.FILES.getlist("logo")
		ask_code = data.get("email")
		
		if ask_code:
			code = send_code_to_email(ask_code)
			if not code["status"]:
				return Response({"status": False, "message": "Unknown error", "code": code})
			
			wait_user = WaitUser.objects.filter(user=request.user).first()
			if wait_user:
				wait_user.code = code["code"]
				wait_user.save()
				return Response({"status": True, "message": f"Sended(again) to {ask_code}"})
			WaitUser.objects.create(user=request.user, email=ask_code, code=code["code"])
			return Response({"status": True, "message": f"Sended to {ask_code}"})
		
		if not all([title, description, code]):
			return Response({"status": False, "message": "Invalid datas"})
		
		store = Store.objects.filter(title=title).first()
		my_store = Store.objects.filter(seller=request.user).first()
		if store or my_store:
			return Response({"status": False, "message": "Store already exists"})
		
		wait_user = WaitUser.objects.filter(user=request.user).first()
		if not wait_user:
			return Response({"status": False, "message": "User not found here"})
		
		if not code.isdigit():
			return Response({"status": False, "message": "Code must be integer"})
		
		if int(code) != int(wait_user.code):
			return Response({"status": False, "message": "Code not matches"})
		
		user = User.objects.filter(id=request.user.id).first()
		user.email = wait_user.email
		user.save()
		store = Store.objects.create(seller=request.user, title=title, description=description, logo=logo[0])
		store = StoreSerializer(store).data
		return Response(store)


