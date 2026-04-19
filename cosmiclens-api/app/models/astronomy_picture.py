"""
Astronomy Picture model - represents NASA's APOD data
"""
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base


class MediaType:
    """Media type constants (SQLite compatible - using strings instead of enum)"""
    IMAGE = "image"
    VIDEO = "video"
    OTHER = "other"


class AstronomyPicture(Base):
    """
    Astronomy Picture model representing NASA's APOD records.

    Contains detailed information about each astronomy picture including
    title, description, media URLs, copyright information, and metadata.
    """
    __tablename__ = "astronomy_pictures"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    explanation = Column(Text, nullable=False)
    media_url = Column(String(1000))
    hd_url = Column(String(1000))
    media_type = Column(String(20), default=MediaType.IMAGE, nullable=False)
    thumbnail_url = Column(String(1000))
    copyright = Column(String(500))
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    keywords = Column(Text)  # Comma-separated keywords

    # Relationships
    collections = relationship(
        "Collection",
        secondary="collection_pictures",
        back_populates="pictures"
    )

    def __repr__(self):
        return f"<AstronomyPicture(id={self.id}, title='{self.title}', date={self.date})>"
