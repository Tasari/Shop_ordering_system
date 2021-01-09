from django import forms

from .models import Product, TempOrder, ProductAmount

class OrderCreationForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label=None, required=False)
    amount = forms.IntegerField(required=False)
    to_delete = forms.ModelChoiceField(queryset=Product.objects.filter(id__in=TempOrder.objects.values('product')), empty_label=None, required=False)
    class Meta:
        model = ProductAmount
        fields = ('product', 'amount')