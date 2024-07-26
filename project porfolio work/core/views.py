from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from store.models import Product, Order, Cart, Bargain, Escrow, OrderItem, Payment, Category
from accounts.models import CustomUser
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from .forms import ProductForm
from random import shuffle
from django.core.paginator import Paginator


def deliveries(request):
    cart_items = Cart.objects.filter(user=request.user)
    orders= Order.objects.filter(delivered=False).prefetch_related('orderitem_set')
    return render(request, 'core/deliveries.html', {'orders': orders, 'cart_items': cart_items })

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Temporarily save the form to get a model instance but don't commit to the database yet
            product.price *= 100  # Modify the price
            product.save()  # Now save the instance to the database
            return redirect('my_shop')
    else:
        form = ProductForm()
        cart_items = Cart.objects.filter(user=request.user)
    
    return render(request, 'core/add_product.html', {'form': form, 'cart_items': cart_items })

def category(request, category):
    if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
    else:
            cart_items =[]
    
    
    category = Category.objects.get(name=category.capitalize())

    products = Product.objects.filter(category=category.id)
    return render(request, 'core/category.html', {'products': products, 'category': category.name , 'cart_items': cart_items })

class Home(View):
    template_name="core/index.html"
    
        
    def get(self, request):
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
        else:
            cart_items =[]
        products = Product.objects.all()
        categories = Category.objects.all()
        # Shuffle the QuerySet to get random products
        products = list(products)
        shuffle(products)

        # Optionally, limit the number of similar products displayed
        products = products[:10]

        return render(request, self.template_name, { 'products' : products, 'cart_items': cart_items, 'categories' : categories})

class MyShop(View):
    template_name="core/my_shop.html"
        
    def get(self, request):
        products = Product.objects.filter(vendor=request.user)
        cart_items = Cart.objects.filter(user=request.user)
        products_paginator = Paginator(products, 10)
        page_num = request.GET.get('page')
        page = products_paginator.get_page(page_num)
        return render(request, self.template_name, { 'cart_items': cart_items, 'page': page })


class Profile(View):
    template_name="core/profile.html"
    
    def get(self, request):
        orders = orders = Order.objects.filter(user=request.user).prefetch_related('orderitem_set')
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, self.template_name, { 'orders' : orders , 'cart_items': cart_items })


class CartView(View):
    template_name="core/cart.html"
    
    def get(self, request):
        user=request.user.id
        cart = Cart.objects.filter(user=user)
        total_price = sum(item.price * item.quantity for item in cart)
        cart_items = Cart.objects.filter(user=request.user)
        print(total_price)
        
        return render(request, self.template_name, { 'cart' : cart, 'total_price': total_price , 'cart_items': cart_items })

    def post(self, request):
        user_id = request.user.id
        total_price = int(request.POST.get('total_price'))
        payment_method = request.POST.get('payment_method')
        cart = Cart.objects.filter(user=user_id)
        cart_items = Cart.objects.filter(user=request.user)
        
        try:
            user = get_object_or_404(CustomUser, id=user_id)
        except:
            error_message = "You need to be logged in to buy an item or bargain"
            return render(request, self.template_name, {'error_message': error_message, 'cart_items': cart_items })
        
        cart = Cart.objects.filter(user=user)

        if payment_method == "pay_on_delivery":
            order = Order.objects.create(user=user, shipping_address="na", total_price=total_price, payment_method="pay_on_delivery")

            for item in cart:
                # create order items for everything in cart
                OrderItem.objects.create(price=item.price, order=order, product=item.product, quantity=item.quantity)
                print(item)
                item.delete()
            
            
        if payment_method == "pay_with_coins":       
            if user.wallet >= total_price:
                
                # Update user's wallet balance (subtract the price)
                print(f"user wallet: {user.wallet}")
                user.wallet -= total_price
                print(f"user wallet: {user.wallet}")
                user.save()

                # Create an order
                order = Order.objects.create(user=user, shipping_address="na", total_price=total_price)

                for item in cart:
                    # create order items for everything in cart
                    OrderItem.objects.create(price=item.price, order=order, product=item.product, quantity=item.quantity)
                    escrow = Escrow.objects.create(buyer=user, vendor=item.product.vendor, amount=item.price, order=order)
                    item.delete()            
            
            # Handle the case where the user doesn't have enough balance
            else:
                
                error_message = "Insufficient wallet balance"
                cart_items = Cart.objects.filter(user=request.user)
                return render(request, self.template_name, { 'cart' : cart, 'error_message': error_message, 'total_price': total_price, 'cart_items': cart_items })

        return redirect("home")

class OrderHistory(View):
    template_name="core/order_history.html"
    # product_ids = Order.objects.values_list('product', flat=True)
    orders = Order.objects.all()
    
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, self.template_name, { 'orders' : self.orders , 'cart_items': cart_items })

