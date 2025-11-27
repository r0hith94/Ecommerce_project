"""
Products Views - Display products, categories, search
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category


def home(request):
    """Homepage - Featured products"""
    featured_products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'products/home.html', context)


# def product_list(request):
#     """All products with filtering and search"""
#     products = Product.objects.filter(is_active=True).select_related('category')
    
#     # Category filter
#     category_slug = request.GET.get('category')
#     if category_slug:
#         products = products.filter(category__slug=category_slug)
    
#     # Search
#     search_query = request.GET.get('search')
#     if search_query:
#         products = products.filter(
#             Q(name__icontains=search_query) |
#             Q(description__icontains=search_query)
#         )
    
#     # Pagination
#     paginator = Paginator(products, 12)  # 12 products per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     categories = Category.objects.all()
    
#     context = {
#         'page_obj': page_obj,
#         'categories': categories,
#         'current_category': category_slug,
#         'search_query': search_query,
#     }
#     return render(request, 'products/product_list.html', context)
def product_list(request):
    """All products with filtering and search"""
    products = Product.objects.filter(is_active=True).select_related('category')
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Price Range Filter (NEW!)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sort by (NEW!)
    sort_by = request.GET.get('sort')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'name':
        products = products.order_by('name')
    
    # Stock filter (NEW!)
    stock_filter = request.GET.get('stock')
    if stock_filter == 'in_stock':
        products = products.filter(stock__gt=0)
    elif stock_filter == 'out_of_stock':
        products = products.filter(stock=0)
    
    # Get price range for display
    from django.db.models import Min, Max
    price_range = Product.objects.filter(is_active=True).aggregate(
        min=Min('price'),
        max=Max('price')
    )
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'stock_filter': stock_filter,
        'price_range': price_range,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Individual product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)