"""
Pydantic schemas for Astronomy Picture endpoints
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime


class MediaTypeEnum(str):
    IMAGE = "image"
    VIDEO = "video"
    OTHER = "other"


class AstronomyPictureBase(BaseModel):
    """Base schema for astronomy picture"""
    title: str = Field(..., min_length=1, max_length=500)
    explanation: str = Field(..., min_length=1)


class AstronomyPictureCreate(AstronomyPictureBase):
    """Schema for creating a new astronomy picture"""
    date: date
    media_type: str = Field(default="image")
    media_url: Optional[str] = None
    hd_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    copyright: Optional[str] = None
    keywords: Optional[str] = None


class AstronomyPictureUpdate(BaseModel):
    """Schema for updating an astronomy picture"""
    title: Optional[str] = None
    explanation: Optional[str] = None
    media_url: Optional[str] = None
    hd_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    copyright: Optional[str] = None
    keywords: Optional[str] = None
    media_type: Optional[str] = None


class AstronomyPictureResponse(AstronomyPictureBase):
    """Schema for astronomy picture response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    media_type: str
    media_url: Optional[str] = None
    hd_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    copyright: Optional[str] = None
    year: int
    month: int
    keywords: Optional[str] = None
    keywords_list: Optional[List[str]] = None

    @classmethod
    def from_orm_with_keywords(cls, obj):
        """Convert ORM object to response with parsed keywords"""
        media_type = obj.media_type
        if hasattr(media_type, 'value'):
            media_type = media_type.value

        return cls(
            id=obj.id,
            date=obj.date,
            title=obj.title,
            explanation=obj.explanation,
            media_type=media_type,
            media_url=obj.media_url,
            hd_url=obj.hd_url,
            thumbnail_url=obj.thumbnail_url,
            copyright=obj.copyright,
            year=obj.year,
            month=obj.month,
            keywords=obj.keywords,
            keywords_list=[k.strip() for k in obj.keywords.split(",")] if obj.keywords else []
        )


class AstronomyPictureListResponse(BaseModel):
    """Paginated list response for astronomy pictures"""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[AstronomyPictureResponse]


class AstronomyPictureSearchParams(BaseModel):
    """Search parameters for filtering pictures"""
    query: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    media_type: Optional[str] = None
    year: Optional[int] = None
    month: Optional[int] = None
    keyword: Optional[str] = None
