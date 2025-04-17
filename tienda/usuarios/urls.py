from django.urls import path
from . import views

urlpatterns = [
    
    # Vista usuarios
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),

    path('address/', views.address, name='address'),
    path('address/add/', views.add_address, name='add_address'),
    path('address/update/<int:id>/', views.update_address, name='update_address'),
    path('address/delete/<int:id>/', views.delete_address, name='delete_address'),
    

]