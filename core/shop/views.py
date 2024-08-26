from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView
from django.core.paginator import Paginator
from django.contrib.postgres.search import TrigramSimilarity
from .models import *
from django.core.exceptions import FieldError
from cart.cart import *
# Create your views here.

class ProductListView(ListView):
    template_name = 'shop/product-grid.html'  # Your template name
    context_object_name = 'object_list'  # Name used in the template to access the list of products
    paginate_by = 6  # Number of products per page
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        """
        Retrieves a queryset of ProductModel objects based on provided filters.
        Returns:
        Filtered and ordered queryset of ProductModel objects.
        """      
        queryset = ProductModel.objects.filter(
            status=ProductStatusType.publish.value) 
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
            results1 = ProductModel.objects.annotate(similarity=TrigramSimilarity('title', search_q))\
                .filter(similarity__gt=0.1)
            results2 = ProductModel.objects.annotate(similarity=TrigramSimilarity('description', search_q)) \
                .filter(similarity__gt=0.1)
            queryset = (results1 | results2).order_by('-similarity')

        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if category_main_id := self.request.GET.get("category_main_id"):
            queryset = queryset.filter(category__main_type__id=category_main_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass

        return queryset
   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products_count'] = self.get_queryset().count()
        context['categories'] = ProductCategoryModel.objects.all()
        return context


class ProductdetailView(DetailView):
    template_name = 'shop/product-detail.html'
    queryset = ProductModel.objects.filter(
        status=ProductStatusType.publish.value)
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        product = self.get_object()  # Retrieve the product object
        custom_attributes = CustomAttribute.objects.filter(product=product)  # Get custom attributes associated with the product

        context['custom_attributes'] = custom_attributes  # Add custom attributes to the context
        context['product_count'] = cart.count_of_product(product.id)
        return context