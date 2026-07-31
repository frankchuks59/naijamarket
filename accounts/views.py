# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from accounts.forms import RegisterForm, LoginForm

def register(request):
    """User registration with OTP"""
    if request.user.is_authenticated:
        return redirect('marketplace:home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Inactive until OTP verified
            user.save()
            
            # Generate and send OTP
            otp = user.generate_otp()
            
            # Send OTP via email
            send_mail(
                subject='Verify Your NaijaMarket Account',
                message=f'Your OTP code is: {otp}\n\nThis code expires in 5 minutes.\n\nWelcome to NaijaMarket!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            # Store user ID in session for OTP verification
            request.session['otp_user_id'] = user.id
            
            messages.success(request, f'Account created! OTP sent to {user.email}. Check your inbox.')
            return redirect('accounts:verify_otp')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def verify_otp(request):
    """OTP Verification"""
    if request.user.is_authenticated:
        return redirect('marketplace:home')
    
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please register again.')
        return redirect('accounts:register')
    
    from accounts.models import CustomUser
    user = CustomUser.objects.get(id=user_id)
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        
        if user.verify_otp(otp_code):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Email verified successfully! Welcome to NaijaMarket! 🎉')
            
            # Clear session
            del request.session['otp_user_id']
            
            # Redirect sellers to complete profile
            if user.role == 'seller':
                return redirect('accounts:complete_profile')
            return redirect('marketplace:home')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
    
    return render(request, 'accounts/verify_otp.html', {'user': user})

def resend_otp(request):
    """Resend OTP"""
    user_id = request.session.get('otp_user_id')
    if user_id:
        from accounts.models import CustomUser
        user = CustomUser.objects.get(id=user_id)
        otp = user.generate_otp()
        
        send_mail(
            subject='Your New OTP Code - NaijaMarket',
            message=f'Your new OTP code is: {otp}\n\nThis code expires in 5 minutes.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        messages.success(request, 'New OTP sent to your email!')
    
    return redirect('accounts:verify_otp')

def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('marketplace:home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}! 👋')
                return redirect('marketplace:home')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('marketplace:home')

@login_required
def complete_profile(request):
    """Complete seller profile after registration"""
    from marketplace.models import SellerProfile
    
    # Check if profile already exists
    if hasattr(request.user, 'seller_profile'):
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        location = request.POST.get('location')
        state = request.POST.get('state')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        offers_delivery = request.POST.get('offers_delivery') == 'on'
        delivery_fee = request.POST.get('delivery_fee')
        
        SellerProfile.objects.create(
            user=request.user,
            business_name=business_name,
            location=location,
            state=state,
            address=address,
            phone=phone,
            offers_delivery=offers_delivery,
            delivery_fee=delivery_fee or 0
        )
        
        messages.success(request, 'Profile completed! You can now add products.')
        return redirect('accounts:dashboard')
    
    return render(request, 'accounts/complete_profile.html')

@login_required
def dashboard(request):
    """User dashboard"""
    from marketplace.models import Product, SellerProfile
    
    # Get user's products
    user_products = Product.objects.filter(seller=request.user)
    
    # Get seller profile if exists
    seller_profile = None
    if hasattr(request.user, 'seller_profile'):
        seller_profile = request.user.seller_profile
    
    context = {
        'user_products': user_products,
        'seller_profile': seller_profile,
    }
    return render(request, 'accounts/dashboard.html', context)

# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = '/accounts/password-reset-done/'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = '/accounts/password-reset-complete/'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'