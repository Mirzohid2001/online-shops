
import re
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get (self,request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears,'mobiles':mobiles ,'totalitem':totalitem})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
           item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})
@login_required
def add_to_cart(request, pk):
    user=request.user
    product = Product.objects.get(pk=pk)
    Cart(user=user, product=product).save()
    return redirect('showcart')





@login_required
# def show_cart(request):
#     if request.user.is_authenticated:
    
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         amount = 0.0
#         shipping_amount = 70.0
#         total_amount = 0.0
#         cart_product = [p for p in Cart.objects.all() if p.user == user]
#         cart_product.reverse
        
#         if cart_product:
#             for p in cart_product:
#                 tempamount = (p.quantity * p.product.discounted_price)
#                 amount += tempamount
#                 totalamount = amount + shipping_amount
#         if not total_amount:
#             total_amount = 0
   
#         return render(request, 'app/addtocart.html', {'carts':cart,'totalamount':totalamount,'amount':amount})
#     else:
#         redirect('customerregistration')

def show_cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total_price = sum([item.total_cost for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])
    
    return render(request, 'app/addtocart.html', {'cart_items': cart_items, 'total_quantity': total_quantity, 'total_price': total_price})


def delete_item(request, pk):
    Cart.objects.get(pk=pk).delete()
    return redirect('showcart')


def summa(request, pk):
    cart_item = Cart.objects.get(pk=pk)
    print(f"Quyidagi {cart_item} kelyapdi")
    return render(request, 'app/addtocart.html', {'cart_item': cart_item} )

def edit_cart_item(request, pk):
    cart_item = Cart.objects.get(pk=pk)
    action = request.GET.get('action')
    if action == 'minus' and cart_item.quantity > 0:
        if cart_item.quantity == 1:
            cart_item.delete()
            return redirect('showcart')
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('showcart')
    cart_item.quantity += 1
    cart_item.save()
    return redirect('showcart')



 
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
            

        data = {'quantity':c.quantity,'amount':amount,'totalamount':amount + shipping_amount}
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET["prod_id"]
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            data = {'quantity':c.quantity,'amount':amount,'totalamount':amount + shipping_amount}
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
            

            data = {'amount':amount,'totalamount':amount}
        return JsonResponse(data)









def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    print(op)
    return render(request, 'app/orders.html',{'order_placed':op})



def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)

    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def login(request):
 return render(request, 'app/login.html')


class CustomerRegistrationView(View):
    def get(self , request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations !! Registered Successfully')
            form.save()
            return redirect('login')
        return render(request, 'app/customerregistration.html',{'form':form})
         

 
        
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 70
    totalamount = 0.0

    cart_product = [p for p in Cart.objects.all() if  p.user == request.user]
    if cart_product:
        for p in cart_product:
          tempamount = (p.quantity * p.product.discounted_price)
          amount += tempamount
          totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.user
    customer = Customer.objects.get(user=user)
    print(customer)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,product=c.product,quentity=c.quantity).save()
        c.delete()
    return redirect("orders")



@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form,'active':'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer( user=usr, name=name, locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Conratulations!! Profile Updated SuccessFully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

