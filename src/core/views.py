from django.shortcuts import render,get_object_or_404,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView,DetailView,View
from django.utils import timezone
from .models import OrderItem, Order, Item
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
            messages.info(request,"This item quantity was updated")
            return redirect('core:order_summary')
        else:
            messages.info(request,"This item was succesfully added to your cart")
            order.items.add(order_item)
            return redirect('core:order_summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This item was succesfully added to your cart")
        return redirect('core:order_summary')



def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request,"This item was succesfully removed to your cart")
            return redirect('core:order_summary')
        else:
            #order does not contain the order item
            messages.info(request,"This item was not present in the cart")
            return redirect('core:product-page',slug=slug)
    else:
        #User does not have a order
        messages.info(request,"you do not have active order")
        return redirect('core:product-page',slug=slug)


def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            if order_item.quantity > 1: 
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            
            messages.info(request,"This item quantity was updated")
            return redirect('core:order_summary')
        else:
            #order does not contain the order item
            messages.info(request,"This item was not present in the cart")
            return redirect('core:order_summary',slug=slug)
    else:
        #User does not have a order
        messages.info(request,"you do not have active order")
        return redirect('core:order_summary',slug=slug)



class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered = False)
            context = { 'object' : order }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"you do not have active order")
            return redirect("/")

        
    


