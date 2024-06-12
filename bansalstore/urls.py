from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('',views.home,name = "home"),
    path('registration',views.registration, name="registration"),
    path('login',views.login,name = 'login'),
    path('logout',views.LogoutPage,name='logout'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('contact',views.contact,name='contact'),
    path('profile',views.profile,name='profile'),
    path('product_details/<int:product_id>/',views.details,name='product-details'),
    path('cart',views.cart,name='cart'),
    path('addtocart/<int:product_id>/',views.add_to_cart,name = "add_cart_items"),
    path('removeitems/<int:item_id>/',views.rmv_items_cart,name = "remove_items"),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('movetowishlist/<int:tp_id>/', views.move_to_wishlist, name='move_to_wishlist'),
    path('removeitemswishlist/<int:item_id>/',views.rmv_items_wishlist,name = "remove_items_wishlist"),
    path('add_from_wishlist_to_cart/<int:wishlist_item_id>/', views.add_from_wishlist_to_cart, name='add_from_wishlist_to_cart'),
    path('addtowhislist/<int:product_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('checkout_page',views.checkout,name='checkout'),
    path('order_history/', views.order_history, name='order_history'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('return_order_item/<int:order_item_id>/', views.return_order_item, name='return_order_item'),
    path('category/<str:category_name>/', views.category_view, name='category_view'),
    path('about',views.about,name='about'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
