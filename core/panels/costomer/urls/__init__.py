from django.urls import path,include

app_name = "customer"

urlpatterns = [
    path("",include("panels.customer.urls.addresses")),
]