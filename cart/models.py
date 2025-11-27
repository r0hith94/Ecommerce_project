"""
Cart App Models - Shopping Cart
Demonstrates: Many-to-One relationships, Composite keys
"""

from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class CartItem(models.Model):
    """
    CartItem - Links users to products
    Many cart items belong to one user
    Many cart items can reference one product
    """
    # Foreign Keys
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    
    # Quantity
    quantity = models.PositiveIntegerField(default=1)
    
    # Timestamps
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart_items'
        # Composite unique constraint - user can't add same product twice
        unique_together = ['user', 'product']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity})"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.product.price * self.quantity