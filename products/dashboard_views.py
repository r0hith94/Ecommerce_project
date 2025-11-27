"""
Admin Dashboard Views - Sales Analytics
Demonstrates: Aggregate functions, GROUP BY, Complex JOINs
"""

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg, F
from products.models import Product, Category
from orders.models import Order, OrderItem
from django.contrib.auth.models import User
from datetime import datetime, timedelta


@staff_member_required
def sales_dashboard(request):
    """
    Sales Analytics Dashboard
    Shows: Total sales, orders, top products, category sales
    """
    
    # Total Statistics
    total_orders = Order.objects.count()
    total_revenue = Order.objects.exclude(status='cancelled').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    total_customers = User.objects.filter(orders__isnull=False).distinct().count()
    
    pending_orders = Order.objects.filter(status='pending').count()
    
    



    # Top 5 Selling Products (by quantity sold)
    top_products = OrderItem.objects.values(
        'product__name', 'product__price'
    ).annotate(
        total_sold=Sum('quantity'),
        revenue=Sum(F('quantity') * F('product_price'))
    ).order_by('-total_sold')[:5]
    

    
    # Sales by Category
    category_sales = OrderItem.objects.values(
        'product__category__name'
    ).annotate(
        total_sold=Sum('quantity'),
        revenue=Sum(F('quantity') * F('product_price'))
    ).order_by('-revenue')
    
    # Recent Orders (last 10)
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    # Low Stock Products (stock < 10)
    low_stock_products = Product.objects.filter(
        stock__lt=10, 
        is_active=True
    ).order_by('stock')
    
    # Orders by Status
    orders_by_status = Order.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # This Month's Revenue
    today = datetime.now()
    first_day = today.replace(day=1)
    month_revenue = Order.objects.filter(
        created_at__gte=first_day,
        status__in=['pending', 'processing', 'shipped', 'delivered']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Today's Orders
    today_orders = Order.objects.filter(
        created_at__date=today.date()
    ).count()

    
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'pending_orders': pending_orders,
        'top_products': top_products,
        'category_sales': category_sales,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'orders_by_status': orders_by_status,
        'month_revenue': month_revenue,
        'today_orders': today_orders, 
       
    }
    
    return render(request, 'admin_dashboard/sales_dashboard.html', context)

@staff_member_required
def show_sql_queries(request):
    """
    Display actual SQL queries being executed
    Shows raw SQL alongside Django ORM
    """
    from django.db import connection
    
    # Query 1: Top Products with Raw SQL
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.name as product_name,
                c.name as category_name,
                SUM(oi.quantity) as total_sold,
                SUM(oi.quantity * oi.product_price) as revenue
            FROM order_items oi
            INNER JOIN products p ON oi.product_id = p.id
            INNER JOIN categories c ON p.category_id = c.id
            GROUP BY p.id, c.id
            ORDER BY revenue DESC
            LIMIT 10
        """)
        top_products_sql = cursor.fetchall()
    
    # Query 2: Customer Order Count
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                u.username,
                u.email,
                COUNT(o.id) as total_orders,
                SUM(o.total_amount) as total_spent
            FROM auth_user u
            INNER JOIN orders o ON u.id = o.user_id
            WHERE o.status != 'cancelled'
            GROUP BY u.id
            ORDER BY total_spent DESC
            LIMIT 10
        """)
        top_customers_sql = cursor.fetchall()
    
    # Query 3: Low Stock Products
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                name,
                stock,
                price,
                (stock * price) as inventory_value
            FROM products
            WHERE stock < 10 AND is_active = 1
            ORDER BY stock ASC
        """)
        low_stock_sql = cursor.fetchall()
    
    # Query 4: Daily Sales (Last 7 days)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                DATE(created_at) as order_date,
                COUNT(*) as order_count,
                SUM(total_amount) as daily_revenue
            FROM orders
            WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY DATE(created_at)
            ORDER BY order_date DESC
        """)
        daily_sales_sql = cursor.fetchall()

            

    
    context = {
        'top_products_sql': top_products_sql,
        'top_customers_sql': top_customers_sql,
        'low_stock_sql': low_stock_sql,
        'daily_sales_sql': daily_sales_sql,
        
    }
    
    return render(request, 'admin_dashboard/sql_display.html', context)

@staff_member_required
def sql_executor(request):
    """Execute custom SQL queries - Admin only"""
    results = None
    columns = None
    error = None
    query = ''
    
    if request.method == 'POST':
        query = request.POST.get('sql_query', '').strip()
        
        # Security: Only allow SELECT queries
        if not query.upper().startswith('SELECT'):
            error = "❌ Only SELECT queries are allowed!"
        else:
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
            except Exception as e:
                error = f"❌ Error: {str(e)}"
    
    context = {
        'results': results,
        'columns': columns,
        'error': error,
        'query': query,
    }
    return render(request, 'admin_dashboard/sql_executor.html', context)