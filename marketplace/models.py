# marketplace/models.py
from django.db import models
from accounts.models import CustomUser

class SellerProfile(models.Model):
    """Seller profile with business information"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)  # City/State
    state = models.CharField(max_length=100, default='Lagos')
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    offers_delivery = models.BooleanField(default=False)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    phone = models.CharField(max_length=15)
    whatsapp = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

class Product(models.Model):
    """Product listing"""
    CATEGORY_CHOICES = [
        ('food-agro', 'Food & Agro'),
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('building', 'Building Materials'),
        ('services', 'Services'),
        ('auto', 'Automobile'),
        ('health', 'Health & Beauty'),
        ('other', 'Other'),
    ]
    
    seller = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='products',
        limit_choices_to={'role__in': ['seller', 'admin']}
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    images = models.JSONField(default=list, blank=True)  # For multiple images
    state = models.CharField(max_length=100, default='Lagos')
    location = models.CharField(max_length=300)
    offers_delivery = models.BooleanField(default=False)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_available = models.BooleanField(default=True)
    
    # Admin flags
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    
    # Tracking
    created_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        related_name='created_products',
        null=True
    )
    updated_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        related_name='updated_products',
        null=True,
        related_query_name='updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def can_edit(self, user):
        """Check if user can edit this product"""
        return user.is_staff or user == self.seller
    
    def can_delete(self, user):
        """Check if user can delete this product"""
        return user.is_staff or user == self.seller