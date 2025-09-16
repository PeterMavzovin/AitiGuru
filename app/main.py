from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def init_test_data():
    db = SessionLocal()
    # Проверяем, есть ли уже продукты
    if db.query(models.Product).count() == 0:
        products = [
            models.Product(name=f"Product {i}", stock=100 + i * 10) for i in range(1, 6)
        ]
        db.add_all(products)
    # Проверяем, есть ли уже заказы
    if db.query(models.Order).count() == 0:
        orders = [models.Order() for _ in range(1, 4)]
        db.add_all(orders)
    db.commit()
    db.close()

init_test_data()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.put("/orders/{order_id}/items/{product_id}", response_model=schemas.OrderItemResponse,
responses = {
    404: {
        "description": "Order or product not found",
        "content": {
            "application/json": {
                "example": {"detail": "Order or product not found"}
            }
        }
    },
    409: {
        "description": "Not enough stock",
        "content": {
            "application/json": {
                "example": {"detail": "Not enough stock"}
            }
        }
    }
})
def add_item_to_order(order_id: int, product_id: int, item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    order_item, error = crud.add_product_to_order(db, order_id, product_id, item.quantity)
    if error == 'order_not_found':
        raise HTTPException(status_code=404, detail="Order not found")
    if error == 'product_not_found':
        raise HTTPException(status_code=404, detail="Product not found")
    if error == 'not_enough_stock':
        raise HTTPException(status_code=409, detail="Not enough stock")
    return order_item
