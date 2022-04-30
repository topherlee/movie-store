from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from ..models import Movie,Director,Actor
from ..forms import SignUpForm

def home(request):
    context = {}
    return render(request, 'movie_store/home.html', context)

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.customer.first_name = form.cleaned_data.get('first_name')
            user.customer.last_name = form.cleaned_data.get('last_name')
            user.customer.address = form.cleaned_data.get('address')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

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
        results = Director.objects.filter(name__iregex=fr"{query}")    #director__name__contains=f'{query}')
    elif search == "artist":
        results = Actor.objects.filter(name__iregex=fr"{query}")
    elif search == "title":
        results = Movie.objects.filter(title__iregex=fr"({query})")

    paginator = Paginator(results, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'results':results,
        'query':query,
        'search':search,
        'page_obj':page_obj,
        }
    return render(request, 'movie_store/search.html', context)