from django.shortcuts import render
from .models import * 
from django.db.models import Q
# Create your views here.


def index(request):
    search_query = request.GET.get('search', '')
    if search_query:
        post = Product.objects.filter(Q(name__icontains=search_query)| Q (brand__icontains=search_query))
    else:
        post = Product.objects.all()
    context={
        'post':post,
    }
    return render(request, 'EcomWebApp/index.html', context)


def detail(request, pk):
    post = Product.objects.get(id=pk)
    context ={
        'post': post,
    }
    return render(request, 'EcomWebApp/details.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() #this order is came from above line which get or create the database of Order
    else:
        items = [] #empty list(if user is not authenticated we return nothing)
        order = {'get_cart_total':0,'get_cart_items':0} #guest user login huda 0/0 dekhaune ho yo chai
    context ={
        'items':items,
        'order':order,
    }
    return render(request, 'EcomWebApp/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0} 
    context ={
        'items':items,
        'order':order,
    }
    return render(request, 'EcomWebApp/checkout.html', context)