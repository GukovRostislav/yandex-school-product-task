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
async def root(couriers: schemas.AddCouriers, service: CouriersService = Depends(CouriersService),  db: Session = Depends(get_db)):
    return service.create_courier(db, couriers)


@router.get("/couriers/{courier_id}")
async def root(courier_id: int, db: Session = Depends(get_db), service=Depends(CouriersService)):
    return service.read_courier(db, courier_id)


@router.get("/couriers/meta-info/{courier_id}")
async def root(courier_id: int, service=Depends(CouriersService), db: Session = Depends(get_db), startDate: str = '0', endDate: str = '0'):
    print(startDate, endDate)
    orders = db.query(models.Order).filter(models.Order.courier_id == courier_id)
    print(orders)
    return 0
