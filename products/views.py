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
    sort = None
    direction = None

    #to take search requests
    if request.GET:
        #for sorting
        if 'sort' in request.GET:
            sortkey= request.GET['sort']
            sort = sortkey
            #sets sort from none to sortkey
            #for case insensitive sorting
            if sortkey == 'name':
                sortkey = 'lower_name'
                #to annotate products
                products  = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

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

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current-sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show product_detail """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)