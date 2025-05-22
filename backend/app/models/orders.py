from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy.orm import relationship


class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")))
    shipping_address = db.Column(db.String(255))
    order_status = db.Column(db.String(15), default="processing")
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = relationship("User", back_populates="orders")
    order_items = relationship("Order_Item", back_populates="order", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "order_date": self.created_at.isoformat(),
            "order_status": self.order_status,
            "shipping_address": self.shipping_address,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
