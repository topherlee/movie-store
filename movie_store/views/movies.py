from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from ..models import Movies
from ..forms import MoviesForm
from django.utils import timezone 
 
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

def movie_modify(request, id=None):
    if id is not None:
        movie = get_object_or_404(Movies, id=id)
    else:
        movie = None
    
    if request.method == "POST":
        form = MoviesForm(request.POST, instance=movie)
        if form.is_valid():
            new_movie = form.save(commit=False)
            new_movie.created_date = timezone.now()
            new_movie.save()
            new_movie.save_m2m()
            return redirect('movie_details', id=new_movie.id)
    else:
        form = MoviesForm(instance=movie)
    return render(request, 'movie_store/movie_edit.html', {'form':form})
"""
def movie_edit(request):
    product = get_object_or_404(Movies, id=id)
    if request.method=="POST":
        form = MoviesForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            form.save_m2m()
            return redirect('movie_details', id=product.id)
    else:
        form = MoviesForm(instance=product)
    return render(request, 'movie_store/movie_edit.html', {'form':form})
"""