from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
import psycopg2
from database import SessionLocal

router = APIRouter(tags=['order-controller'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/orders/")
async def root(db: Session = Depends(get_db), limit: int = 1, offset: int = 0):
    return view_orders(db, limit, offset)


@router.post("/orders/")
async def root(orders: schemas.AddOrders, db: Session = Depends(get_db)):
    for order in orders.orders:
        print(order)
        db_order = models.Order(
                                weight=order.weight,
                                regions=order.regions,
                                delivery_hours=order.delivery_hours,
                                cost=order.cost
                                )
        db.add(db_order)
    db.commit()
    # db.refresh(db_order)
    return db_order


@router.post("/orders/complete/")
async def root(orders: schemas.CompleteOrders, db: Session = Depends(get_db)):
    a = []
    for order in orders.complete_info:
        try:
            print(order)

            order_model = db.query(models.Order).filter(models.Order.id == order.order_id).first()
            if not order_model.courier_id or order_model.courier_id != order.courier_id:
                raise HTTPException(status_code=400, detail="Bad Request")
            print(order_model.__dict__)
            order_model.completed_time = order.complete_time
            order_model.courier_id = order.courier_id

            b = schemas.Order(
                            order_id=order_model.id,
                            weight=order_model.weight,
                            regions=order_model.regions,
                            delivery_hours=order_model.delivery_hours,
                            cost=order_model.cost,
                            completed_time=order_model.completed_time
                            )

            db.commit()

        #print(order_model.completed_time)
            a.append(b)

        except IndexError:
            raise HTTPException(status_code=400, detail="Bad Request")


    print(a)
    return a


@router.get("/orders/{order_id}")
async def root(order_id: int, db: Session = Depends(get_db)):
    db_order = read_order(db, order_id)
    return schemas.Order(
                        order_id=db_order.id,
                        weight=db_order.weight,
                        regions=db_order.regions,
                        delivery_hours=db_order.delivery_hours,
                        cost=db_order.cost
                         )


def view_orders(orders: Session, limit: int, offset: int):
    skip = offset * limit
    return orders.query(models.Order).limit(limit).offset(skip).all()


def read_order(orders: Session, courier_id):
    return orders.query(models.Order).filter(models.Order.id == courier_id).first()
