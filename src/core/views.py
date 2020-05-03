from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import OrderItem, Order, Item

class HomeView(ListView):
    model = Item
    template_name = "home-page.html"
    
    
class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

def checkout_page(request):
    return render(request,"checkout-page.html",{})

