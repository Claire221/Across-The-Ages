import random
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category


# Create your views here.
def all_products(request):
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    products = Product.objects.all()

    product = get_object_or_404(Product, pk=product_id)

    product_category = product.category

    similar_products = Product.objects.filter(category=product_category)
    
    related_products = []

    for item in similar_products:
        if len(similar_products) > 4:
            while len(related_products) <= 3:
                if similar_products not in related_products:
                    related_products.append(random.choice(similar_products))
                    print(similar_products)
        elif len(similar_products) <= 4:
            if item not in related_products:
                related_products.append(random.choice(item))
    
    context = {
        'product': product,
        'similar_products' : related_products
    }

    print("TEST")
    print(len(similar_products))
    return render(request, 'products/product_detail.html', context)