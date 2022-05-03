from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.movie_list, name='movie_list2'),
    path('movies/', views.movie_list, name='movie_list'),
    path('director/<id>/', views.movie_from_director, name='movie_from_director'),
    path('movie_details/<id>/', views.movie_details, name='movie_details'),
    path('movies/new/', views.movie_modify, name='add_movie'),
    path('movies/modify/<id>/', views.movie_modify, name='edit_movie'),
    path('movies/delete/<id>/', views.movie_delete, name='delete_movie'),
    path('orders/', views.order_list, name='order_list'),
    path('order_details/<id>/', views.order_details, name='order_details'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer_details/<id>/', views.customer_details, name='customer_details'),
    path('customer_modify/' ,views.customer_modify ,name='customer_modify'),
    path('my_details/', views.customer_own_detail, name='my_details'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('basket_add/<int:movie_id>/', views.basket.basket_add, name ='basket_add'),
    path('basket_remove/<int:movie_id>/', views.basket.basket_remove, name ='basket_remove'),
    path('basket_detail/', views.basket.basket_detail, name ='basket_detail'),
    path('purchase/', views.purchase, name ='purchase'),
    path('payment/', views.payment, name ='payment'),
]
