# 🛒 E-commerce Website

A full-stack Django-based e-commerce application with authentication, cart,
checkout, and product management.

------------------------------------------------------------
# 🔥 Features
------------------------------------------------------------
• Full-stack Django web app
• Product listing with categories
• Add to cart / Remove from cart / Update quantity
• User authentication (Login / Signup / Logout)
• Order place → Checkout flow
• Responsive UI using Bootstrap
• SQLite database
• Hosted on Render
• Auto-deployment from GitHub
• CSRF-protected + session-based cart system

------------------------------------------------------------
# 🧱 Tech Stack
------------------------------------------------------------
Frontend  : HTML, CSS, JavaScript, Bootstrap
Backend   : Django, Django ORM, Django Templates
Database  : SQLite
Deployment: Render + GitHub

------------------------------------------------------------
# 🔧 How It Works
------------------------------------------------------------
1. User opens website
2. Browses products
3. Adds products to cart
4. Cart stores items in Django session
5. User logs in to checkout
6. Django processes order
7. Confirmation shown to user

------------------------------------------------------------
# ⚙️ Setup Instructions
------------------------------------------------------------
# Clone repository
git clone <repo-link>

# Go to project folder
cd ecommerce-project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver

------------------------------------------------------------
# 🧠 Skills Demonstrated
------------------------------------------------------------
• Full-stack development
• Django backend development
• Session handling & authentication
• Database modeling with Django ORM
• Deployment on Render
• Git & GitHub workflow
• Responsive UI design

