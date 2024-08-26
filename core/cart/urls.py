from django.contrib import admin
from django.urls import path,include,re_path
from .views import  *

app_name = "cart"

urlpatterns = [
path("session/add-product/",SessionAddView.as_view(),name="session-add-product"),
path("session/decrease-product/",SessionDecreaseView.as_view(),name="session-decrease-product"),
path("summery/",SessionCartSummeryView.as_view(),name="cart-summery"),
path("session/remove-product/",SessionRemoveProductView.as_view(),name="session-remove-product"),
path("session/update-product-quantity/",SessionUpdateProductCountView.as_view(),name="session-update-product-quantity"),
]
