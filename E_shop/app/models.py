from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
      return self.name

class Sub_Category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

    def __str__(self):
      return self.name


class Contact_us(models.Model):
    name= models.CharField(max_length=100)
    email=  models.CharField(max_length=100)
    subject= models.CharField(max_length=100)
    message= models.TextField()

    def __str__(self):
        return self.email

class Brand(models.Model):
    name = models.CharField(max_length= 150)


    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete = models.CASCADE )
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE, null = True)
    image = models.ImageField(upload_to = 'ecommerce/pimg')
    name = models.CharField(max_length= 100)
    price = models.IntegerField()
    date = models.DateField(auto_now_add = True)
    stock = models.IntegerField(default=0)


    def __str__(self):
      return self.name


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required = True, label ='Email', error_messages={'exists': 'This Email Already Exists'})

    class Meta:
        model = User
        fields =('username', 'first_name','last_name','email', 'password1','password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    def save(self, commit =True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user')
    items = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quentity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quentity} X {self.items}"
    
    def get_total(self):
        total = float(self.items.price) * self.quentity
        print(total)
        return "{:.2f}".format(total)

class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    ordered_id = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    payment_id = models.CharField(max_length=250, blank=True, null=True)
    order_id = models.CharField(max_length=250, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    order_confirm = models.BooleanField(default=False)
    ordered_at = models.DateTimeField(null=True)
    confirmed_at =  models.DateTimeField(null=True)
    delevery_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.ordered_id:
            year = str(datetime.date.today().year)[2:4]
            month = str(datetime.date.today().month)
            day = str(datetime.date.today().day)
            self.ordered_id = 'SD'+year+month+day+str(self.pk).zfill(4)
        if self.ordered and not self.ordered_at:
            self.ordered_at = timezone.now()
        
        if self.order_confirm and not self.confirmed_at:
            self.confirmed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}'s orders  "

    def get_totals(self):
        total = 0
        for order_item  in self.orderitems.all():
            total += float(order_item.get_total())
        return total

class PaymentRequest(models.Model):

    phone_number = models.CharField(max_length=20)
    name = models.CharField(max_length=255, default='test name')
    address = models.CharField(max_length=255)
    email = models.EmailField()
    product = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pin = models.CharField(max_length=4)
    is_confirmed = models.BooleanField(default=False)
    list_display = ('address', 'email', 'product')

    def confirm_payment(self, request, queryset):
        # Process the payment confirmation logic
        # Set the payment status as confirmed and any other necessary updates

        # Redirect to the payment success page
        return redirect(reverse('payment_success'))

    confirm_payment.short_description = 'Confirm Payment'

    # Register the custom action in the admin panel
    actions = [confirm_payment]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=264, blank=True)
    last_name = models.CharField(max_length=15, blank=True)
    phone_number = models.CharField(max_length=20, null=True)
    address_1 = models.CharField(max_length=100, null=True)
    address_2 = models.CharField(max_length=100, null=True)
    photo = models.ImageField(upload_to=None, null=True)
    date_of_join = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.first_name+"'s profile"
    
    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]

        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

class ShippingCharge(models.Model):
    shipping_charge = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now_add=True)

class BillingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shipping_address')
    address = models.CharField( max_length=250, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    city  = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=20, blank=True)


    def __str__(self):
        return str(self.user)
    

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]

        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True
    
    class Meta:
        verbose_name_plural = 'Billing Addresses'
