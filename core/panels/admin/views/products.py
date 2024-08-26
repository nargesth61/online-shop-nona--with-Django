from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic import View, TemplateView,UpdateView,ListView,CreateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_views
from ..forms.profile import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from accounts.models import Profile,User
from django.shortcuts import redirect
from django.contrib import messages
from shop.models import ProductModel,ProductCategoryModel,ProductImageModel,CustomAttribute
from django.core.exceptions import FieldError
from ..forms.products import *
from django.shortcuts import get_object_or_404

class AdminListView(LoginRequiredMixin,HasAdminAccessPermission,ListView):
    template_name = "dashboard/admin/products/product-list.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["categories"] = ProductCategoryModel.objects.all()
        return context
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = ProductModel.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
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

class AdminProductCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/products/product-create.html"
    queryset = ProductModel.objects.all()
    form_class = ProductsForm
    success_message = "ایجاد محصول با موفقیت انجام شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse_lazy("dashboard:admin:product-edit", kwargs={"pk": form.instance.pk}))

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:products-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_form"] = ProductImageForm()
        context["attributes_form"] = CustomAttributeForm()
        return context

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Handle adding images
        if 'add_image' in request.POST:
            image_form = ProductImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                image_form.instance.product = self.object
                image_form.save()
                messages.success(request, 'تصویر با موفقیت اضافه شد.')
            else:
                messages.error(request, 'خطا در اضافه کردن تصویر.')
        # Handle adding attributes
        elif 'add_attribute' in request.POST:
            attributes_form = CustomAttributeForm(request.POST)
            if attributes_form.is_valid():
                attributes_form.instance.product = self.object
                attributes_form.save()
                messages.success(request, 'ویژگی با موفقیت اضافه شد.')
            else:
                messages.error(request, 'خطا در اضافه کردن ویژگی.')
        return response
class AdminProsuctsEditView(UpdateView,SuccessMessageMixin,LoginRequiredMixin,HasAdminAccessPermission):
    template_name = "dashboard/admin/products/product-edit.html"
    queryset = ProductModel.objects.all()
    form_class = ProductsForm
    success_message = "بروز رسانی محصول با موفقیت انجام شد"
    
    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-edit", kwargs={"pk": self.get_object().pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image_form"] = ProductImageForm()
        context["atteributes_form"] = CustomAttributeForm() 
        context["custom_attributes"] = self.get_related_custom_attributes()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.product_images.prefetch_related()
        return obj
    
    def get_related_custom_attributes(self):
        return CustomAttribute.objects.filter(product=self.get_object())

class AdminProductAddImageView(LoginRequiredMixin, HasAdminAccessPermission, CreateView):
    http_method_names = ['post']
    form_class = ProductImageForm

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')})

    def get_queryset(self):
        return ProductImageModel.objects.filter(product__id=self.kwargs.get('pk'))

    def form_valid(self, form):
        form.instance.product = ProductModel.objects.get(
            pk=self.kwargs.get('pk'))
        # handle successful form submission
        messages.success(
            self.request, 'تصویر مورد نظر با موفقیت ثبت شد')
        return super().form_valid(form)

    def form_invalid(self, form):
        # handle unsuccessful form submission
        messages.error(
            self.request, 'اشکالی در ارسال تصویر رخ داد لطفا مجدد امتحان نمایید')
        return redirect(reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')}))


class AdminProductRemoveImageView(LoginRequiredMixin,HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    
    http_method_names = ["post"]
    success_message = "تصویر مورد نظر با موفقیت حذف شد"

    def get_queryset(self):
        return ProductImageModel.objects.filter(product__id=self.kwargs.get('pk'))
    
    def get_object(self, queryset=None):
        return self.get_queryset().get(pk=self.kwargs.get('image_id'))

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')})

    def form_invalid(self, form):
        messages.error(
            self.request, 'اشکالی در حذف تصویر رخ داد لطفا مجدد امتحان نمایید')
        return redirect(reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')}))

class AdminProductAddAttributeView(LoginRequiredMixin, HasAdminAccessPermission, CreateView):
    http_method_names = ['post']
    form_class = CustomAttributeForm

    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')})


    def form_valid(self, form):
        form.instance.product = ProductModel.objects.get(pk=self.kwargs.get('pk'))
        messages.success(self.request, 'ویژگی با موفقیت ثبت شد')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'اشکالی در ارسال ویژگی رخ داد لطفا مجدد امتحان نمایید')
        return redirect(reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')}))


class AdminProductRemoveAttributeView(LoginRequiredMixin, HasAdminAccessPermission, DeleteView):
    model = CustomAttribute
    http_method_names = ['post']
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.kwargs.get('pk')})
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.error(request, 'ویژگی مورد نظر پیدا نشد.')
            return redirect(self.get_success_url())
        
        # حذف ویژگی
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'ویژگی با موفقیت حذف شد.')
        return redirect(success_url)

    def get_object(self, queryset=None):
        """
        Overrides the default method to get the object based on 'attribute_id'.
        """
        attribute_id = self.kwargs.get('attribute_id')
        return get_object_or_404(CustomAttribute, id=attribute_id)