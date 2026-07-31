# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Super Admin'),
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    # OTP Fields
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_seller(self):
        return self.role == 'seller'
    
    def generate_otp(self):
        """Generate 6-digit OTP"""
        self.otp_code = str(random.randint(100000, 999999))
        from django.utils import timezone
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp_code
    
    def verify_otp(self, code):
        """Verify OTP code"""
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.otp_code:
            return False
        
        # Check if OTP is expired (5 minutes)
        if self.otp_created_at and timezone.now() > self.otp_created_at + timedelta(minutes=5):
            self.otp_code = None
            self.save()
            return False
        
        # Check if code matches
        if self.otp_code == code:
            self.otp_verified = True
            self.otp_code = None
            self.save()
            return True
        
        return False