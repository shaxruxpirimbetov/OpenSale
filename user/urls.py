from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterApi.as_view()),
    path("change_password/", views.ChangePasswordApi.as_view()),
    path("saved_products/", views.SavedProductApi.as_view()),
    path("get_me/", views.GetMeApi.as_view()),
    path("page/", views.PageApi.as_view()),
    
]