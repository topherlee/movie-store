from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from ..models import Movie
from ..forms import BasketAddProductForm, MoviesForm
from django.utils import timezone
import random
 
def movie_list(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    basket_movie_form = BasketAddProductForm()
    #choose random movie button
    ids = Movie.objects.count()
    first = Movie.objects.first().id
    randoms = Movie.objects.get(id=random.randint(first,ids))
    context = {
        'page_obj':page_obj,
        'randoms':randoms,
        'basket_movie_form':basket_movie_form,
    }
    return render(request, 'movie_store/movie_list.html', context)

def movie_details(request, id):
    movie = get_object_or_404(Movie, id=id)
    basket_movie_form = BasketAddProductForm()
    context = {
        'movie':movie,
        'basket_movie_form':basket_movie_form,
    }
    return render(request, 'movie_store/movie_details.html', context)

@login_required
def movie_modify(request, id=None):
    if id is not None:
        movie = get_object_or_404(Movie, id=id)
    else:
        movie = None
    
    if request.method == "POST":
        form = MoviesForm(request.POST, instance=movie)
        if form.is_valid():
            new_movie = form.save(commit=False)
            new_movie.created_date = timezone.now()
            new_movie.save()
            form.save_m2m()
            return redirect('movie_details', id=new_movie.id)
    else:
        form = MoviesForm(instance=movie)
    return render(request, 'movie_store/movie_edit.html', {'form':form})

@login_required
def movie_delete(request, id):
    movie = get_object_or_404(Movie, id=id)
    deleted = request.session.get('deleted','empty')
    request.session['deleted'] = movie.title
    movie.delete()
    return redirect('movie_list')