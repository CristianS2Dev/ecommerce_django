
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('products/', views.products, name='products'),
    path('list_products/', views.list_products, name='list_products'),
    path('product_detail/<int:id_producto>/', views.product_detail, name='product_detail'),
    path('products_by_category/<int:id_categoria>/', views.products_by_category, name='products_by_category'),

] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
