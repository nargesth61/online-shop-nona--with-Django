from typing import Any
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from .cart import CartSession

# Create your views here.
class SessionAddView(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        cart.add_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart": cart.get_cart_dict(),"len_quantity":cart.get_total_quantity()})

class SessionDecreaseView(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        cart.decrease_product(product_id)
        return JsonResponse({"cart": cart.get_cart_dict(),"len_quantity":cart.get_total_quantity()})

class SessionCartSummeryView(TemplateView):
   template_name = "cart/cart-summary.html"

   def get_context_data(self, **kwargs: Any):
       context = super().get_context_data(**kwargs)
       cart = CartSession(self.request.session)
       cart_items = cart.get_cart_items()
       context['cart_items'] = cart_items
       context["total_quantity"] = cart.get_total_quantity()
       context["total_payment_price"] = cart.get_total_payment_amount()
       return context


class SessionUpdateProductCountView(View):
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        if quantity and product_id :
            cart.update_product(product_id,quantity)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart": cart.get_cart_dict(),"len_quantity":cart.get_total_quantity()})

class SessionRemoveProductView(View):
    
    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if product_id :
            cart.remove_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart": cart.get_cart_dict(),"len_quantity":cart.get_total_quantity()})