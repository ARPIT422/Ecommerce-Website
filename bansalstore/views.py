from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Product,Category,CartItem,Order,OrderItem,Wishlist,UserProfile
from .forms import LoginForm
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    categories = Category.objects.all()
    return render(request,'home2.html',{'categories':categories})

def contact(request):
    return render(request,'Contact page2.html')

def about(request):
    return render(request,'about us2.html')

def registration(request):
    if request.method == "POST":
        username =  request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get("password")
        confirm_password = request.POST.get('confirm_password')
        firstname = request.POST.get('firstname')
        lastname  = request.POST.get('lastname')
        phone_number = request.POST.get('phone_number')
        print(phone_number)
        if password!=confirm_password:
            HttpResponse("Password not same")
        else:
            my_user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
            my_user.save()
            return redirect('login')
    return render(request,'registration.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user_identifier  = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if '@' in user_identifier:
                 try:
                    user = User.objects.get(email=user_identifier)
                    user = authenticate(request, username=user.username, password=password)
                 except User.DoesNotExist:
                     user = None             
            else:
                user = authenticate(request, username=user_identifier, password=password)
            if user is not None:
                auth_login(request, user)
                subject='Welcome to Bansal Store'
                message = f"Hello {user.first_name} {user.last_name}, \n\nWelcome back to Bansal Store. We are thrilled to see you again. As a token of our appreciation, we have prepared an exclusive offer just for you.,\n\nWhether you are looking to upgrade your wardrobe, discover new tech gadgets, or treat yourself to something special, we have got you covered. Explore our latest collections and hottest deals, curated especially for our valued customers like you.,\n\nPlus, do not forget to check out our new arrivals and best-selling products. With our wide range of items, there is always something exciting to discover.,\n\nReady to start shopping? Simply click the button below to unlock your exclusive offer and dive into a world of endless possibilities.\n\nThank you for choosing Bansal Store. We can't wait to see what you'll find!.\n\nHappy shopping!,\n\nWarm regards, \n\nBansal Store Team"

                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message,from_email,recipient_list)
                return redirect('home')
            else:
                form.add_error(None,'Invalid user')
    else:
        form = LoginForm()
    return render(request, 'login2.html', {'form': form})

def LogoutPage(request):
    logout(request)
    return redirect('home')

@login_required
def changepassword(request):
    if request.method =="POST":
        old_password = request.POST.get("currentPassword")
        new_password = request.POST.get("newPassword")
        confirm_password = request.POST.get("confirmPassword")
        user  = authenticate(username=request.user.username,password=old_password)
        if user is None:
            messages.error(request,'The password is incorrect')
        elif new_password != confirm_password:
            messages.error(request,'Current and old Password dont match')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request,request.user)
            messages.success(request,"Password change successfully")
            subject='Password Change'
            message = f'Hello{user.username},\n\n You have successfully Changed your Password,\n\n The new password is{new_password}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message,from_email,recipient_list)
            return redirect('login')
    return render(request,'changepassword.html')


@login_required
def profile(request):
    # Retrieve the user's profile
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        # Retrieve the data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('dob')
        mobile_number = request.POST.get('phone')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile-picture')
        if profile:
            profile.name = name
            profile.email = email
            profile.address = address
            profile.gender = gender
            profile.date_of_birth = date_of_birth
            profile.mobile_number = mobile_number
            profile.bio = bio
            profile.profile_picture = profile_picture
        else:
            profile = UserProfile(user=request.user, name=name, email=email, address=address, gender=gender, date_of_birth=date_of_birth,
                mobile_number=mobile_number, bio=bio, profile_picture=profile_picture)
        profile.save()
        return redirect('profile')
    context = {
        'profile': profile,
    }
    return render(request, 'profile page2.html', context)

def details(request,product_id):
    product=Product.objects.get(id=product_id)
    return render(request,'Product-details3.html',{'product':product})

def cart(request):
    cart_items = CartItem.objects.filter(user = request.user)
    amount = sum(item.product.price*item.qunatity for item in cart_items)
    total_price = amount+40
    return render(request,'cart3.html',{'cart_items':cart_items,'total_price':total_price,"amount":amount})

def add_to_cart(request,product_id):
    product = Product.objects.get(id = product_id)
    cart_item,created =  CartItem.objects.get_or_create(product=product,user=request.user)
    cart_item.qunatity += 1
    cart_item.save()
    return redirect('cart')

def rmv_items_cart(request,item_id):
    cart_item =CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')

def increase_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.qunatity += 1
    cart_item.save()
    return redirect('cart')

def decrease_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.qunatity > 0:
        cart_item.qunatity -= 1
        if cart_item.qunatity == 0:
            cart_item.delete()  # Remove the item if quantity is zero
        else:
            cart_item.save()
    return redirect('cart')

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist2.html', {'wishlist_items': wishlist_items})

@login_required
def move_to_wishlist(request, tp_id):
    cart_item = CartItem.objects.get(id=tp_id)
    Wishlist.objects.create(product=cart_item.product, user=request.user)
    cart_item.delete()
    return redirect('cart')

def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(product=product, user=request.user)
    if created:
        print("Product added to wishlist.")
    else:
        print("Product is already in the wishlist.")
    return redirect('product-details',product_id=product.id)

def rmv_items_wishlist(request,item_id):
    wishlist_item =Wishlist.objects.get(id=item_id)
    wishlist_item.delete()
    return redirect('wishlist')

def add_from_wishlist_to_cart(request,wishlist_item_id):
    wishlist_item = Wishlist.objects.get(id=wishlist_item_id)
    product = wishlist_item.product
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.qunatity += 1
    cart_item.save()
    wishlist_item.delete()
    return redirect('cart')

def place_order(request):
    order = Order(user=request.user,total_amount=0)
    order.save()
    total_amount=0
    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        order_items=OrderItem(order=order, product=item.product, quantity=item.qunatity)
        order_items.save()
        total_amount += item.product.price * item.qunatity
    order.total_amount = total_amount
    order.save()
    cart_items.delete()
    return redirect('order_confirmation',order_id=order.id)
    #return redirect('order_confirmation',order_id=order.id)

def order_confirmation(request,order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order_items = order.items.all()
    return render(request, 'order_confirmation.html', {'order': order,"order_items":order_items})


def category_view(request, category_name):
    category = Category.objects.get(name=category_name)
    brand = request.GET.get('brand')
    products = category.products.all()
    if brand:
        products = products.filter(brand=brand)
    brands = products.values_list('brand', flat=True).distinct()
    print(brands)
    return render(request, 'category_view2.html', {'category': category, 'products': products, 'brands': brands})

def order_history(request):
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        order.items_list = order.items.all()
    context = {
        'orders': orders
    }      
    return render(request, 'order page2.html',context)

@login_required
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id,user=request.user )
    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
        order.items.all().delete()
    return redirect('order_history')

@login_required
def return_order_item(request, order_item_id):
    order_item=OrderItem.get(id=order_item_id)
    if not order_item.is_returned:
        order_item.is_returned = True
        order_item.return_date = timezone.now()
        order_item.save()
        order = order_item.order
        order.total_amount -= order_item.product.price * order_item.quantity
        order.save()
    return redirect('order_history')

def checkout(request):
    cart_items = CartItem.objects.filter(user = request.user)
    amount = sum(item.product.price*item.qunatity for item in cart_items)
    total_price = amount+40
    return render(request,'checkout page.html',{'cart_items':cart_items,'total_price':total_price,"amount":amount})