import random
from app.models import db, User, Product
from sqlalchemy.sql import text
from app.models.db import environment, SCHEMA

def seed_favorites():
    
    if environment == "production":
        db.session.execute(text(f"SET search_path TO {SCHEMA}"))

    users = User.query.all()
    products = Product.query.all()

    for user in users:
        # 50% chance this user won't favorite anything
        if random.random() < 0.5:
            continue

        # Get products NOT sold by this user
        non_owned = [p for p in products if p.seller_id != user.id]

        if not non_owned:
            continue

        # Randomly select 1–2 non-owned products to favorite
        num_to_favorite = min(len(non_owned), random.randint(1, 2))
        chosen = random.sample(non_owned, k=num_to_favorite)

        for product in chosen:
            if product not in user.favorite_products:
                user.favorite_products.append(product)

    db.session.commit()


def undo_favorites():
    if environment == "production":
        db.session.execute(text(f"SET search_path TO {SCHEMA}"))
        db.session.execute(f"TRUNCATE table favorites RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM favorites"))
    db.session.commit()
