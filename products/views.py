from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    # to set initial stateof query to none
    query = None
    categories = None

    #to take search requests
    if request.GET:
        #for category search
        if 'category' in request.GET:
            categories = request.GET['category'].split(',') #split query at commas (where appropriate) and use to search all present products
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if 'q' in request.GET:
            query = request.GET['q']
            #to handle blank searches
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                return redirect(reverse('products'))

            #set variable = to Q object where name or description contians query
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # adds queries var to the filter
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show product_detail """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)