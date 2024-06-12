from django.contrib import admin
from .models import Product, Category,CartItem,Order,OrderItem,Wishlist,UserProfile

@admin.register(UserProfile)
class UserProfilelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','email','address','gender','date_of_birth','mobile_number','bio','profile_picture']

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display=['id','name']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','name','description','price','brand','category','image']


@admin.register(CartItem)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display=['id','product','qunatity','user','date_added']

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=['id','user','total_amount','date_place','status']

@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display=['id','order','product','quantity','is_returned','return_date']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','product','user','date_added']