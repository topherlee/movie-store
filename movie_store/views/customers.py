from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from ..models import Customer, Order, LineItem
from django.contrib.auth.decorators import login_required, user_passes_test
from ..forms import CustomerForm

@user_passes_test(lambda u: u.is_staff)
def customer_list(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
    context = {
        'page_obj':page_obj
    }
    return render(request, 'movie_store/customers.html', context)

@user_passes_test(lambda u: u.is_staff)
def customer_details(request, id):
    customer = get_object_or_404(Customer, user_id=id)
    orders = Order.objects.filter(customer_id=customer.user_id)

    context = {
        'customer':customer,
        'orders':orders,
    }
    return render(request, 'movie_store/customer_details.html', context)

@login_required
def customer_own_detail(request):

    customer = get_object_or_404(Customer, user_id=request.user.id)
    orders = Order.objects.filter(customer_id=customer.user_id)

    context = {
        'customer':customer,
        'orders':orders,
    }
    return render(request, 'movie_store/customer_details.html', context)

@login_required
def customer_modify(request, id):
    customer = get_object_or_404(Customer, user_id=id)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            edited_cust = form.save(commit=False)
            edited_cust.user = request.user
            edited_cust.save()
            return redirect('customer_details', id=edited_cust.user_id)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'movie_store/customer_modify.html', {'form':form,'customer':customer})