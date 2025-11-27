"""
Products App URLs
"""

from django.urls import path
from . import views
from . import dashboard_views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('dashboard/', dashboard_views.sales_dashboard, name='sales_dashboard'),
    path('dashboard/sql/', dashboard_views.show_sql_queries, name='show_sql_queries'),
    path('dashboard/sql-executor/', dashboard_views.sql_executor, name='sql_executor'),
]