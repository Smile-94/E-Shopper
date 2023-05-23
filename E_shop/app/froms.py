from django import forms
from app.models import Profile
from app.models import BillingAddress


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    address_1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address 1'}))
    address_2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address 2'}))
    

    class Meta:
        model = Profile
        exclude = ('user',)


class BillingAddressForm(forms.ModelForm):

    class Meta:
        model = BillingAddress
        exclude = ('user',)