"""
Collection model - user-created collections of astronomy pictures
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


collection_pictures = Table(
    'collection_pictures',
    Base.metadata,
    Column('collection_id', Integer, ForeignKey('collections.id', ondelete='CASCADE'), primary_key=True),
    Column('picture_id', Integer, ForeignKey('astronomy_pictures.id', ondelete='CASCADE'), primary_key=True),
    Column('added_at', DateTime, default=datetime.utcnow)
)


class Collection(Base):
    """
    Collection model for user-created collections of astronomy pictures.

    Allows users to organize astronomy pictures into themed collections
    with optional descriptions and public/private visibility.

    Each collection belongs to a specific user and is isolated to that user.
    """
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    is_public = Column(Integer, default=0)  # 0 = private (user only), 1 = public
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    picture_count = Column(Integer, default=0)

    # User relationship for isolation
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="collections")
    pictures = relationship(
        "AstronomyPicture",
        secondary=collection_pictures,
        back_populates="collections",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Collection(id={self.id}, name='{self.name}', user_id={self.user_id}, picture_count={self.picture_count})>"
