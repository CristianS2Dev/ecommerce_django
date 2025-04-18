
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
 path('cart/', views.cart, name='cart'),
    path('get_cart/', views.get_cart, name='get_cart'),
    path('add_item/<int:id_producto>/', views.add_item, name='add_item'),
    path('update_item/<int:id_elemento>/', views.update_item, name='update_item'),
    path('remove_item/<int:id_elemento>/', views.remove_item, name='remove_item'),
    path('checkout_cart/', views.checkout_cart, name='checkout_cart'),
]