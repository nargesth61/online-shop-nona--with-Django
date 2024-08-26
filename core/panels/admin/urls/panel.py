from django.urls import path,include,re_path
from .. import views
from django.contrib import admin

urlpatterns = [
    path("home/", views.AdminHomeView.as_view(), name="home"),
]