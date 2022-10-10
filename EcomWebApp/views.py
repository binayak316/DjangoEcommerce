from django.shortcuts import render
from .models import Product
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