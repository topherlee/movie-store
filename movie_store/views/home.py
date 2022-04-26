from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from ..models import Movies,Director,Artist

def home(request):
    context = {}
    return render(request, 'movie_store/home.html', context)

def search(request):
    if 'query' in request.session:
        search = request.session['search']
        query = request.session['query']
    else:    
        results,search,query,page_obj = None,None,None,None
    request.session.modified=True

    if request.method == "POST":
        query = request.POST.get("query")
        search = request.POST.get("search")
        request.session['query'] = query
        request.session['search'] = search

    if search == "director":
        results = Director.objects.filter(name__iregex=fr"{query}+")    #director__name__contains=f'{query}')
    elif search == "artist":
        results = Artist.objects.filter(name__iregex=fr"{query}+")
    elif search == "title":
        results = Movies.objects.filter(title__iregex=fr"{query}+")

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'results':results,
        'query':query,
        'search':search,
        'page_obj':page_obj,
        }
    return render(request, 'movie_store/search.html', context)