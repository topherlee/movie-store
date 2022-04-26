from django.shortcuts import render, redirect, get_object_or_404


def home(request):
    context = {}
    return render(request, 'movie_store/home.html', context)

def search(request):
    context = {}
    return render(request, 'movie_store/search.html', context)