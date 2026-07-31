# marketplace/urls.py
from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.home, name='home'),
    path('add-product/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('search/', views.search_products, name='search_products'),
    
    # Admin URLs - Changed prefix to 'manage/' to avoid conflict
    path('manage/products/', views.admin_product_list, name='admin_product_list'),
    path('manage/products/add/', views.admin_add_product, name='admin_add_product'),
    path('manage/products/<int:product_id>/edit/', views.admin_edit_product, name='admin_edit_product'),
    path('manage/products/<int:product_id>/delete/', views.admin_delete_product, name='admin_delete_product'),
    path('manage/products/<int:product_id>/toggle-featured/', views.admin_toggle_featured, name='admin_toggle_featured'),
    path('manage/products/<int:product_id>/toggle-verified/', views.admin_toggle_verified, name='admin_toggle_verified'),
]