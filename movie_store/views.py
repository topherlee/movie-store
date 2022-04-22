from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Movies


# Create your views here.
def home(request):
    context = {}
    return render(request, 'movie_store/home.html', context)

def movie_list(request):
    movies = Movies.objects.all()
    paginator = Paginator(movies, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj,
    }
    return render(request, 'movie_store/movie_list.html', context)

def movie_details(request, id):
    movie = get_object_or_404(Movies, id=id)
    context = {
        'movie':movie
    }
    return render(request, 'movie_store/movie_details.html', context)

def search(request):
    context = {}
    return render(request, 'movie_store/search.html', context)