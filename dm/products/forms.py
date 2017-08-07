from django import forms
from .models import Product

class ProductAdd(forms.Form):
    title = forms.CharField(max_length=30)
    description = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10,decimal_places=2)

class ProductModel(forms.ModelForm):
    tags = forms.CharField(label='Related tags', required=False)
    class Meta:
        model = Product
        fields = ["title","description","price","sale_price"]
