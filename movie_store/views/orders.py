from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ..models import LineItem, Order

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'movie_store/order_list.html', {'orders':orders})

@login_required
def order_details(request, id):
    order = get_object_or_404(Order, id=id)
    customer = order.customer
    user = get_object_or_404(User, id=customer.pk)
    line_items = LineItem.objects.filter(order_id=order.id)
    context = {
        'order':order, 'user':user, 'line_items':line_items, 'customer':customer
    }
    return render(request, 'movie_store/order_details.html', context)