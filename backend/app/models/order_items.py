from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy.orm import relationship


class Order_Item(db.Model):
    __tablename__ = 'order_items'
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("orders.id")))
    product_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("products.id")))
    quantity = db.Column(db.Integer)
    item_price = db.Column(db.Numeric(precision=8, scale = 2), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product',  back_populates='order_items')

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.item_price,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
