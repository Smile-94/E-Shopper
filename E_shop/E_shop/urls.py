
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from  django.conf import settings
from django.conf.urls.static import static
from.import views
from .views import bikash_payment_view
from admin_app import urls as amdin_app_urls

from app import urls as app_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('master/', views.Master, name='master'),
    path('', views.Index, name='index'),
    path('', include(app_urls)),
    path('', include(amdin_app_urls)),


    path('signup', views.signup,name='signup'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),


    #contct page
    path('contact_us', views.Contact_Page, name='contact_page'),

    #checkout page
    path('checkout/', views.submit_payment_request, name='checkout'),

    #order page
    path('order/', views.Your_Order, name = 'order'),


    #product Page
    path('product/', views.Product_page, name='product'),

    #product_detail
    path('product/<str:id>', views.Product_detail, name='product_detail'),

    path('accounts/', views.Account_details, name='accounts'),

    path('ferthosi/', views.Ferthosi, name='ferthosi'),
    path('payment/', views.payment_view, name='payment'),

    path('bikash-payment/', views.bikash_payment_view, name='bikash_payment'),
    path('payment-request/', views.payment_request_view, name='payment_request'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment-confirmation/', views.payment_confirmation_view, name='payment_confirmation'),
    path('submit-payment-request/', views.submit_payment_request, name='submit_payment_request'),
              ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
