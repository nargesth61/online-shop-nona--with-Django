from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from decimal import Decimal
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

class ProductStatusType(models.IntegerChoices):
    publish = 1 ,("نمایش")
    draft = 2 ,("عدم نمایش")

class CustomAttribute(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE, related_name='custom_attributes')

    def __str__(self):
        return f"{self.name}: {self.value}"
    

class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

  
class ProductModel(models.Model):
    user = models.ForeignKey("accounts.User",on_delete=models.PROTECT)
    category = models.ManyToManyField(ProductCategoryModel)
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField()
    brief_description = models.TextField(null=True,blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=ProductStatusType.choices,default=ProductStatusType.draft.value)
    discount_percent = models.IntegerField(default=0,validators = [MinValueValidator(0),MaxValueValidator(100)])
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_date"]
    
    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])
        
    def __str__(self):
        return self.title
    
    def get_price(self):        
        discount_amount = self.price * Decimal(self.discount_percent / 100)
        discounted_amount = self.price - discount_amount
        return round(discounted_amount)
    
    def is_discounted(self):
        return self.discount_percent != 0
    
    def is_published(self):
        return self.status == ProductStatusType.publish.value
    
    def get_related_custom_attributes(self):
        return CustomAttribute.objects.filter(product=self)

class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name="product_images")
    file = models.ImageField(upload_to="product_images/")
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_date"]
