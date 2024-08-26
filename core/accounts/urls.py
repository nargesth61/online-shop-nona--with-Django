from django.contrib import admin
from django.urls import path,include
from .views import  *

app_name = "accounts"

urlpatterns = [
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('register/',register, name='register'),
    path('verify/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
]
