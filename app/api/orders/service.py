from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException


class OrdersService:
    def view_orders(self, all_orders: Session, limit: int, offset: int):
        skip = offset * limit
        orders = all_orders.query(models.Order).limit(limit).offset(skip).all()
        orders_list = []
        for order in orders:
            orders_list.append(schemas.Courier(
                                courier_id=order.id,
                                courier_type=order.courier_type,
                                regions=order.regions,
                                working_hours=order.working_hours
                                ))
        return orders_list


    def read_order(self, orders: Session, courier_id):
        order = orders.query(models.Order).filter(models.Order.id == courier_id).first()
        order_info = schemas.Order(
                        order_id=order.id,
                        weight=order.weight,
                        regions=order.regions,
                        delivery_hours=order.delivery_hours,
                        cost=order.cost)
        return order_info


    def create_order(self, db, orders):
        for order in orders.orders:
            db_order = models.Order(
                weight=order.weight,
                regions=order.regions,
                delivery_hours=order.delivery_hours,
                cost=order.cost
            )
            db.add(db_order)
        db.commit()
        return db_order


    def complete_order(self, db, orders):
        a = []
        for order in orders.complete_info:
            try:
                order_model = db.query(models.Order).filter(models.Order.id == order.order_id).first()
                if not order_model.courier_id or order_model.courier_id != order.courier_id:
                    raise HTTPException(status_code=400, detail="Bad Request")
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
                a.append(b)
            except IndexError:
                raise HTTPException(status_code=400, detail="Bad Request")
        return a
