from django.urls import path

# Views
from app.views import add_to_cart
from app.views import increase_cart_item
from app.views import decrease_cart_item
from app.views import remove_form_cart
from app.views import ChartProductListView
from app.views import check_out
from app.views import payment
from app.views import complete_payment
from app.views import purchase
from app.views import MyOrderListView

app_name = 'app'



# manage order
urlpatterns = [
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart-details/', ChartProductListView.as_view(), name='cart_details'),
    path('remove-from_cart/<int:pk>/', remove_form_cart, name='remove_form_cart'),
    path('increase-from-cart/<int:pk>/', increase_cart_item, name='increase_cart'),
    path('decrease-from-cart/<int:pk>/', decrease_cart_item, name='decrease_cart'),
    # path('my-order/', manage_order.MyOrderListView.as_view(),name="my_order"),
]

urlpatterns += [
    path('checkout/', check_out, name='checkout'),
    path('payment/', payment, name='payment'),
    path('payment-success/', complete_payment, name='payment_success'),
    path('purchase/<val_id>/<tran_id>/', purchase, name='purchase'),
    path('my-order/', MyOrderListView.as_view(),name="my_order"),
]