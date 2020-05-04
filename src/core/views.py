from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from django.utils import timezone
from .models import OrderItem, Order, Item
from django.contrib import messages
class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"
    
    
class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

def checkout_page(request):
    return render(request,"checkout-page.html",{})

def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item ,created= OrderItem.objects.get_or_create(item=item,user=request.user,ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"This item was succesfully added to your cart")
            return redirect('core:product-page',slug=slug)
        else:
            messages.info(request,"This item was succesfully added to your cart")
            order.items.add(order_item)
            return redirect('core:product-page',slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This item was succesfully added to your cart")
        return redirect('core:product-page',slug=slug)



def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request,"This item was succesfully removed to your cart")
            return redirect('core:product-page',slug=slug)
        else:
            #order does not contain the order item
            messages.info(request,"This item was not present in the cart")
            return redirect('core:product-page',slug=slug)
    else:
        #User does not have a order
        messages.info(request,"you do not have active order")
        return redirect('core:product-page',slug=slug)
    



