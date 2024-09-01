from django.urls import path,include
from . import views

app_name = "dashboard"

urlpatterns = [
    path("home/",views.DashboardHomeView.as_view(),name="home"),
   
    path("admin/",include('panels.admin.urls')),
    path("costomer/",include('panels.costomer.urls')),
]
