from fastapi import APIRouter
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
import psycopg2
from database import SessionLocal
from .service import CouriersService


router = APIRouter(tags=['courier-controller'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/couriers/")
async def root(service: CouriersService = Depends(CouriersService), db: Session = Depends(get_db), limit: int = 1, offset: int = 0):
    return service.view_couriers(db, limit, offset)


@router.post("/couriers/")
async def root(couriers: schemas.AddCouriers, db: Session = Depends(get_db)):
    return CouriersService.create_courier(db, couriers)


@router.get("/couriers/{courier_id}")
async def root(courier_id: int, db: Session = Depends(get_db)):
    db_courier = CouriersService.read_courier(db, courier_id)
    return schemas.Courier(courier_id=db_courier.id, courier_type=db_courier.courier_type, regions=db_courier.regions, working_hours=db_courier.working_hours)


@router.get("/couriers/meta-info/{courier_id}")
async def root(courier_id: int, db: Session = Depends(get_db), startDate: str = '0', endDate: str = '0'):
    print(startDate, endDate)

    orders = db.query(models.Order).filter(models.Order.courier_id == courier_id)



    print(orders)
    return 0
