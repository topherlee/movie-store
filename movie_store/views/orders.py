from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models import LineItem, Order

@user_passes_test(lambda u: u.is_staff)
def order_list(request):
    orders = Order.objects.all().order_by("-created_date")
    return render(request, 'movie_store/order_list.html', {'orders':orders})

@login_required
def order_details(request, id):
    order = get_object_or_404(Order, id=id)
    customer = order.customer
    username = get_object_or_404(User, id=customer.pk)
    line_items = LineItem.objects.filter(order_id=order.id)
    context = {
        'order':order, 'username':username, 'line_items':line_items, 'customer':customer
    }
    return render(request, 'movie_store/order_details.html', context)