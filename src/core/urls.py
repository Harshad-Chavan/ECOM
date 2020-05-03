from django.urls import path
from .views import checkout_page,HomeView,ItemDetailView,add_to_cart

app_name = 'core'
urlpatterns = [
    path('',HomeView.as_view(),name='home-page'),
    path('product/<slug>/',ItemDetailView.as_view(),name='product-page'),
    path('checkout/',checkout_page,name='checkout-page'),
    path('add-to-cart/<slug>',add_to_cart,name='add-to-cart'),

]