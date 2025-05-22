from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_users():

    if environment == "production":
        db.session.execute(text(f"SET search_path TO {SCHEMA}"))

    demo = User(
        username='Demo', first_name="Demo", email='demo@aa.io', password='password')
    marnie = User(
        username='marnie', first_name="marnie", email='marnie@aa.io', password='password')
    bobbie = User(
        username='bobbie', first_name="bobbie", email='bobbie@aa.io', password='password')
    seller_1 = User(
        seller = True, username='seller_1', first_name="seller_1", email='seller_1@aa.io', password='password')
    seller_2 = User(
        seller = True, username='seller_2', first_name="seller_2", email='seller_2@aa.io', password='password')

    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)
    db.session.add(seller_1)
    db.session.add(seller_2)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(text(f"SET search_path TO {SCHEMA}"))
        db.session.execute(f"TRUNCATE table orders RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE table users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM orders"))
        db.session.execute(text("DELETE FROM users"))
    
    db.session.commit()

