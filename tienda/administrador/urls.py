
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin routes
        path('login/admin/', views.login, name='login_admin'),
        path('logout/admin/', views.logout, name='logout_admin'),
        path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),

        path('dashboard_admin/productos/', views.lista_productos_admin, name='lista_productos_admin'),
        path('dashboard_admin/agregar_producto/', views.agregar_producto, name='agregar_producto'),
        path('dashboard_admin/editar_producto/<int:id_producto>/', views.editar_producto, name='editar_producto'),
        path('dashboard_admin/eliminar_producto/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),

        path('dashboard_admin/list_brands/', views.list_brands, name='list_brands'),
        path('dashboard_admin/brand/add_brand/', views.add_brand, name='add_brand'),
        path('dashboard_admin/brand/edit_brand/<int:brand_id>/', views.edit_brand, name='edit_brand'),
        path('dashboard_admin/brand/delete_brand/<int:brand_id>/', views.delete_brand, name='delete_brand'),

        path('dashboard_admin/banner/', views.list_banners, name='list_banners'),
        path('dashboard_admin/banner/add_banner/', views.add_banner, name='add_banner'),
        path('dashboard_admin/banner/edit_banner/<int:banner_id>/', views.edit_banner, name='edit_banner'),
        path('dashboard_admin/banner/delete_banner/<int:banner_id>/', views.delete_banner, name='delete_banner'),

        path('variants/', views.list_variants, name='list_variants'),
        path('add_variant/<int:id_producto>/', views.add_variant, name='add_variant'),
        path('edit_variant/<int:id_variante>/', views.edit_variant, name='edit_variant'),
        path('delete_variant/<int:id_variante>/', views.delete_variant, name='delete_variant'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
