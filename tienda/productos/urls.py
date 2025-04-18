
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.list_products, name='list_products'),  
    path('category/<int:id_categoria>/', views.list_products, name='products_by_category'),
    path('product_detail/<int:id_producto>/', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
