from sqlalchemy.orm import Session
from . import models

def add_product_to_order(db: Session, order_id: int, product_id: int, quantity: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        return None, 'order_not_found'
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return None, 'product_not_found'
    if product.stock < quantity:
        return None, 'not_enough_stock'
    order_item = db.query(models.OrderItem).filter_by(order_id=order_id, product_id=product_id).first()
    if order_item:
        if product.stock < order_item.quantity + quantity:
            return None, 'not_enough_stock'
        order_item.quantity += quantity
    else:
        order_item = models.OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
        db.add(order_item)
    product.stock -= quantity
    db.commit()
    db.refresh(order_item)
    return order_item, None
