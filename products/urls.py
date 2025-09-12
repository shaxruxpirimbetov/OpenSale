from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductApi.as_view()),
    
]