from django import forms
from django.contrib.auth.models import User

from .models import *

class OrderCreationForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label=None, required=False)
    amount = forms.IntegerField(required=False)
    to_delete = forms.ModelChoiceField(queryset=Product.objects.filter(id__in=TempOrder.objects.values('product')), empty_label=None, required=False)
    class Meta:
        model = ProductAmount
        fields = ('product', 'amount')

class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')

class EditOrderForm(forms.Form):
    status = forms.CharField()
    class Meta:
        model = Order
        fields = ('status')

class EditEmployeeForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    position = forms.CharField()
    hourly_rate = forms.DecimalField(max_digits=4, decimal_places=2)
    class Meta:
        model = Employee
        fields = ("first_name", "last_name", "position", "hourly_rate")

class EditIngredientForm(forms.Form):
    name = forms.CharField()
    amount_stored = forms.IntegerField()
    class Meta:
        model = Ingredient
        fields = ("name", "amount_stored")


class RestockIngredientForm(forms.Form):
    amount_to_restock = forms.IntegerField()
    class Meta:
        model = Ingredient
        fields = ('amount_to_restock')