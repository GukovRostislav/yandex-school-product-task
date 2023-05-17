from pydantic import BaseModel


class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: list[int]
    working_hours: list[str]
    rating: int
    earnings: int


class CreateCourier(BaseModel):
    courier_type: str
    regions: list[int]
    working_hours: list[str]


class AddCouriers(BaseModel):
    couriers: list[CreateCourier]


class CourierResponse(Courier):
    courier_id: int


class Order(BaseModel):
    order_id: int
    weight: int
    regions: int
    delivery_hours: list[str]
    cost: int
    completed_time: str


class CreateOrder(BaseModel):
    weight: int
    regions: int
    delivery_hours: list[str]
    cost: int


class AddOrders(BaseModel):
    orders: list[CreateOrder]


class Orders(BaseModel):
    orders: list[Order]


class OrderComplete(BaseModel):
    courier_id: int
    order_id: int
    complete_time: str


class CompleteOrders(BaseModel):
    complete_info: list[OrderComplete]
