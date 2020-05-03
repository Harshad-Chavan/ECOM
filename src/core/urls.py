from django.urls import path
from .views import checkout_page,product_page,HomeView

app_name = 'core'
urlpatterns = [
    path('',HomeView.as_view(),name='home-page'),
    path('products/',product_page,name='product-page'),
    path('checkout/',checkout_page,name='checkout-page')

]