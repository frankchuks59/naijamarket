# marketplace/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import SellerProfile, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'category', 'price', 'is_featured', 'is_verified', 'created_at']
    list_filter = ['category', 'is_featured', 'is_verified', 'state']
    search_fields = ['name', 'description', 'seller__username']
    list_editable = ['is_featured', 'is_verified']
    
    # Add custom link to admin dashboard
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_title'] = True
        return super().changelist_view(request, extra_context=extra_context)

# Add admin dashboard link
admin.site.site_header = "NaijaMarket Admin"
admin.site.site_title = "NaijaMarket Admin Portal"
admin.site.index_title = "Welcome to NaijaMarket Administration"
