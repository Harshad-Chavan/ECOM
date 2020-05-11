from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

Category_choices = (
                    ('S','Shirt'),
                    ('SW','Sport Wear'),
                    ('OW','Out wear'),
                    ('G','Gases'),
                    ('C','Chemicals'),

                )


Label_choices = (
                    ('P','primary'),
                    ('S','secondary'),
                    ('D','danger')

                )

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    category = models.CharField(choices=Category_choices,max_length=2)
    label = models.CharField(choices=Label_choices,max_length=1)
    description = models.TextField()
    image_name = models.CharField(max_length=100)
    availability = models.IntegerField(null=True)
    slug = models.SlugField()
    


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product-page",kwargs={ 'slug': self.slug })


    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart",kwargs={ 'slug': self.slug })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart",kwargs={ 'slug': self.slug })



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_price_difference(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    
class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username