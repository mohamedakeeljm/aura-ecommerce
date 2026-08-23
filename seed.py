import os
import django

# Set settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product

def seed_db():
    print("Seeding database...")
    
    # 1. Create superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')
        print("Superuser created (admin / admin12345)")
    else:
        print("Superuser admin already exists")
        
    # 2. Create categories
    categories = {}
    cat_names = ["Electronics", "Fashion", "Home & Living", "Books"]
    for name in cat_names:
        cat, created = Category.objects.get_or_create(name=name)
        categories[name] = cat
        if created:
            print(f"Category '{name}' created")
            
    # 3. Create products
    products_data = [
        # Electronics
        {
            "category": "Electronics",
            "name": "Quantum Pro Headphones",
            "price": 149.99,
            "description": "Experience premium audio with hybrid active noise cancellation, 40-hour battery life, and high-fidelity sound. Crafted for comfort and everyday listening.",
            "stock": 15
        },
        {
            "category": "Electronics",
            "name": "Aura Smart Watch Series 5",
            "price": 249.50,
            "description": "Track your health metrics, receive instant notifications, and stay connected with the Aura Smart Watch. Features an always-on Retina display and water resistance up to 50m.",
            "stock": 8
        },
        {
            "category": "Electronics",
            "name": "Lumina Mechanical Keyboard",
            "price": 89.99,
            "description": "Tactile, responsive mechanical switches with customizable RGB backlighting. Sleek aluminum top plate and durable double-shot PBT keycaps for intense gaming or daily coding.",
            "stock": 25
        },
        # Fashion
        {
            "category": "Fashion",
            "name": "Nomad Canvas Backpack",
            "price": 65.00,
            "description": "Weatherproof waxed canvas backpack featuring premium leather accents, padded laptop sleeve, and multiple quick-access pockets. Ideal for daily commute or weekend adventures.",
            "stock": 12
        },
        {
            "category": "Fashion",
            "name": "Classic Merino Wool Sweater",
            "price": 79.00,
            "description": "Knit from 100% fine Italian Merino wool. Incredibly soft, breathable, and temperature-regulating. A timeless classic designed for layers.",
            "stock": 20
        },
        # Home & Living
        {
            "category": "Home & Living",
            "name": "AeroPure Smart Air Purifier",
            "price": 120.00,
            "description": "True HEPA filter captures 99.97% of airborne particles, smoke, dust, and pollen. Ultra-quiet operation and smart app connectivity to monitor air quality in real-time.",
            "stock": 5
        },
        {
            "category": "Home & Living",
            "name": "Minimalist Ceramic Coffee Dripper Set",
            "price": 45.00,
            "description": "Handcrafted matte ceramic V60 dripper with heat-resistant glass carafe. Elegant design that delivers a perfect, clean pour-over coffee extraction every morning.",
            "stock": 30
        },
        # Books
        {
            "category": "Books",
            "name": "Architects of the Digital Age",
            "price": 19.99,
            "description": "An engaging narrative charting the history of software engineering, artificial intelligence, and the visionaries who built the systems shaping modern society.",
            "stock": 50
        },
        {
            "category": "Books",
            "name": "Designing Interfaces for Tomorrow",
            "price": 24.95,
            "description": "A comprehensive guide to UX/UI design theory, interaction patterns, and human psychology. Essential reading for designers and product builders.",
            "stock": 40
        }
    ]
    
    for prod in products_data:
        cat = categories[prod["category"]]
        product, created = Product.objects.get_or_create(
            name=prod["name"],
            defaults={
                "category": cat,
                "price": prod["price"],
                "description": prod["description"],
                "stock": prod["stock"]
            }
        )
        if created:
            print(f"Product '{prod['name']}' created")
        else:
            # Update stock and price if it exists
            product.price = prod["price"]
            product.stock = prod["stock"]
            product.save()
            print(f"Product '{prod['name']}' updated")
            
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_db()
