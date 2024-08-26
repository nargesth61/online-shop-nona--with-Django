from django.contrib import admin
from django.urls import path,include,re_path
from .. import views

urlpatterns = [
   
    path("products/list/",views.AdminListView.as_view(),name="products-list"),
    path("product/create/",views.AdminProductCreateView.as_view(),name="product-create"),
    path("products/<int:pk>/edit/",views.AdminProsuctsEditView.as_view(),name="product-edit"),
    path("product/<int:pk>/add-image/",views.AdminProductAddImageView.as_view(),name="product-add-image"),
    path("product/<int:pk>/image/<int:image_id>/remove/",views.AdminProductRemoveImageView.as_view(),name="product-remove-image"),
    path('admin/products/<int:pk>/add-attribute/',views.AdminProductAddAttributeView.as_view(), name='product-add-attribute'),
    path('dashboard/admin/products/<int:pk>/remove-attribute/<int:attribute_id>/', views.AdminProductRemoveAttributeView.as_view(), name='product-remove-attribute'),
    ]
