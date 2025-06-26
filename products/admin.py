from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "sale_price", "rating", "reviews", "created_at")
    list_filter = ("rating",)
    search_fields = ("name",)
    ordering = ("-created_at",)