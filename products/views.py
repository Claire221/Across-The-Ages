import random

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


# Create your views here.
def all_products(request):
    total_products = None
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
                messages.error(request,
                               "You didn't enter any search criteria!"
                               )
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)  # noqa
            products = products.filter(queries)

        total_products = len(products)
        # pagination
        page = request.GET.get("page", 1)
        # number of products per paginated page
        paginator = Paginator(products, 12)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'total_products': total_products,
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

    while len(related_products) != 4:
        random_choices = random.choices(similar_products, k=1)

        for choice in random_choices:
            if str(product.name) != str(choice):
                if choice in related_products:
                    pass
                else:
                    related_products.append(choice)

    context = {
        'product': product,
        'similar_products': related_products
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry you are not authorised to preform this function'
                       )
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product successfully added')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product, please try again.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry you are not authorised to preform this function'
                       )
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product successfully updated')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           'Failed to update product. Please try again'
                           )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    form = ProductForm(instance=product)
    messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request,
                       'Sorry you are not authorised to preform this function'
                       )
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product successfully deleted')

    return redirect(reverse('products'))
