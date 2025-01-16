from django.shortcuts import render,redirect,get_object_or_404
from cart.cart import Cart
from .forms import NewShippingForm
from .models import NewShippingAddress,Order,OrderItem
from django.contrib import messages
from shop.models import Product
from django.contrib.auth.models import User

def payment_success(request):
    return render(request,'newpayment/payment_success.html', {})

def checkout(request):
    cart=Cart(request)
    cart_products=cart.get_prods()
    quantities=cart.get_quants()
    total=cart.get_total()
    if request.user.is_authenticated:
        shipping_user=NewShippingAddress.objects.get(user__id=request.user.id)
        shipping_form=NewShippingForm(request.POST or None,instance=shipping_user)
        return render(request,'newpayment/checkout.html',{'cart_products':cart_products,'quantities':quantities,'total':total,'shipping_form':shipping_form})
    else:
        shipping_form=NewShippingForm(request.POST or None)
        return render(request,'newpayment/checkout.html',{'cart_products':cart_products,'quantities':quantities,'total':total,'shipping_form':shipping_form})

def confirm_order(request):
    if request.POST:
        cart=Cart(request)
        cart_products=cart.get_prods()
        quantities=cart.get_quants()
        total=cart.get_total()

        user_shipping=request.POST
        request.session['user_shipping']=user_shipping
        return render(request,'newpayment/confirm_order.html',{'cart_products':cart_products,'quantities':quantities,'total':total,'shipping_info':user_shipping})
    #return render(request,'newpayment/confirm_order.html',{})    
    else:
        messages.success(request,'دسترسی به این صفحه امکان پذیر نمیباشد')
        return redirect('home')
    
def process_order(request):
    if request.POST:
        cart=Cart(request)
        cart_products=cart.get_prods()
        quantities=cart.get_quants()
        total=cart.get_total()

        user_shipping=request.session.get('user_shipping')
        #print(user_shipping)
        full_name=user_shipping['new_full_name']
        email=user_shipping['new_email']
        full_address=f'{user_shipping['new_address1']}\n{user_shipping['new_address2']}\n{user_shipping['new_city']}\n{user_shipping['new_state']}\n{user_shipping['new_zipcode']}\n{user_shipping['new_country']}'
        
        if request.user.is_authenticated:
            user=request.user
            new_order=Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=full_address,
                amount_paid=total
            )
            new_order.save()
            
            odr=get_object_or_404(Order,id=new_order.pk)
            for product in cart_products:
                prod=get_object_or_404(Product,id=product.id)
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price
                for k,v in quantities.items():
                    if int(k) == product.id:
                        new_item=OrderItem(
                            order=odr,
                            product=prod,
                            price=price,
                            quantity=v,
                            user=user
                        )
                        new_item.save()

            messages.success(request,'سفارش ثبت شد')
            return redirect('home')
        
        else:
            new_order=Order(
                full_name=full_name,
                email=email,
                shipping_address=full_address,
                amount_paid=total
            )
            new_order.save()

            odr=get_object_or_404(Order,id=new_order.pk)
            for product in cart_products:
                prod=get_object_or_404(Product,id=product.id)
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price
                for k,v in quantities.items():
                    if int(k) == product.id:
                        new_item=OrderItem(
                            order=odr,
                            product=prod,
                            price=price,
                            quantity=v
                        )
                        new_item.save()
            messages.success(request,'سفارش ثبت شد')
            return redirect('home')
    else:
        messages.success(request,'دسترسی به این صفحه امکان پذیر نمی باشد')
        return redirect('home')