class ProductDetail(View):
    template_name="core/product_detail.html"
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
        else:
            cart_items =[]
            
        product = get_object_or_404(Product, id=id)

        # Retrieve all products in the same category, exclude the current product
        similar_products = Product.objects.filter(category=product.category).exclude(id=id)

        # Shuffle the QuerySet to get random products
        similar_products = list(similar_products)
        shuffle(similar_products)

        # Optionally, limit the number of similar products displayed
        similar_products = similar_products[:4]
        
        
        return render(request, self.template_name, { 'product' : product, 'similar_products': similar_products , 'cart_items': cart_items })

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
        else:
            cart_items =[]
        id = kwargs.get('id')
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')
        price = int(request.POST.get('price')) 
        product = get_object_or_404(Product, id=product_id)
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity'))

           # Retrieve all products in the same category, exclude the current product
        similar_products = Product.objects.filter(category=product.category).exclude(id=id)

        # Shuffle the QuerySet to get random products
        similar_products = list(similar_products)
        shuffle(similar_products)

        # Optionally, limit the number of similar products displayed
        similar_products = similar_products[:4]

        print(f"{user_id} {product_id} {price} {action}")
        
        try:
            user = get_object_or_404(CustomUser, id=user_id)
        except:
            error_message = "You need to be logged in to buy an item or bargain"
            return render(request, self.template_name, {'product': product, 'error_message': error_message, 'cart_items': cart_items })
            
        
        if action == "add":
            Cart.objects.create(user=user, price=price, product=product, quantity=quantity)
            success_message = "Item added to cart successfully"
            return render(request, self.template_name, {'product': product, 'similar_products': similar_products, 'success_message': success_message, 'cart_items': cart_items })

        if action == "bargain":
            Bargain.objects.create(user=user, product=product, price=price*100, quantity=quantity)
            success_message = "Bargain created successfully"
            return render(request, self.template_name, {'product': product, 'similar_products': similar_products, 'success_message': success_message, 'cart_items': cart_items })
            
                    
        return render(request, self.template_name, {'product': product, 'error_message': error_message, 'similar_products': similar_products, 'cart_items': cart_items })

class Wallet(View):
    template_name="core/wallet.html"
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        amount = int(request.POST.get('amount')) * 100
        # ref = request.POST.ref
        user = request.user
        payment = Payment.objects.create(amount=amount, user=user)
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, "core/make_payment.html", {'paystack_public_key' : settings.PAYSTACK_PUBLIC_KEY, 'payment' : payment, 'cart_items': cart_items })
        
def verify_payment(request, ref):
    user = request.user
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    
    if verified:
        # Add amount to user wallet
        user.wallet += payment.amount
        user.save()
        messages.success(request, "Verification Successful")
    else:
        messages.error(request, "Verification Failed")
    return redirect("home")
    
class BargainView(View):
    template_name="core/bargains.html"
    
    def get(self, request, *args, **kwargs):
        user = request.user.id
        bargains = Bargain.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, self.template_name, { 'bargains' : bargains , 'cart_items': cart_items })

    def post(self, request, *args, **kwargs):
        bargain_id = request.POST.get('bargain_id')
        bargain = Bargain.objects.get(id=bargain_id)

        if bargain.approved:
            # Add the item to cart
            Cart.objects.create(
                user=bargain.user,
                price=bargain.price,
                product=bargain.product,
                quantity=bargain.quantity
            )
            # Remove the bargain
            bargain.delete()
        return redirect("bargains")

class VendorBargain(View):
    template_name="core/vendor/bargains.html"
    
    def get(self, request, *args, **kwargs):
        user = request.user.id
        bargains = Bargain.objects.filter(product__vendor_id=user)
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, self.template_name, { 'bargains' : bargains , 'cart_items': cart_items })
    
    def post(self, request, *args, **kwargs):
        bargain_id = request.POST.get('bargain_id')
        bargain = Bargain.objects.get(id=bargain_id)
        bargain.approved = True
        bargain.save()
        return redirect("seller_bargains")

def delete_bargain(request, id):
    bargain = Bargain.objects.get(id=id)
    bargain.delete()

    return redirect("seller_bargains")

def delete_cart_item(request, id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    return redirect("cart")


def deliver(request, id):
    order= Order.objects.get(id=id)
    order.status = "DELIVERED"
    order.delivered = True
    order.save()
    return redirect("deliveries")

def search(request):
    if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
    else:
            cart_items =[]
    query = request.GET.get('q')
    products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query)
        )
    products_paginator = Paginator(products, 10)
    page_num = request.GET.get('page')
    
    page = products_paginator.get_page(page_num)
    return render(request, "core/search.html", { 'page' : page, 'query': query , 'cart_items': cart_items })

def receive(request, id):
    order= Order.objects.get(id=id)
    order.received = True
    order.save()
    if order.payment_method=="coins":
        escrow = Escrow.objects.get(order=id)
        escrow.is_paid = True
        vendor = escrow.vendor
        amount = escrow.amount
        user = CustomUser.objects.get(id=vendor.id)
        user.wallet += amount
        escrow.save()
        user.save()
    # Add amount to vendor wallet
    return redirect("profile")

