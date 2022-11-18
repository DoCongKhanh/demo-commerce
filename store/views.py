from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Sub_Category, Product, Order, OrderItems, Brand
from .forms import UserCreateForm, OrderForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate, login
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError

from .cart import Cart
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'store/index.html')


def signup(request):
    if request.method == 'POST':        
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()         
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            new_user = authenticate(request,username = username,password = password)
            print('new_user',new_user)    
            login(request, new_user)
            messages.success(request, "Registration successful." )
            return redirect('shop')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreateForm()      
    context = {'form':form}
    return render(request, 'store/signup.html', context)


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "forget_password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request, template_name="forget_password/password_reset_form.html", context={"password_reset_form":password_reset_form})


def shop_view(request):
    category = Category.objects.all()
    category_sub = Sub_Category.objects.all()
    brand = Brand.objects.all()
    products = Product.objects.all() 
    paginator = Paginator(Product.objects.all(), 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'category_sub': category_sub,
        'brand': brand,
        'products': products,
        'page_obj': page_obj
        
    }
    return render(request, 'store/shop.html', context)


def category_detail(request, slug):
    category = Category.objects.all()
    category_slug = get_object_or_404(Sub_Category, slug=slug)
    products = category_slug.products.all()
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category':category,
        'category_slug': category_slug,
        'products':products,
        'page_obj': page_obj
    }
    return render(request, 'store/category_detail.html', context)


# def brand_detail(request, brand_slug):
#     category = Category.objects.all()
#     brand = Brand.objects.all()
#     brand_obj = get_object_or_404(Brand, slug=brand_slug)
#     products = brand_obj.products.all()
#     paginator = Paginator(products, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'category': category,
#         'brand': brand,
#         'brand_obj' : brand_obj,
#         'page_obj': page_obj
#     }   
#     return render(request, 'store/brand_detail.html', context)


def product_view(request, category_slug, slug):
    cart = Cart(request)
    print(cart.get_total_cost())
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'store/product_view.html',context)

def search(request):
    query = request.GET.get('query','')
    print('query',query)
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(slug__icontains=query))
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'query':query,
        'products':products,
        'page_obj':page_obj
    }
    return render(request, 'store/search.html',context)
    

# Cart
def add_to_cart(request, product_id):
    action = request.GET.get('action', '')
    print('action',action)
    if action:
        quantity = 1
        cart = Cart(request)
        cart.add(product_id,quantity,True)
    return redirect('shop')


def cart_view(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'store/cart_view.html', context)


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart-view')
 
 
def change_quantity(request, product_id):
    action = request.GET.get('action', '')
    print('action',action)
    if action:
        quantity = 1
        if action == 'decrease':
            quantity = -1         
        cart = Cart(request)
        cart.add(product_id, quantity, True)
    return redirect('cart-view')
   

@login_required
def check_out_cart(request):
    cart = Cart(request)
    if request.method == 'POST':
        order = Order()
        order.user = request.user
        order.first_name = request.POST.get('firstname')
        order.last_name = request.POST.get('lastname')
        order.phone = request.POST.get('number')
        order.address = request.POST.get('add')
        order.distric = request.POST.get('district')
        order.city = request.POST.get('city')
        order.zipcode = request.POST.get('zip')       
        total_cost_cart = 0
        for items in cart:
            product = items['product']
            quantity = int(items['quantity'])               
            total_cost_cart = total_cost_cart + product.price * quantity  
        order.total_cost = total_cost_cart
        order.save()
        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            total_price = product.price * quantity    
            item = OrderItems.objects.create(order=order, product=product, total_price=total_price, quantity=quantity)
        cart.clear()  
        messages.success(request, "Your order has been received" )
        return redirect('confirmation')   
    return render(request, 'store/checkout.html')


@login_required
def confirmation_view(request):
    order = Order.objects.filter(user=request.user).first()
    items = order.items.all()
    print('order',order)
    print('items',items)
    context = {'order': order, 'items':items }  
    return render(request, 'store/confirmation.html', context)