from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import Products


def item_exists(form, field):
    #! checking if item exhists
    product_id = field.data
    item = Products.query.filter(Products.id == product_id).first()
    if not item:
        raise ValidationError('Item does not exhist.')
    if item.quantity == 0:
        raise ValidationError('Item not in stock.')

class OrderItemForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired(), item_exists,])
    quantity = IntegerField(
        'quantity', validators=[DataRequired(), item_exists])
