"""Models package"""
from app.models.astronomy_picture import AstronomyPicture
from app.models.collection import Collection, collection_pictures

__all__ = ["AstronomyPicture", "Collection", "collection_pictures"]
