from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.movie_list, name='movie_list2'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movie_details/<id>/', views.movie_details, name='movie_details'),
    path('movies/new/', views.movie_modify, name='add_movie'),
    path('movies/modify/<id>/', views.movie_modify, name='edit_movie'),
    path('movies/delete/<id>/', views.movie_delete, name='delete_movie'),
    path('orders/', views.order_list, name='order_list'),
    path('order_details/<id>/', views.order_details, name='order_details'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
]
