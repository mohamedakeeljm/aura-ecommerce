# AuraShop - Simple E-Commerce Store Web Application

A fully functional, responsive, modern full-stack E-Commerce Store built using **Python/Django**, **SQLite**, and a premium custom **Vanilla CSS** and **Vanilla JavaScript** frontend.

---

## Technical Stack
- **Backend**: Django 6.1 (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3 (Vanilla CSS variables, grid, and animations), and JavaScript (Vanilla AJAX for shopping cart updates).
- **Authentication**: Django's built-in User Authentication system (login, registration, logout, profile forms).

---

## Features Implemented
1. **Home Page**: Interactive hero banner, shop collections category routing, featured products grid, dynamic cart counter header, responsive navigation, and contact footer.
2. **Product Catalog**: Category filtering side widget, text search engine, modern product grid with details, and fast add-to-cart action.
3. **Product Details Page**: Large product card, stock status warning labels, quantity adjusters, detailed specifications, and category-matching recommendations.
4. **Shopping Cart Page**: Table view of items with live AJAX increment/decrement/removal controls, automatic real-time subtotal/total calculations without reloading, continue shopping, and proceed-to-checkout CTAs.
5. **Checkout & Form Handling**: Shipping form details, side-by-side order summary breakdown, CSRF security verification, stock quantity validation, and database storage.
6. **Order Placement & Confirmation**: Custom unique order numbers generated (`ORD-YYYYMMDD-XXXXX`), cart wiping post-checkout, and success message cues.
7. **Order History**: User profile records displaying order dates, numbers, total amounts, and color-coded status badges (`Pending`, `Processing`, etc.).
8. **Admin Panel Control**: Full models registry for managers to control products, stocks, categories, users, and modify order fulfillment status directly.

---

## Project Structure
```
ecommerce/
├── db.sqlite3                  # SQLite Database File
├── manage.py                   # Django CLI executable
├── seed.py                     # Initial database seeding script
├── venv/                       # Python Virtual Environment
├── ecommerce/                  # Django project root configurations
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                      # Main e-commerce shop app
│   ├── admin.py                # Admin portal registry
│   ├── cart.py                 # Session Cart storage class
│   ├── context_processors.py   # Cart global template context loader
│   ├── forms.py                # Registration, profile, checkout forms
│   ├── models.py               # SQLite Models (Category, Product, Order)
│   ├── urls.py                 # App sub-routing definitions
│   ├── views.py                # App controllers / handlers
│   └── templates/
│       └── store/              # HTML Templates (base, home, details, cart, etc.)
└── static/                     # Static assets directory
    ├── css/
    │   └── style.css           # Custom design system CSS
    └── js/
        └── cart.js             # Cart AJAX update controller
```

---

## Installation & Setup Instructions

### 1. Prerequisites
Ensure you have **Python 3.12+** installed. (If you ran the system commands, Python 3.12 is already installed at: `C:\Users\SOOQ ELASER\AppData\Local\Programs\Python\Python312\python.exe`).

### 2. Activate the Virtual Environment
Open a terminal in the project directory (`c:\xampp\htdocs\application\ecommerce`) and execute:
```powershell
# PowerShell
.\venv\Scripts\Activate.ps1
```
```cmd
# Command Prompt
venv\Scripts\activate.bat
```

### 3. Install Dependencies
*(Already completed in task execution)*
If recreating, run:
```bash
pip install django pillow
```

### 4. Database Setup & Seeding
The database comes configured and seeded. To recreate or reseed from scratch:
```bash
# Run migrations to build the tables
python manage.py migrate

# Seed categories, default products, and the administrator account
python seed.py
```

### 5. Running the Application
Start the Django development server:
```bash
python manage.py runserver
```
The server will boot up locally at:
**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Demo Credentials for Testing (Local Development Only)
- **Admin Panel URL**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

> [!WARNING]
> For local testing, a default user `admin` with password `admin12345` is seeded. 
> **Never use these credentials in a live production environment.** For secure production setup, create a new administrator account by running:
> ```bash
> python manage.py createsuperuser
> ```

