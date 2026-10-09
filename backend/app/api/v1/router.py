from __future__ import annotations
from fastapi import APIRouter
from app.api.v1 import auth, organizations, users, products, onboarding, orders, wholesaler_inventory, return_acts, retailer_inventory, billing, analytics

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(organizations.router)
api_router.include_router(users.router)
api_router.include_router(products.router)
api_router.include_router(onboarding.router)
api_router.include_router(orders.router)
api_router.include_router(wholesaler_inventory.router)
api_router.include_router(return_acts.router)
api_router.include_router(retailer_inventory.router)
api_router.include_router(billing.router)
api_router.include_router(analytics.router)
