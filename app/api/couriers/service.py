from sqlalchemy.orm import Session

import models
import schemas


class CouriersService:

    def read_courier(self, couriers: Session, courier_id):
        courier = couriers.query(models.Courier).filter(models.Courier.id == courier_id).first()
        courier_info = schemas.Courier(courier_id=courier.id, courier_type=courier.courier_type,
                                       regions=courier.regions, working_hours=courier.working_hours, rating=0,
                                       earnings=0)
        return courier_info

    def view_couriers(self, all_couriers, limit: int, offset: int):
        skip = offset * limit
        couriers = all_couriers.query(models.Courier).limit(limit).offset(skip).all()
        couriers_list = []
        for courier in couriers:
            couriers_list.append(
                schemas.Courier(courier_id=courier.id, courier_type=courier.courier_type, regions=courier.regions,
                                working_hours=courier.working_hours, rating=0, earnings=0))
        return couriers_list

    def create_courier(self, db, couriers):
        for courier in couriers.couriers:
            db_courier = models.Courier(
                courier_type=courier.courier_type,
                regions=courier.regions,
                working_hours=courier.working_hours
            )
            db.add(db_courier)
        db.commit()
        return db_courier


    def calculate_earnings(self, orders):
        return 0
