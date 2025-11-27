
# Create your models here.
"""
Products App Models - MySQL Database Tables
Demonstrates: Foreign Keys, Indexes, Constraints, Normalization
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """
    Category Model - Parent table for products
    Demonstrates: 3NF Normalization, One-to-Many relationship
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
        db_table = 'categories'
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product Model - Main product table
    Foreign Key to Category (Many-to-One)
    All changes sync automatically to MySQL
    """
    # Basic Information
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    # Foreign Key - Links to Category table
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    
    # Image Upload
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Who added this product
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='added_products'
    )
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'products'
        indexes = [
            models.Index(fields=['name', 'category']),
            models.Index(fields=['is_active']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    @property
    def is_in_stock(self):
        return self.stock > 0