from django.shortcuts import render, redirect, HttpResponse
from app.models import Category, Product,Contact_us, Order,Brand
from .forms import PaymentForm
from django.core.mail import send_mail
from .forms import BikashPaymentForm
from django.contrib.auth import authenticate,login
from app.models import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from app.models import Cart
from app.models import PaymentRequest

import stripe

stripe.api_key = "sk_test_51Lx8w7FIEDXjR5hTWLXSDlj3WXjJ9S8MFzUkn7j5ryXjACD2wnrsqtS5PRgteBsqsHEaolhg2q8O6b1N2li2x7th00tyRQzOf2"


def Master(request):
    return render(request,'master.html')


def Index(request):
   category = Category.objects.all()
   products = Product.objects.all()
   brand = Brand.objects.all()
   brandID = request.GET.get('brand')
#    total_items = Cart.objects.filter(user =request.user, purchased = False).count()

   categoryID = request.GET.get('category')


   if categoryID:
    products = Product.objects.filter(sub_category = categoryID).order_by('-id')

   elif brandID:
    products = Product.objects.filter(brand =brandID).order_by('-id')

   else:
       products = Product.objects.all()

   searched_text = request.GET.get('searched_text')
   if searched_text:
       products = products.filter(name__contains=searched_text)



   context = {
       'category': category,
       'products': products,
       'brand': brand,
    #    'total_items':total_items,
   }
   return render(request, 'index.html',context)





def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password =form.cleaned_data['password1'],

            )
            new_user.first_name= form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            login(request,new_user)
            return redirect('index')
    else:
        form = UserCreateForm()

    context ={
        'form': form,
    }
    return render(request,'registration/signup.html',context )

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    # cart = Cart(request)
    session = request.session
    

    return render(request, 'cart/cart_detail.html')


def Contact_Page(request):
    if request.method == 'POST':
        contact = Contact_us(
           name = request.POST.get('name'),
           email= request.POST.get('email'),
           subject=request.POST.get('subject'),
           message =request.POST.get('message'),
        )
        contact.save()

    return render(request, 'contact.html')
def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)

    order = Order.objects.filter(user = user)
    context = {
        'order': order,
    }
    return render(request, 'order.html', context)

def CheckOut(request):
    if request.method == "POST":

        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk = uid)
        print(cart)


        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a*b

            order = Order(
                user = user,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                address = address,
                phone = phone,
                pincode = pincode,
                total = total,


            )
            order.save()
        request.session['cart'] = { }
        return redirect('index')
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order = Order.objects.filter(user=user)

    context={

        'order':order,
        'user':user,
    }

    return render(request, 'checkout.html', context)




def Product_page(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')

    categoryID = request.GET.get('category')

    if categoryID:
        products = Product.objects.filter(sub_category=categoryID).order_by('-id')

    elif brandID:
        products = Product.objects.filter(brand=brandID).order_by('-id')

    else:
        product = Product.objects.all()


    context={
        'category': category,
        'brand': brand,
        'product': product,
    }




    return render(request, 'product.html', context)



def Product_detail(request,id):
    product = Product.objects.filter( id = id ).first()
    brand = Brand.objects.all()

    print('seg')
    print(product.name)
    context={
        'product' : product,
        'brand': brand,
    }
    return render(request, 'product_detail.html', context)

@login_required(login_url="/accounts/login/")
def Account_details(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)

    order = Order.objects.filter(user=user)
    context = {
        'order': order,

    }

    return render(request, 'account_detail.html', context)


def Ferthosi(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff is True:
            login(request, user)
            return redirect('authority:authority')

        elif user is not None:
            login(request, user)

            return redirect('index')
        else:
            return render(request, 'ferthosi.html', {'username': username, 'password': password, 'error': True})
    else:
        return render(request, 'ferthosi.html')




# my custom edits to the project



def paysuccess(request):
    return render(request, "success.html")


def checkout(request):
    if request.method == 'POST':
        # Retrieve form data
        name=request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        # Create a PaymentRequest instance
        payment_request = PaymentRequest.objects.create(email=email, address=address)

        # Update the email and address fields of the PaymentRequest instance
        payment_request.email = email
        payment_request.address = address
        payment_request.save()

        # Redirect or render a success message

    return render(request, 'checkout.html')

def submit_payment_request(request):
    if request.method == 'POST':
        # Retrieve the values from the request's POST data
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        request.session['name'] = name
        request.session['address'] = address
        request.session['email'] = email

        # print(name, email, address)
        # payment_request = PaymentRequest( address=address, email=email)
        # payment_request.save()

        # Redirect to the bikash_payment page
        return redirect('bikash_payment')# Redirect to the payment confirmation page

    return render(request, 'checkout.html')


def payment_view(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if payment_method == 'online_payment':
            # Redirect to the online payment page
            return redirect('online_payment')
        elif payment_method == 'pay_after_receiving':
            # Perform pay after receiving logic
            # ...
            return redirect('payment_success')

    return render(request, 'payment.html')


def bikash_payment_view(request):
    if request.method == 'POST':
        form = BikashPaymentForm(request.POST)

        if form.is_valid():
            # Process the form data and perform necessary actions

            return redirect('payment_confirmation')  # Redirect to the payment confirmation page

        # If the form is not valid, you can render the form again with the validation errors
        return render(request, 'bikash_payment.html', {'form': form})

    # If the request is GET, render the form initially
    form = BikashPaymentForm()
    return render(request, 'bikash_payment.html', {'form': form})

def payment_request_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        pin = request.POST.get('pin')
        amount = request.POST.get('amount')
        name = request.session['name']
        email = request.session['email']
        address = request.session['address']

        # Check if all the required fields are present
        if phone_number and pin and amount:
            # Create a payment request object
            payment_request = PaymentRequest.objects.create(
                phone_number=phone_number,
                pin=pin,
                amount=amount,
                name=name,
                email=email,
                address=address
            )

            # Process the payment request, e.g., send it to the admin panel

            return redirect('payment_confirmation')  # Redirect to the payment confirmation page
        else:
            # Handle the scenario where one or more required fields are missing
            error_message = 'Please provide all the required information.'
            return render(request, 'bikash_payment.html', {'error_message': error_message})

    # Handle GET request or other cases
    return render(request, 'bikash_payment.html')# payment page if there's an error or unauthorized access

def payment_success(request):
    # Retrieve the necessary data for the invoice (user name, phone, amount, address, email)
    user = request.user
    # Retrieve other relevant data as needed

    # Pass the data to the template
    context = {
        'user': user,
        # Pass other relevant data as needed
    }

    return render(request, 'payment_success.html', context)

def payment_confirmation_view(request):
    # Add any necessary logic here
    return render(request, 'payment_confirmation.html')