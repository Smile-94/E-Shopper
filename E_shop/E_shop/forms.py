from django import forms

class PaymentForm(forms.Form):
    cardholder_name = forms.CharField(label='Name')
    card_number = forms.CharField(label='Address')
    expiration_date = forms.CharField(label='Phone NUmber ')
    cvv = forms.CharField(label='Email')

class BikashPaymentForm(forms.Form):
    phone_number = forms.CharField(label='Phone Number')
    pin_number = forms.CharField(label='PIN Number', widget=forms.PasswordInput)


