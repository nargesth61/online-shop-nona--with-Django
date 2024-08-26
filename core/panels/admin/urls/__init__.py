from django.urls import path,include

app_name = "admin"

urlpatterns = [
    path("",include("panels.admin.urls.panel")),
    path("",include("panels.admin.urls.profile")),
    path("",include("panels.admin.urls.products")),
    #path("",include("dashboard.admin.urls.orders")),
    #path("",include("dashboard.admin.urls.reviews")),
    #path("",include("dashboard.admin.urls.newsletters")),
    #path("",include("dashboard.admin.urls.contacts")),
    #path("",include("dashboard.admin.urls.users")),
    #path("",include("dashboard.admin.urls.coupons")),
]