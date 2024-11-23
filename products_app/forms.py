from django import forms

from .models import OrderModel


class OrderForm(forms.ModelForm):

    product_id = forms.IntegerField()
    quantity = forms.IntegerField()

    class Meta:
        model = OrderModel
        fields = []
        