from .models import CartItem


def cart_count(request):
    """Make cart count available in all templates"""
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    return {'cart_count': count}