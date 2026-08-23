import datetime
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Category, Product, Order, OrderItem
from .forms import UserRegistrationForm, UserProfileForm, CheckoutForm
from .cart import Cart

# Home Page View
def home(request):
    featured_products = Product.objects.all().order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'featured_products': featured_products,
        'categories': categories,
    })

# Product Listing View
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    
    if category_id:
        products = products.filter(category_id=category_id)
        
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id and category_id.isdigit() else None,
        'search_query': search_query,
    })

# Product Details View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })

# Cart Page View
def cart_detail(request):
    return render(request, 'store/cart.html')

# Add to Cart View
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.GET.get('qty', 1))
    
    # Check stock
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect('product_detail', product_id=product.id)
        
    cart.add(product=product, quantity=quantity)
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('cart_detail')

# AJAX Cart Update Views
def cart_update_api(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        action = request.POST.get('action') # 'add', 'remove', 'update'
        qty = int(request.POST.get('qty', 1))
        
        product = get_object_or_404(Product, id=product_id)
        
        if action == 'add':
            cart.add(product=product, quantity=qty)
        elif action == 'update':
            cart.add(product=product, quantity=qty, override_quantity=True)
        elif action == 'remove':
            cart.remove(product)
            
        # Recalculate values
        item_qty = 0
        item_subtotal = 0.00
        for item in cart:
            if str(item['product'].id) == str(product_id):
                item_qty = item['quantity']
                item_subtotal = float(item['total_price'])
                break
                
        return JsonResponse({
            'success': True,
            'cart_len': len(cart),
            'item_qty': item_qty,
            'item_subtotal': f"{item_subtotal:.2f}",
            'cart_total': f"{float(cart.get_total_price()):.2f}"
        })
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Checkout View (Requires Login)
@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Add products to checkout.")
        return redirect('product_list')
        
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Verify stock before placing order
            for item in cart:
                prod = item['product']
                qty = item['quantity']
                if prod.stock < qty:
                    messages.error(request, f"Insufficient stock for {prod.name}. Available: {prod.stock}")
                    return render(request, 'store/checkout.html', {'form': form})
            
            # Place order
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            
            # Generate unique order number (e.g. ORD-20260823-12345)
            date_str = datetime.date.today().strftime('%Y%m%d')
            rand_suffix = random.randint(10000, 99999)
            order.order_number = f"ORD-{date_str}-{rand_suffix}"
            order.save()
            
            # Save order items and reduce stock
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                price = item['price']
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                
                # Reduce stock
                product.stock -= quantity
                product.save()
                
            # Clear cart
            cart.clear()
            messages.success(request, "Thank you! Your order has been placed successfully.")
            return redirect('order_confirmation', order_id=order.id)
    else:
        # Prepopulate customer info with user details if available
        initial_data = {
            'customer_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)
        
    return render(request, 'store/checkout.html', {
        'form': form,
    })

# Order Confirmation View
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {
        'order': order,
    })

# Order History View
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {
        'orders': orders,
    })

# User Profile View
@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
        
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'store/profile.html', {
        'form': form,
        'recent_orders': orders,
    })

# User Registration View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save User manually since password needs hashing
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Authenticate and login the new user
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if new_user:
                login(request, new_user)
                messages.success(request, f"Registration successful! Welcome to the store, {new_user.first_name or new_user.username}!")
                return redirect('home')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'store/register.html', {
        'form': form,
    })

# User Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                # Redirect to next parameter if present
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'store/login.html', {
        'form': form,
    })

# User Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
