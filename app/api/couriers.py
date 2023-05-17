from fastapi import APIRouter
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
import psycopg2
from database import SessionLocal

router = APIRouter(tags=['courier-controller'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/couriers/")
async def root(db: Session = Depends(get_db), limit: int = 1, offset: int = 0):
    couriers = db.query(models.Courier).all()
    couriers_list = []
    for courier in couriers:
        couriers_list.append(schemas.Courier(courier_id=courier.id, courier_type=courier.courier_type, regions=courier.regions, working_hours=courier.working_hours))
    return couriers_list


@router.post("/couriers/")
async def root(couriers: schemas.AddCouriers, db: Session = Depends(get_db)):
    for courier in couriers.couriers:
        print(courier)
        # print(couriers.couriers)
        db_courier = models.Courier(courier_type=courier.courier_type, regions=courier.regions,
                                    working_hours=courier.working_hours)
        db.add(db_courier)
    db.commit()
    # db.refresh(db_courier)
    return db_courier


@router.get("/couriers/{courier_id}")
async def root(courier_id: int, db: Session = Depends(get_db)):
    db_courier = read_courier(db, courier_id)
    return schemas.Courier(courier_id=db_courier.id, courier_type=db_courier.courier_type, regions=db_courier.regions, working_hours=db_courier.working_hours)



def read_courier(couriers: Session, courier_id):
    return couriers.query(models.Courier).filter(models.Courier.id == courier_id).first()


def view_couriers(couriers: Session, limit: int, offset: int):
    skip = offset * limit
    return couriers.query(models.Courier).limit(limit).offset(skip).all()


def create_courier(db: Session, courier: schemas.CreateCourier):
    db_courier = models.Courier(
        courier_type=courier.courier_type,
        regions=courier.regions,
        working_hours=courier.working_hours
    )
    db.add(db_courier)
    db.commit()
    db.refresh(db_courier)
    return db_courier