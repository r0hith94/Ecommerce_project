from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from cart.models import CartItem


@login_required
def checkout(request):
    """Checkout page"""
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart:view_cart')
    
    total = sum(item.subtotal for item in cart_items)
    
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total,
                    shipping_address=address,
                    phone=phone,
                    payment_method=payment_method
                )
                
                # Create order items and reduce stock
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        product_name=cart_item.product.name,
                        product_price=cart_item.product.price,
                        quantity=cart_item.quantity
                    )
                    
                    # Reduce stock
                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.save()
                
                # Clear cart
                cart_items.delete()
                
                messages.success(request, 'Order placed successfully!')
                return redirect('orders:order_confirmation', order_id=order.id)
                
        except Exception as e:
            messages.error(request, 'Error placing order. Please try again.')
            return redirect('orders:checkout')
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})


@login_required
def order_list(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})