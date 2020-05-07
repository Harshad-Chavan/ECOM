from django.urls import path
from .views import checkout_page,HomeView,ItemDetailView,add_to_cart,remove_from_cart,OrderSummaryView,remove_single_item_from_cart

app_name = 'core'
urlpatterns = [
    path('',HomeView.as_view(),name='home-page'),
    path('product/<slug>/',ItemDetailView.as_view(),name='product-page'),
    path('checkout/',checkout_page,name='checkout-page'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path('remove_from_cart/<slug>/',remove_from_cart,name='remove-from-cart'),
    path('order_summary/',OrderSummaryView.as_view(),name='order_summary'),
    path('remove_item_from_cart/<slug>/',remove_single_item_from_cart,name='remove-single-item-from-cart'),


    

]