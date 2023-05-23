from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect

# Packages for python
import requests
import socket
from pysslcmz.payment import SSLCSession
from decimal import Decimal

# Generic Classes
from django.views.generic import TemplateView
from django.views.generic import ListView

# Permission 
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from app.models import Cart
from app.models import Order
from app.models import ShippingCharge
from app.models import Product
from app.models import Profile
from app.models import BillingAddress

# Forms
from app.froms import BillingAddressForm

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, id=pk)

    order_item = Cart.objects.get_or_create(items=item, user=request.user,purchased=False)
    order_qs = Order.objects.filter(user = request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        
        if order.orderitems.filter(items=item).exists():
            order_item[0].quentity +=1
            order_item[0].save()
            return redirect('index')
        else:
            order.orderitems.add(order_item[0])
            return redirect('index')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        return redirect('index')

class ChartProductListView(TemplateView):

    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Cart Page"
        # context["product"] = Product.objects.filter(is_active=True).order_by('-id')[:10]
        context["chart_items"] = Cart.objects.filter(user =self.request.user, purchased = False)
        context["total_items"] = Cart.objects.filter(user =self.request.user, purchased = False).count()
        context["total_price"] =Cart.objects.filter(user=self.request.user, purchased=False).annotate(item_total=F('quentity') * F('items__price')).aggregate(total_price=Sum('item_total'))['total_price'] or 0
        # context["shipping_charge"] =ShippingCharge.objects.latest('id')
        return context

@login_required
def remove_form_cart(request, pk):
    item = get_object_or_404(Product, id = pk)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(items=item).exists():
            order_item = Cart.objects.filter(items=item, user= request.user, purchased=False )[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            return redirect('app:cart_details')
        else:
            return redirect('index')
    else:
        return redirect('index')

@login_required
def increase_cart_item(request, pk):
    item = get_object_or_404(Product, id = pk)
    print("Item: ",item)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        print(order)
        if order.orderitems.filter(items=item).exists():
            order_item = Cart.objects.filter(items=item, user= request.user, purchased=False )[0]
            print("Order Item quentity", order_item)
            if order_item.quentity >= 1:
                order_item.quentity +=1
                order_item.save()
            return redirect('app:cart_details')
        else:
            return redirect('index')
    else:
        return redirect('index')
    
@login_required
def decrease_cart_item(request, pk):
    item = get_object_or_404(Product, id = pk)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(items=item).exists():
            order_item = Cart.objects.filter(items=item, user= request.user, purchased=False )[0]

            if order_item.quentity > 1:
                order_item.quentity -=1
                order_item.save()
                return redirect('app:cart_details')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                return redirect('app:cart_details')
        else:
            return redirect('index')
    else:
        return redirect('index')

class MyOrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'home/my_order.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user, ordered=True).order_by('id')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My order"
        context["shipping_charge"] = ShippingCharge.objects.latest('id')
        return context


@login_required
def check_out(request):
    saved_address = BillingAddress.objects.get_or_create(user = request.user)[0]
    shipping_charges = ShippingCharge.objects.latest("id")
    form = BillingAddressForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingAddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.user = request.user 
            form.save()
            form = BillingAddressForm(instance=saved_address)
    
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    order_items = order_qs[0].orderitems.all()
    total_item = order_qs[0].orderitems.all().count()
    order_total = order_qs[0].get_totals()
    shipping_charge=shipping_charges.shipping_charge
    total_pay = shipping_charge+order_total
           


    return render(request, 'checkout.html', context={'form':form, 'order_items':order_items,'order_total':order_total, 'total_item':total_item, 'saved_address': saved_address,'total_pay':total_pay,'shipping_charge':shipping_charge})


@login_required
def payment(request):

    saved_address = BillingAddress.objects.get_or_create(user = request.user)[0]

    if not saved_address.is_fully_filled():
        messages.info(request, "Please complete your shipping address")
        return redirect('app:checkout')

    if not request.user.profile.is_fully_filled():
        messages.info(request, "Please complete your profile information.")
        return redirect('home:edit_profile', request.user.id)


    status_url = request.build_absolute_uri(reverse('app:payment_success'))
    print(status_url)
    shipping_charge = ShippingCharge.objects.latest('id')
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_items_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()+shipping_charge.shipping_charge

    current_user = request.user
    full_name = str(current_user.profile.first_name+" "+current_user.profile.last_name)
    print(full_name)

    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id='sizzl64456beb762af', sslc_store_pass='sizzl64456beb762af@ssl')

    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='food', product_name=order_items, num_of_item=order_items_count, shipping_method='YES', product_profile='None')

    mypayment.set_customer_info(name=full_name, email=current_user.email, address1=current_user.profile.address_1, address2=current_user.profile.address_1, city='Dhaka', postcode='1230', country='Bangladesh', phone=current_user.profile.phone_number)

    mypayment.set_shipping_info(shipping_to=full_name, address=saved_address.address, city=saved_address.city, postcode=saved_address.zip_code, country=saved_address.country)

    response_data = mypayment.init_payment()
    print(response_data)

    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete_payment(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data= request.POST
    
        payment_status = payment_data['status']
        
        if payment_status == 'VALID':
            transaction_id = payment_data['tran_id']
            bank_tran_id = payment_data['bank_tran_id']
            messages.success(request, "Your payment completed Successfully")
            
            return HttpResponseRedirect(reverse('app:purchase', kwargs={'val_id':bank_tran_id,'tran_id':transaction_id}))
        
        elif payment_status == 'FAILD':
            messages.warning(request, "Your payment Faild, please try again!")
            return HttpResponseRedirect(reverse('app:checkout'))
        
        else:
            messages.warning(request, "Your payment Faild, please try again!")
            return HttpResponseRedirect(reverse('app:checkout'))
    
    return render(request, 'payment/payment_success.html', context={})


@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)[0]
    order_qs.order_id = val_id
    order_qs.payment_id = tran_id
    order_qs.ordered = True
    order_qs.payment_status = True
    order_qs.save()

    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()

    # return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('app:my_order'))

class MyOrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user, ordered=True).order_by('id')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My order"
        context["shipping_charge"] = ShippingCharge.objects.latest('id')
        return context