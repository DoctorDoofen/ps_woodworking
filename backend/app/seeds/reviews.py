from app.models import db, User, Product, Review, environment, SCHEMA
from sqlalchemy.sql import text
import random


def seed_reviews():
    try:
        if environment == "production":
            db.session.execute(text(f"SET search_path TO {SCHEMA}"))
        # Get all products
        for product in Product.query.all():
            product_id = product.id
            seller_id = product.seller_id
            # Get all users who are not sellers of the product
            for user in User.query.filter(User.id != seller_id).all():
                review = Review(
                    user_id = user.id,
                    product_id = product_id,
                    rating = random.randint(1,5),
                )
                if review.rating <= 2:
                    review.review = "It was not very good experiance. Don't recommend."
                elif review.rating >2 and review.rating <=3:
                    review.review = "The product did what I wanted but I expected better."
                else:
                    review.review = "This is excellent product!"
                db.session.add(review)
        db.session.commit()
    except BaseException as e:
        print(f'Exception occurred: {e}\nRollback all transactions.')
        db.session.rollback()
        
def undo_reviews():
    if environment == 'production':
        db.session.execute(text(f"SET search_path TO {SCHEMA}"))
        db.session.execute(f"TRUNCATE table reviews RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reviews"))

    db.session.commit()
        