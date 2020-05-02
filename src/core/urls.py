from django.urls import path
from .views import home_page,checkout_page,product_page

app_name = 'core'
urlpatterns = [
    path('',home_page,name='home-page'),
    path('products/',product_page,name='product-page'),
    path('checkout/',checkout_page,name='checkout-page')

]