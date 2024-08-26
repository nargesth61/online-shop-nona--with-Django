from django.contrib import admin
from .models import *
from django.contrib.sessions.models import Session

# Register your models here.
class CustomAttributeInline(admin.TabularInline):
    model = CustomAttribute
    extra = 1

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "stock", "status","price","discount_percent", "created_date")
    inlines = [CustomAttributeInline]

@admin.register(ProductCategoryModel)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_date")

@admin.register(ProductImageModel)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_date")



class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
admin.site.register(Session, SessionAdmin)