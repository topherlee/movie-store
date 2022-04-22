from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movie_details/<id>/', views.movie_details, name='movie_details'),
    path('search/', views.search, name='search'),
]
