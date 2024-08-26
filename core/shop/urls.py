from django.contrib import admin
from django.urls import path,include,re_path
from .views import  *

app_name = "shop"

urlpatterns = [
    path('product/grid/',ProductListView.as_view(),name="product-grid"),
    re_path(r"product/(?P<slug>[-\w]+)/detail/",ProductdetailView.as_view(),name="product-detail"),
]
