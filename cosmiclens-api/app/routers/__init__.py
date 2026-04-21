"""Routers package"""
from app.routers.pictures import router as pictures_router
from app.routers.collections import router as collections_router
from app.routers.analytics import router as analytics_router
from app.routers.auth import router as auth_router

__all__ = ["pictures_router", "collections_router", "analytics_router", "auth_router"]
