from fastapi import APIRouter

from .couriers.router import router as courier_router
from .orders.router import router as orders_router

router = APIRouter()
router.include_router(courier_router)
router.include_router(orders_router)