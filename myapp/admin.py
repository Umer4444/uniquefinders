from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        # Retrieve the products related to the cart being deleted
        products = obj.products.all()
        
        # Remove the association of these products with the cart
        for product in products:
            obj.products.remove(product)

        # Continue with the deletion of the cart
        super().delete_model(request, obj)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'status', 'total_price')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'id')  # Search by user's username or order ID

@admin.register(BillingDetails)
class BillingDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'total_price', 'company_name',
    'country',
    'street_address',
    'town_city',
    'zip_code',
    'phone',
    'email',
    'order_notes'
    ) 


# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     pass