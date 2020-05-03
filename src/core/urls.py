from django.urls import path
from .views import checkout_page,HomeView,ItemDetailView

app_name = 'core'
urlpatterns = [
    path('',HomeView.as_view(),name='home-page'),
    path('product/<slug>/',ItemDetailView.as_view(),name='product-page'),
    path('checkout/',checkout_page,name='checkout-page')

]