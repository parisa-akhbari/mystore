from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm,UpdateUserForm,UpdatePasswordForm,UpdateUserInfo
from django.db.models import Q
import json
from cart.cart import Cart
from newpayment.forms import NewShippingForm
from newpayment.models import NewShippingAddress

def search(request):
    if request.method == 'POST':
        searched=request.POST['searched']
        #searched=Product.objects.filter(name__icontains=searched)
        searched=Product.objects.filter(Q(name__icontains=searched)|Q(description__icontains=searched))
        if not searched:
            messages.success(request,'چنین محصولی وجود ندارد')
            return render(request,'search.html',{})
        else:
            return render(request, 'search.html', {'searched': searched})  
    return render(request, 'search.html',{})  # Handle GET request

def helloworld(request):
    all_products=Product.objects.all()
    return render(request, 'index.html', {'products':all_products})
    #return HttpResponse(all_products)

def about(request):
    return render(request,'about.html')

def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)

            current_user=Profile.objects.get(user__id=request.user.id)
            saved_cart=current_user.old_cart

            if saved_cart:
                converted_cart=json.loads(saved_cart)
                cart=Cart(request)

                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request,("با موفقیت وارد شدید"))
            return redirect("home")
        else:
            messages.success(request,("مشکلی در لاگین وجود داشت"))
            return redirect("login")
    else:
        return render(request,'login.html')

def logout_user(request):
    logout(request)
    messages.success(request,("با موفقیت خارج شدید"))
    return redirect("home")

def signup_user(request):
    form=SignUpForm()
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid:
            form.save()
            username=form.cleaned_data['username']
            password1=form.cleaned_data['password1']
            user=authenticate(request,username=username,password=password1)
            login(request,user)
            messages.success(request,("اکانت شما ساخته شد"))
            return redirect("update_info")
        else:
            messages.success(request,("مشکلی در ثبت نام شما وجود دارد"))
            return redirect("signup")
    else:
        return render(request,'signup.html',{'form':form})
    
def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        user_form=UpdateUserForm(request.POST or None , instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request,'پروفایل شما ویرایش شد')
            return redirect('home')
        return render(request,'update_user.html',{'user_form':user_form})
    else:
        messages.success(request,'ابتدا لاگین شوید')
        return redirect('home') 

def update_info(request):
    if request.user.is_authenticated:
        #current_user=User.objects.get(id=request.user.id)
        current_user=Profile.objects.get(user__id=request.user.id)
        new_shipping_user=NewShippingAddress.objects.get(user__id=request.user.id)

        form=UpdateUserInfo(request.POST or None , instance=current_user)
        new_shipping_form=NewShippingForm(request.POST or None , instance=new_shipping_user)

        if form.is_valid() or new_shipping_form.is_valid():
            form.save()
            new_shipping_form.save()
            messages.success(request,'اطلاعات کاربری شما ویرایش شد')
            return redirect('home')
        return render(request,'update_info.html',{'form':form, 'new_shipping_form':new_shipping_form })
    else:
        messages.success(request,'ابتدا لاگین شوید')
        return redirect('home')  

def update_password(request):
    if request.user.is_authenticated:
        current_user=request.user

        if request.method=='POST':
            form=UpdatePasswordForm(current_user,request.POST)

            if form.is_valid():
                form.save()
                messages.success(request,'رمز با موفقیت ویرایش شد')
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                   messages.error(request,error)
                return redirect('update_password')
        else:
            form=UpdatePasswordForm(current_user)
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request,'در ابتدا لاگین شوید')
        return redirect('home')
    
def product(request,pk):
    product=Product.objects.get(id=pk)
    similar_products = Product.objects.filter(category=product.category_id).exclude(id=product.id)
    return render(request,'product.html',{'product':product,'similar_products':similar_products})

def category(request,cat):
    cat=cat.replace("-"," ")
    try:
        category=Category.objects.get(name=cat)
        products=Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})
    except:
        messages.success(request,('دسته بندی وجود ندارد'))
        return redirect('home')
    
def category_summary(request):
    all_cat=Category.objects.all()
    return render(request,'category_summary.html',{'category':all_cat})

