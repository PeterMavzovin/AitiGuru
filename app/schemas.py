from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    quantity: int

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    class Config:
        orm_mode = True
