from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem
from products.models import Product


@login_required
def view_cart(request):
    """Display user's cart"""
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    
    total = sum(item.subtotal for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Check stock
    if product.stock < quantity:
        messages.error(request, 'Not enough stock available!')
        return redirect('products:product_detail', slug=product.slug)
    
    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Item already in cart, update quantity
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart:view_cart')


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart:view_cart')


@login_required
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated!')
    else:
        cart_item.delete()
        messages.success(request, 'Item removed from cart!')
    
    return redirect('cart:view_cart')