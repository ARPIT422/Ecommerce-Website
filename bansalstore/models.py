from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,Group, Permission
User = get_user_model()


gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=False, null=False, blank=False,default='abc@gmail.com')
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=gender_choices)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=200,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    qunatity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.qunatity} x {self.product.name}'

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_place = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'),
                                                      ('Shipped', 'Shipped'),
                                                      ('Delivered', 'Delivered'),
                                                      ('Cancelled', 'Cancelled')], default='Pending')

    def __self__(self):
        return f'{self.id} by {self.user}'

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    is_returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} x {self.user.username}'
#return f'{self.qunatity} x {self.product.name}'

    
    