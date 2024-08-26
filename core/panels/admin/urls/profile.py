from django.contrib import admin
from django.urls import path,include,re_path
from .. import views

urlpatterns = [
   
    path("security/",views.AdminSecurityEditeView.as_view(),name="security-edit"),
    path("profile/",views.AdminProfileEditeView.as_view(),name="profile-edit"),
    path("profile/image/edit/",views.AdminProfileImageEditView.as_view(),name="profile-image-edit"),
]
