# marketplace/forms.py
from django import forms
from marketplace.models import Product

STATE_CHOICES = [
    ('', 'Select State'),
    ('Lagos', 'Lagos'),
    ('Abuja', 'Abuja'),
    ('Kano', 'Kano'),
    ('Rivers', 'Rivers'),
    ('Oyo', 'Oyo'),
    ('Anambra', 'Anambra'),
    ('Delta', 'Delta'),
    ('Kaduna', 'Kaduna'),
    ('Enugu', 'Enugu'),
    ('Ogun', 'Ogun'),
    ('Imo', 'Imo'),
    ('Kogi', 'Kogi'),
    ('Edo', 'Edo'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Plateau', 'Plateau'),
    ('Benue', 'Benue'),
    ('Niger', 'Niger'),
    ('Bauchi', 'Bauchi'),
    ('Kwara', 'Kwara'),
    ('Sokoto', 'Sokoto'),
    ('Adamawa', 'Adamawa'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Borno', 'Borno'),
    ('Gombe', 'Gombe'),
    ('Zamfara', 'Zamfara'),
    ('Kebbi', 'Kebbi'),
    ('Jigawa', 'Jigawa'),
    ('Katsina', 'Katsina'),
    ('Abia', 'Abia'),
    ('Bayelsa', 'Bayelsa'),
    ('Cross River', 'Cross River'),
    ('Ebonyi', 'Ebonyi'),
    ('Ekiti', 'Ekiti'),
    ('Nasarawa', 'Nasarawa'),
]

class ProductForm(forms.ModelForm):
    """Form for sellers to add products"""
    
    state = forms.ChoiceField(
        choices=STATE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'category',
            'image',
            'state',
            'location',
            'offers_delivery',
            'delivery_fee',
            'stock_available',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Fresh Organic Tomatoes (50kg)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your product in detail...'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 12500'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mile 12 Market, Lagos'
            }),
            'offers_delivery': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'delivery_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 1000'
            }),
            'stock_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Category choices
        self.fields['category'].choices = [
            ('', 'Select Category'),
        ] + list(Product.CATEGORY_CHOICES)