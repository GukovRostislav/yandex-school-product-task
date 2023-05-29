from fastapi import APIRouter
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
import psycopg2
from database import SessionLocal


class CouriersService:


    def read_courier(self, couriers: Session, courier_id):
        return couriers.query(models.Courier).filter(models.Courier.id == courier_id).first()


    def view_couriers(self, all_couriers, limit: int, offset: int):
        skip = offset * limit
        couriers = all_couriers.query(models.Courier).limit(limit).offset(skip).all()
        couriers_list = []
        for courier in couriers:
            couriers_list.append(schemas.Courier(courier_id=courier.id, courier_type=courier.courier_type, regions=courier.regions, working_hours=courier.working_hours))
        return couriers_list


    def create_courier(self, db, couriers):
        for courier in couriers.couriers:
            print(courier)
            # print(couriers.couriers)
            db_courier = models.Courier(
                                        courier_type=courier.courier_type,
                                        regions=courier.regions,
                                        working_hours=courier.working_hours
                                            )
            db.add(db_courier)
        db.commit()
        return db_courier
