from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse, HttpResponse
from .forms import BillingDetailsForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def home(request):
    products = Product.objects.all()
    products_baby = Product.objects.filter(category='Baby')[:4]  
    products_diy_tools = Product.objects.filter(category='DIY & Tools')[:4]  
    context = {
        'products': products,
        'products_baby': products_baby,
        'products_diy_tools': products_diy_tools,
    }
    return render(request, 'myapp/home.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_images = ProductImage.objects.filter(product=product)
    category_products = Product.objects.filter(category=product.category)[:8]
    return render(request, 'myapp/product_detail.html', {'product': product, 'product_images': product_images, 'category_products': category_products})

def category_products(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'myapp/category_products.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    
    return redirect('cart_view')

def cart_view(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        if cart:
            products_in_cart = cart.products.all()
            total_products_in_cart = products_in_cart.count()
            total_price = sum(product.price for product in products_in_cart)
        else:
            products_in_cart = []
            total_products_in_cart = 0
            total_price = 0

        return render(request, 'myapp/cart.html', {
            'products_in_cart': products_in_cart,
            'total_products_in_cart': total_products_in_cart,
            'total_price': total_price
        })
    else:
        return redirect('account_login')  # Redirect unauthenticated users to login page


def get_cart_details(request):
    # Logic to fetch total_products and total_price from the cart
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    if cart:
        products_in_cart = cart.products.all()
        total_products = products_in_cart.count()

        # Calculate total price
        total_price = sum(product.price for product in products_in_cart)
    else:
        total_products = 0
        total_price = 0

    data = {
        'total_products': total_products,
        'total_price': total_price,
    }
    return JsonResponse(data)

# def checkout(request):
#     if request.method == 'POST':
#         form = BillingDetailsForm(request.POST)
#         if form.is_valid():
#             order = Order.objects.create(
#                 user=request.user,
#                 # Assign form data to respective model fields
#                 first_name=form.cleaned_data['first_name'],
#                 last_name=form.cleaned_data['last_name'],
#                 # Add other form fields here
#             )
#             return render(request, 'myapp/checkout_success.html')
#     else:
#         form = BillingDetailsForm()
    
#     return render(request, 'myapp/checkout.html', {'form': form})

def checkout(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        products_in_cart = cart.products.all()

        if products_in_cart.exists():
            current_order = Order.objects.filter(user=request.user).first()

            if current_order:
                total_price = current_order.total_price
            else:
                total_price = 0

            if request.method == 'POST':
                form = BillingDetailsForm(request.POST)
                if form.is_valid():
                    billing_details = BillingDetails.objects.create(
                        user=request.user,
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        company_name=form.cleaned_data['company_name'],
                        country=form.cleaned_data['country'],
                        street_address=form.cleaned_data['street_address'],
                        town_city=form.cleaned_data['town_city'],
                        zip_code=form.cleaned_data['zip_code'],
                        phone=form.cleaned_data['phone'],
                        email=form.cleaned_data['email'],
                        order_notes=form.cleaned_data['order_notes'],
                        # Add other form fields here
                    )
                    order = Order.objects.create(
                        user=request.user,
                        billing_details=billing_details,
                        # Add other order-related fields here
                        total_price=total_price  # Set the total_price from the current order
                    )

                    # Assuming you have a way to retrieve products (cart, session)
                    cart, _ = Cart.objects.get_or_create(user=request.user)
                    order.products.set(cart.products.all())

                    # Clear cart/session
                    cart.products.clear()
                    request.session['cart'] = []

                    return render_checkout_success(request, order)
                
            else:
                form = BillingDetailsForm()
            
            return render(request, 'myapp/checkout.html', {'form': form, 'total_price': total_price})
        else:
            # Handle the case where there are no products in the cart
            return HttpResponse("Go the home page")
    else:
        return redirect('account_login')  # Redirect unauthenticated users to login page

def render_checkout_success(request, order):
    products = order.products.all()
    return render(request, 'myapp/checkout_success.html', {'products': products})

def aboutus(request):
    return render(request, 'myapp/aboutus.html')

def shop_view(request):
    all_products = Product.objects.all()
    paginator = Paginator(all_products, 12)  # Show 12 products per page

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render(request, 'myapp/shop.html', {'products': products})

def contactus(request):
    return render(request, 'myapp/contactus.html')

# def add_to_wishlist(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     Wishlist.objects.get_or_create(user=request.user, product=product)
#     return redirect('wishlist')

# def wishlist_view(request):
#     wishlist_items = Wishlist.objects.filter(user=request.user)
#     return render(request, 'myapp/wishlist.html', {'wishlist_items': wishlist_items})



def check_authentication(request):
    if request.user.is_authenticated:
        # User is authenticated
        return JsonResponse({'authenticated': True})
    else:
        # User is not authenticated
        return JsonResponse({'authenticated': False})

def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=product_id)

        # Remove the product from the cart
        cart.products.remove(product)

        data = {'message': 'Product removed successfully'}
        return JsonResponse(data)
    else:
        data = {'error': 'User not authenticated'}
        return JsonResponse(data, status=401)

def update_subtotal(request):
    if request.method == 'POST':
        subtotal_value = request.POST.get('subtotal', '0.00')

        # Assuming you have a user associated with the request
        user = request.user

        # Get or create BillingDetails instance for the user
        billing_details, created = BillingDetails.objects.get_or_create(user=user)

        # Update subtotal and save
        billing_details.subtotal = subtotal_value
        billing_details.save()

        return JsonResponse({'status': 'success', 'subtotal': str(billing_details.subtotal)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})