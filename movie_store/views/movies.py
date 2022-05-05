from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from ..models import Director, Movie, Comment
from ..forms import BasketAddProductForm, CommentForm, MoviesForm
from django.utils import timezone
import random

def movie_from_director(request,id):
    movies = Movie.objects.filter(director_id=id)
    director = Director.objects.get(id=id)
    return render(request, 'movie_store/movie_from_director.html', {'movies':movies,'director':director,})
 
def movie_list(request):
    sort_by = None
    basket_movie_form = BasketAddProductForm()

    if "sort" in request.session:
        sort_by = request.session["sort"]
    else:
        request.session["sort"] = None
    request.session.modified = True
    
    if request.method=="POST":
        sort_by = request.POST.get("sort")
        request.session["sort"] = sort_by
    
    if sort_by == None:
        movies = Movie.objects.all().order_by("title")
    else:
        movies = Movie.objects.all().order_by(f"{sort_by}")
    
    if sort_by == "title":
        sort = "Title (A-Z)"
    elif sort_by == "-title":
        sort = "Title (Z-A)"
    elif sort_by == "year_released":
        sort = "Release Year (Ascending)"
    elif sort_by == "-year_released":
        sort = "Release Year (Descending)"
    elif sort_by == "-imdb_rating":
        sort = "IMDb Rating (Descending)"
    elif sort_by == "imdb_rating":
        sort = "IMDb Rating (Ascending)"
    elif sort_by == "-price":
        sort = "Price (Descending)"
    elif sort_by == "price":
        sort = "Price (Ascending)"
    else:
        sort = "Title (A-Z)"
    
    paginator = Paginator(movies, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
   
    #choose random movie button
    ids = Movie.objects.count()
    first = Movie.objects.first().id
    last = Movie.objects.last().id
    if Movie.objects.get(id=random.randint(first,last)) == None:
        randoms = Movie.objects.first()
    else:
        randoms = Movie.objects.get(id=random.randint(first,last))
   
    context = {
        'page_obj':page_obj,
        'randoms':randoms,
        'basket_movie_form':basket_movie_form,
        'sort':sort,
    }
    return render(request, 'movie_store/movie_list.html', context)

def movie_details(request, id):
    recently_viewed_movies = None
    movie = get_object_or_404(Movie, id=id)
    basket_movie_form = BasketAddProductForm()
    comments = Comment.objects.filter(movie__id=id)


    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.movie = movie
            new_comment.save()
            return redirect("movie_details", id=movie.id)
    else:
        comment_form = CommentForm()

    if 'recently_viewed' in request.session:
        if id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(id)

        recently_viewed_movies = Movie.objects.filter(id__in=request.session['recently_viewed']) 
        request.session['recently_viewed'].insert(0, id)
        if len(request.session['recently_viewed']) > 7:
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [id]
    
    request.session.modified = True

    context = {
        'movie':movie,
        'basket_movie_form':basket_movie_form,
        'comments':comments,
        'comment_form':comment_form,
        'recently_viewed_movies':recently_viewed_movies,
        'page_obj':page_obj,
    }
    return render(request, 'movie_store/movie_details.html', context)

@user_passes_test(lambda u: u.is_staff)
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