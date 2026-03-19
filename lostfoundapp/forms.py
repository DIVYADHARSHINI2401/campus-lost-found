from django import forms
from .models import Item, Profile

CATEGORY_CHOICES = [
    ('', 'Select a Category'),
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing/Accessories'),
    ('Keys', 'Keys & IDs'),
    ('Books', 'Books & Stationery'),
    ('Jewelry', 'Jewelry & Watches'),
    ('Other', 'Other')
]

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'description', 'location', 'date', 'image', 'item_type', 'contact_email', 'contact_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Calculator'}),
            'category': forms.Select(choices=CATEGORY_CHOICES, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description of the item'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Library'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'item_type': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your-email@college.edu'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number (optional)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('contact_email')
        phone = cleaned_data.get('contact_phone')
        
        if not email and not phone:
            raise forms.ValidationError('Please provide at least one contact method (email or phone).')
            
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_type'].choices = [('lost', 'Lost'), ('found', 'Found')]
        self.fields['item_type'].initial = 'lost'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'college_name', 'department', 'year_of_study', 'phone', 'photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'college_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'College Name'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'year_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Year of Study'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }