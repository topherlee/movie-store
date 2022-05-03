from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from ..models import Customer, Order, LineItem
from django.contrib.auth.decorators import login_required, user_passes_test
from ..forms import CustomerForm, UserForm

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
def customer_modify(request):
    #customer = get_object_or_404(Customer,user_id=request.user.id)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        customer_form = CustomerForm(request.POST, instance=request.user.customer)
        if user_form.is_valid() and customer_form.is_valid():
            customer_form.save()
            user_form.save()
            return redirect('my_details')
    else:
        customer_form = CustomerForm(instance=request.user.customer)
        user_form = UserForm(instance=request.user)
    return render(request, 'movie_store/customer_modify.html', {'user_form':user_form,'customer_form':customer_form})