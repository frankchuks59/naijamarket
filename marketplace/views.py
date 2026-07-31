# marketplace/views.py
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import CustomUser
from marketplace.models import SellerProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from marketplace.models import Product
from marketplace.forms import ProductForm
from django.db import models

def home(request):
    """Home page - shows featured products if available"""
    # Get featured products (or all products if no featured ones)
    featured_products = Product.objects.filter(is_featured=True)[:4]
    
    # If no featured products, show recent products
    if not featured_products:
        featured_products = Product.objects.all()[:4]
    
    context = {
        'featured_products': featured_products,
        'total_products': Product.objects.count(),
    }
    return render(request, 'marketplace/home.html', context)

@login_required
def add_product(request):
    """Add a new product (for sellers and admin)"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.created_by = request.user
            
            # Auto-verify if admin is adding
            if request.user.is_admin:
                product.is_verified = True
            
            product.save()
            
            messages.success(request, f'Product "{product.name}" added successfully! 🎉')
            return redirect('accounts:dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'marketplace/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    """Edit product (only owner or admin)"""
    product = get_object_or_404(Product, id=product_id)
    
    # Check permission
    if not product.can_edit(request.user):
        messages.error(request, 'You do not have permission to edit this product.')
        return redirect('marketplace:home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.updated_by = request.user
            product.save()
            
            messages.success(request, f'Product "{product.name}" updated successfully! ✨')
            return redirect('accounts:dashboard')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'marketplace/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    """Delete product (only owner or admin)"""
    product = get_object_or_404(Product, id=product_id)
    
    # Check permission
    if not product.can_delete(request.user):
        messages.error(request, 'You do not have permission to delete this product.')
        return redirect('marketplace:home')
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully.')
        return redirect('accounts:dashboard')
    
    return render(request, 'marketplace/delete_product.html', {'product': product})

def product_detail(request, product_id):
    """Product detail page"""
    product = get_object_or_404(Product, id=product_id)
    
    # Get similar products
    similar_products = Product.objects.filter(
        category=product.category,
        state=product.state
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'marketplace/product_detail.html', context)

def search_products(request):
    """Search and filter products"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    state = request.GET.get('state', '')
    delivery = request.GET.get('delivery', '')
    
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            models.Q(name__icontains=query) | 
            models.Q(description__icontains=query)
        )
    
    if category:
        products = products.filter(category=category)
    
    if state:
        products = products.filter(state=state)
    
    if delivery == 'yes':
        products = products.filter(offers_delivery=True)
    
    context = {
        'products': products,
        'query': query,
        'category': category,
        'state': state,
        'delivery': delivery,
    }
    return render(request, 'marketplace/search.html', context)
@staff_member_required
def admin_product_list(request):
    """Admin dashboard - view all products"""
    products = Product.objects.all().select_related('seller')
    
    # Filter options
    status = request.GET.get('status', '')
    if status == 'featured':
        products = products.filter(is_featured=True)
    elif status == 'verified':
        products = products.filter(is_verified=True)
    elif status == 'unverified':
        products = products.filter(is_verified=False)
    
    context = {
        'products': products,
        'total_products': Product.objects.count(),
        'featured_count': Product.objects.filter(is_featured=True).count(),
        'verified_count': Product.objects.filter(is_verified=True).count(),
    }
    return render(request, 'marketplace/admin/product_list.html', context)

@staff_member_required
def admin_add_product(request):
    """Admin can add product for any seller"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            
            # Admin can assign product to any seller
            seller_id = request.POST.get('seller')
            if seller_id:
                product.seller = CustomUser.objects.get(id=seller_id)
            else:
                product.seller = request.user
            
            product.created_by = request.user
            product.is_verified = True  # Auto-verify admin products
            product.save()
            
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('marketplace:admin_product_list')
    else:
        form = ProductForm()
    
    sellers = CustomUser.objects.filter(role='seller')
    context = {
        'form': form,
        'sellers': sellers,
        'is_admin': True,
    }
    return render(request, 'marketplace/admin/add_product.html', context)

@staff_member_required
def admin_edit_product(request, product_id):
    """Admin can edit any product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.updated_by = request.user
            
            # Admin can change featured/verified status
            product.is_featured = request.POST.get('is_featured') == 'on'
            product.is_verified = request.POST.get('is_verified') == 'on'
            product.save()
            
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('marketplace:admin_product_list')
    else:
        form = ProductForm(instance=product)
    
    sellers = CustomUser.objects.filter(role='seller')
    context = {
        'form': form,
        'product': product,
        'sellers': sellers,
        'is_admin': True,
    }
    return render(request, 'marketplace/admin/edit_product.html', context)

@staff_member_required
def admin_delete_product(request, product_id):
    """Admin can delete any product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('marketplace:admin_product_list')
    
    context = {'product': product}
    return render(request, 'marketplace/admin/delete_product.html', context)

@staff_member_required
def admin_toggle_featured(request, product_id):
    """Toggle featured status"""
    product = get_object_or_404(Product, id=product_id)
    product.is_featured = not product.is_featured
    product.save()
    
    status = "featured" if product.is_featured else "unfeatured"
    messages.success(request, f'Product {status} successfully!')
    return redirect('marketplace:admin_product_list')

@staff_member_required
def admin_toggle_verified(request, product_id):
    """Toggle verified status"""
    product = get_object_or_404(Product, id=product_id)
    product.is_verified = not product.is_verified
    product.save()
    
    status = "verified" if product.is_verified else "unverified"
    messages.success(request, f'Product {status} successfully!')
    return redirect('marketplace:admin_product_list')