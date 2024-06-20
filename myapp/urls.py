from . import views
from django.urls import path
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<str:category>/', views.category_products, name='category_products'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('get_cart_details/', views.get_cart_details, name='get_cart_details'),
    path('checkout/', views.checkout, name='checkout'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('shop/', views.shop_view, name='shop'),
    path('contactus/', views.contactus, name='contactus'),
    path('check-authentication/', views.check_authentication, name='check_authentication'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_subtotal/', views.update_subtotal, name='update_subtotal'),
    path('logo_uniquefindertraders with background.ico', RedirectView.as_view(url='/static/images/logo_uniquefindertraders with background.ico')),


    # path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    # path('wishlist/', views.wishlist_view, name='wishlist'),
    
]
