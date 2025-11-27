"""
Orders App Models - Order Management
Demonstrates: Complex relationships, Transaction handling, Junction tables
"""

from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    """
    Order Model - Main order table
    One user can have many orders
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
    ]
    
    # Foreign Key to User
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    # Order info
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    
    # Shipping details
    shipping_address = models.TextField()
    phone = models.CharField(max_length=15)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['order_number']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            self.order_number = f"ORD{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"


class OrderItem(models.Model):
    """
    OrderItem - Junction table between Order and Product
    Stores snapshot of product details at time of order
    """
    # Foreign Keys
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items'
    )
    
    # Product snapshot (for history)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        return f"{self.order.order_number} - {self.product_name}"
    
    @property
    def subtotal(self):
        return self.product_price * self.quantity
    
    def save(self, *args, **kwargs):
        # Store product details at time of order
        if self.product and not self.product_name:
            self.product_name = self.product.name
            self.product_price = self.product.price
        super().save(*args, **kwargs)
