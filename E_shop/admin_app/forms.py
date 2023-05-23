from django import forms

from app.models import Order

class ConfirmDeleveryForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('delevery_status',)


class OrderConfirmForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('order_confirm',)