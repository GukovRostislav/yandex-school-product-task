from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ARRAY
from sqlalchemy.orm import relationship
from database import Base, engine


class Courier(Base):
    __tablename__ = "couriers"

    id = Column(Integer, primary_key=True, index=True)
    courier_type = Column(String)
    regions = Column(ARRAY(Integer))
    working_hours = Column(ARRAY(String))


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Integer)
    regions = Column(Integer)
    delivery_hours = Column(ARRAY(String))
    cost = Column(Integer)
    completed_time = Column(String)
    courier_id = Column(Integer, ForeignKey('couriers.id'), nullable=True)
    courier = relationship('Courier', backref='orders')


Base.metadata.create_all(bind=engine)
