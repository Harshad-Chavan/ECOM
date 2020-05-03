from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import OrderItem, Order, Item

class HomeView(ListView):
    model = Item
    template_name = "home-page.html"
    
    

def checkout_page(request):
    return render(request,"checkout-page.html",{})

def product_page(request):
    return render(request,"product-page.html",{})