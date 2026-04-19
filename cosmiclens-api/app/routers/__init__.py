"""Routers package"""
from app.routers.pictures import router as pictures_router
from app.routers.collections import router as collections_router
from app.routers.analytics import router as analytics_router

__all__ = ["pictures_router", "collections_router", "analytics_router"]
