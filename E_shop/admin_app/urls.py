from django.urls import path


app_name = 'authority'

# Views

from admin_app import manage_order
from admin_app import admin_main

urlpatterns = [
    path('authority/', admin_main.AdminHomeView.as_view(), name='authority'),
    path('logout/', manage_order.UserLogout.as_view(), name='logout'),
    
]

# # manage set menu
# urlpatterns += [
#     path('add-set-menu-food/', manage_foods.AddMenuFoodView.as_view(), name='add_set_menu_food'),
#     path('update-set-menu-food/<int:pk>/', manage_foods.UpdateMenuFoodView.as_view(), name='update_set_menu_food'),
#     path('delete-set-menu-food/<int:pk>/', manage_foods.DeleteMenuFoodView.as_view(), name='delete_set_menu_food'),
#     path('add-set-menu/', manage_foods.AddFoodsView.as_view(), name='add_set_menu'),
#     path('update-set-menu/<int:pk>/', manage_foods.UpdateFoodsView.as_view(), name='update_set_menu'),
#     path('delete-set-menu/<int:pk>/', manage_foods.DeleteFoodsView.as_view(), name='delete_set_menu'),
    
# ]

# # Manage Table
# urlpatterns += [
#     path('table-booking-request/', manage_table.TableBookingRequestListView.as_view(), name='table_bookig_request_list'),
#     path('table-booked-list/', manage_table.TableBookedListView.as_view(), name='table_booked_list'),
#     path('table-booking-details/<int:pk>/', manage_table.TableBookingDetailsView.as_view(), name='table_bookig_details'),
#     path('table-booking-confirm/<int:pk>/', manage_table.ConfirmTableBookingView.as_view(), name='table_bookig_confirm'),
#     path('table-booking-delete/<int:pk>/', manage_table.DelteBookTableView.as_view(), name='table_bookig_delete'),
#     path('table-report/', manage_table.TableReportView.as_view(), name='table_report'),
# ]


# # manage admin settings
# urlpatterns += [
#     path('add-food-category/', admin_settings.AddFoodCategoryView.as_view(), name='add_food_category'),
#     path('update-food-category/<int:pk>/', admin_settings.UpdateFoodCategoryView.as_view(), name='update_food_category'),
#     path('delete-food-category/<int:pk>/', admin_settings.DeleteFoodCategoryView.as_view(), name='delete_food_category'),
#     path('add-shipping-charge/', admin_settings.AddShippingChargeView.as_view(), name='add_shipping_charge'),
#     path('update-shipping-charge/<int:pk>/', admin_settings.UpdateShippingChargeView.as_view(), name='update_shipping_charge'),
#     path('Customer-message/', admin_settings.CustomerMessageView.as_view(), name='customer_message'),
#     path('Customer-message-detail/<int:pk>/', admin_settings.CustomerMessageDetailView.as_view(), name='customer_message_detail'),
# ]

# Manage Order
urlpatterns += [
    path('pending-order-list/', manage_order.PendingListView.as_view(), name='pending_order_list'),
    path('confirmed-order-list/', manage_order.ConfirmedOrderListView.as_view(), name='confirmed_order_list'),
    path('order-details/<int:pk>/',  manage_order.OrderDetailsView.as_view(), name='order_details'),
    path('order-confirm/<int:pk>/',  manage_order.ConfirmOrderView.as_view(), name='order_confirm'),
    path('order-delete/<int:pk>/',  manage_order.DeleteOrderView.as_view(), name='order_delete'),
    path('order-report/',  manage_order.ConfirmedOrderListReportView.as_view(), name='order_report'),
    path('confirm_delevery/<int:pk>/',  manage_order.ConfirmDeleveryView.as_view(), name='confirm_delevery'),
    
]
