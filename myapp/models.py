from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    CATEGORY = (
        ('Baby', 'Baby'),
        ('DIY & Tools', 'DIY & Tools'),
        ('Grocery', 'Grocery'),
        ('Health & Beauty', 'Health & Beauty'),
        ('Home & Kitchen', 'Home & Kitchen'),
        ('Office Products', 'Office Products'),
        ('Pet Supplies', 'Pet Supplies'),
        ('Sports & Outdoors', 'Sports & Outdoors'),
        ('Toys', 'Toys'),
    )
    title = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    short_description = models.CharField(max_length=255, null=True, blank=True)
    detailed_description = models.TextField()

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.title}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Cart - User: {self.user.username}"

class BillingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    company_name = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    street_address = models.CharField(max_length=250, null=True)
    town_city = models.CharField(max_length=250, null=True)
    zip_code = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=250, null=True)
    email = models.EmailField(max_length=254, null=True)
    order_notes = models.CharField(max_length=250, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # New field for subtotal


    def __str__(self):
        return f"BillingDetails - User: {self.user.username}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    billing_details = models.ForeignKey(BillingDetails, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Order #{self.id} - User: {self.user.username}, Status: {self.status}"
    
    # def total_price(self):
    #     # Calculate total price of all products in the order
    #     total = sum(product.price for product in self.products.all())
    #     return total

    # def __str__(self):
    #     return f"Order #{self.id} - User: {self.user.username}, Status: {self.status}"

# class Wishlist(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product)

#     def __str__(self):
#         return f"Wishlist for {self.user.username}"
