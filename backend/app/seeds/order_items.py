from app.models import db, OrderItem, Order, Product, environment, SCHEMA
from sqlalchemy.sql import text
import random

def seed_order_items():
    orders = Order.query.all()
    products = Product.query.all()

    if not orders or not products:
        print("⚠️ Orders or Products must be seeded first.")
        return

    order_items = []

    for order in orders:
        # Pick 2–3 products that this user did NOT sell
        available_products = [p for p in products if p.seller_id != order.user_id]
        if len(available_products) < 1:
            continue

        selected_products = random.sample(available_products, min(3, len(available_products)))

        for product in selected_products:
            item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=random.randint(1, 5),
                item_price=product.product_price
            )
            order_items.append(item)

    db.session.add_all(order_items)
    db.session.commit()

def undo_order_items():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.order_items RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM order_items"))
    db.session.commit()
