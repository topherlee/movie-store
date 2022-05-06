from decimal import Decimal
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from movie_store.models import Movie
from movie_store.forms import BasketAddProductForm 

class Basket(object):
    
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            # save an empty basket in the session
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def __iter__(self):
        print(f'basket: { self.basket }')
        movie_ids = self.basket.keys()
        movies = Movie.objects.filter(id__in=movie_ids)

        basket = self.basket.copy()
        for movie in movies:
            basket[str(movie.id)]['movie'] = movie
            basket[str(movie.id)]['movie_id'] = movie.id

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.basket.values())

    def add(self, movie, quantity=1, override_quantity=False):
        movie_id = str(movie.id)
        if movie_id not in self.basket:
            self.basket[movie_id] = {'quantity': 0,
                                      'price': str(movie.price)}
        if override_quantity:
            self.basket[movie_id]['quantity'] = quantity
        else:
            self.basket[movie_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, movie):
        movie_id = str(movie.id)
        if movie_id in self.basket:
            del self.basket[movie_id]
            self.save()

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())


@require_POST
def basket_add(request, movie_id):
    basket = Basket(request)
    movie = get_object_or_404(Movie, id=movie_id)
    form = BasketAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        basket.add(movie=movie,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@require_POST
def basket_remove(request, movie_id):
    basket = Basket(request)
    movie = get_object_or_404(Movie, id=movie_id)
    basket.remove(movie)
    return redirect('basket_detail')

def basket_detail(request):
    basket = Basket(request)
    total = len(basket)
    for item in basket:
        item['update_quantity_form'] = BasketAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    return render(request, 'movie_store/basket.html', {'basket': basket, 'total':total})
