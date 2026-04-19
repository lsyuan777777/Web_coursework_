"""
Pydantic schemas for Collection endpoints
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class CollectionBase(BaseModel):
    """Base schema for collection"""
    name: str = Field(..., min_length=1, max_length=200, description="Collection name")
    description: Optional[str] = Field(None, description="Collection description")


class CollectionCreate(CollectionBase):
    """Schema for creating a new collection"""
    is_public: bool = Field(default=True, description="Whether collection is public")


class CollectionUpdate(BaseModel):
    """Schema for updating a collection"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_public: Optional[bool] = None


class CollectionResponse(CollectionBase):
    """Schema for collection response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_public: bool
    picture_count: int
    created_at: datetime
    updated_at: datetime


class AddPictureToCollection(BaseModel):
    """Schema for adding a picture to collection"""
    picture_id: int = Field(..., description="ID of the picture to add")


class CollectionPictureSummary(BaseModel):
    """Summary of a picture within a collection"""
    id: int
    date: datetime
    title: str
    media_type: str
    media_url: Optional[str] = None
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CollectionDetailResponse(CollectionResponse):
    """Detailed collection response with pictures"""
    pictures: List[CollectionPictureSummary] = []


class CollectionListResponse(BaseModel):
    """Paginated list response for collections"""
    total: int
    page: int
    page_size: int
    items: List[CollectionResponse]
