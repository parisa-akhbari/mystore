from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.db.models.signals import post_save

class NewShippingAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    new_full_name=models.CharField(max_length=250)
    new_email=models.CharField(max_length=300)
    new_address1=models.CharField(max_length=250,blank=True)
    new_address2=models.CharField(max_length=250,blank=True,null=True)
    new_city=models.CharField(max_length=25,blank=True)
    new_state=models.CharField(max_length=25,blank=True ,null=True)
    new_zipcode=models.CharField(max_length=25,blank=True ,null=True)
    new_country=models.CharField(max_length=25,default='IRAN')
    

    class Meta:
        verbose_name_plural='Shipping Address'

    def __str__(self):
        return f'Shipping Address From {self.new_full_name}'
    
def create_shipping_user(sender,instance,created,**kwargs):
    if created:
        user_shipping=NewShippingAddress(user=instance)
        user_shipping.save()

post_save.connect(create_shipping_user,sender=User)
    
class Order(models.Model):
     STATUS_ORDER=[
         ('Pending','در انتظار پرداخت'),
         ('Processing','در حال پردازش'),
         ('Shipped','ارسال شده به پست'),
         ('Delivered','تحویل داده شده')
     ]
     user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
     full_name=models.CharField(max_length=250)
     email=models.EmailField(max_length=300)
     shipping_address=models.TextField(max_length=150000)
     amount_paid=models.DecimalField(decimal_places=0,max_digits=12)
     date_ordered=models.DateTimeField(auto_now_add=True)
     status=models.CharField(max_length=50,choices=STATUS_ORDER,default='Pending')

     def __str__(self):
         return f'Order - {self.id}'
     
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(decimal_places=0,max_digits=12)

    def __str__(self):
        if self.user is not None:
            return f'Order Item - {str(self.id)} - for {self.user}'
        else:
             return f'Order Item - {str(self.id)}'

