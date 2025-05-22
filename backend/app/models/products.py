from .db import db, environment, SCHEMA, add_prefix_for_prod
from flask_login import current_user
from sqlalchemy.orm import relationship

# Join Table for Favorites (User ↔ Product)
favorites_table = db.Table(
    'favorites',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey(add_prefix_for_prod('products.id')), primary_key=True),
    schema=SCHEMA
)

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)
    product_name = db.Column(db.String(50), nullable = False)
    product_price = db.Column(db.Numeric(precision=8, scale = 2), default=0)
    department = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default = 0)
    description = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default=db.func.now())


    user = relationship("User", back_populates="products")
    order_items = relationship('Order_Item', back_populates='product', cascade="all, delete")
    reviews = relationship("Review", back_populates="product", cascade="all, delete")
    images = relationship("Image", back_populates="product", cascade = "all, delete")

     # Users who favorited this product
    favorited_by = relationship(
        "User",
        secondary=favorites_table,
        back_populates="favorite_products"
    )
    
    def to_dict(self, include_image=True):
        from flask_login import current_user  # ensure this works in all routes

        data = {
            "id": self.id,
            "sellerId": self.seller_id,
            "name": self.product_name,
            "price": float(self.product_price),
            "department": self.department,
            "quantity": self.quantity,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "favorite_count": len(self.favorited_by),
            "is_favorited": current_user.is_authenticated and current_user in self.favorited_by
        }

        if include_image:
            preview = next((img.url for img in self.images if img.preview), None)
            data["previewImage"] = preview

        return data

