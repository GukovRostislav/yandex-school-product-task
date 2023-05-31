from fastapi import APIRouter
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import schemas
from database import SessionLocal
from .service import OrdersService

router = APIRouter(tags=['order-controller'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/orders/")
async def root(service=Depends(OrdersService), db: Session = Depends(get_db), limit: int = 1, offset: int = 0):
    return service.view_orders(db, limit, offset)


@router.post("/orders/")
async def root(orders: schemas.AddOrders, service=Depends(OrdersService), db: Session = Depends(get_db)):
    return service.create_order(db, orders)


@router.post("/orders/complete/")
async def root(orders: schemas.CompleteOrders, service=Depends(OrdersService), db: Session = Depends(get_db)):
    return service.complete_order(db, orders)


@router.get("/orders/{order_id}")
async def root(order_id: int, service=Depends(OrdersService), db: Session = Depends(get_db)):
    return service.read_order(db, order_id)
