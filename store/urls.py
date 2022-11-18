from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('password_reset/', views.password_reset_request, name='password_reset'),
    
    path('', views.home, name='home'), 
    path('search/',views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('shop/', views.shop_view, name='shop'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('change-quantity/<int:product_id>/', views.change_quantity, name='change-quantity'),
    path('remove-from-cart/<str:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    
    path('cart-view/', views.cart_view, name='cart-view'),
    path('checkout/', views.check_out_cart, name='checkout'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
    # path('<slug:brand_slug>/', views.brand_detail, name='brand_detail'),  
    path('<slug:category_slug>/<slug:slug>/', views.product_view, name='product_view'),
]