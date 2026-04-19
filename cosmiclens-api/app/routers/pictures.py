"""
Astronomy Pictures API endpoints - CRUD operations for APOD data
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from datetime import date

from app.database import get_db
from app.models.astronomy_picture import AstronomyPicture, MediaType
from app.schemas.astronomy_picture import (
    AstronomyPictureCreate,
    AstronomyPictureUpdate,
    AstronomyPictureResponse,
    AstronomyPictureListResponse
)

router = APIRouter(prefix="/pictures", tags=["Astronomy Pictures"])


@router.get("", response_model=AstronomyPictureListResponse)
def list_pictures(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    year: Optional[int] = Query(None, ge=1995, le=2030),
    month: Optional[int] = Query(None, ge=1, le=12),
    media_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """List all astronomy pictures with pagination and filtering."""
    query = db.query(AstronomyPicture)

    if year:
        query = query.filter(AstronomyPicture.year == year)
    if month:
        query = query.filter(AstronomyPicture.month == month)
    if media_type:
        query = query.filter(AstronomyPicture.media_type == media_type)

    total = query.count()
    total_pages = (total + page_size - 1) // page_size

    pictures = query.order_by(AstronomyPicture.date.desc()) \
                    .offset((page - 1) * page_size) \
                    .limit(page_size) \
                    .all()

    return AstronomyPictureListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=[AstronomyPictureResponse.from_orm_with_keywords(p) for p in pictures]
    )


@router.get("/search", response_model=AstronomyPictureListResponse)
def search_pictures(
    q: str = Query(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    media_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Search astronomy pictures by title, explanation, or keywords."""
    query = db.query(AstronomyPicture)

    search_pattern = f"%{q}%"
    query = query.filter(
        or_(
            AstronomyPicture.title.ilike(search_pattern),
            AstronomyPicture.explanation.ilike(search_pattern),
            AstronomyPicture.keywords.ilike(search_pattern)
        )
    )

    if start_date:
        query = query.filter(AstronomyPicture.date >= start_date)
    if end_date:
        query = query.filter(AstronomyPicture.date <= end_date)
    if media_type:
        query = query.filter(AstronomyPicture.media_type == media_type)

    total = query.count()
    total_pages = (total + page_size - 1) // page_size

    pictures = query.order_by(AstronomyPicture.date.desc()) \
                    .offset((page - 1) * page_size) \
                    .limit(page_size) \
                    .all()

    return AstronomyPictureListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=[AstronomyPictureResponse.from_orm_with_keywords(p) for p in pictures]
    )


@router.get("/{picture_id}", response_model=AstronomyPictureResponse)
def get_picture(picture_id: int, db: Session = Depends(get_db)):
    """Get a specific astronomy picture by ID."""
    picture = db.query(AstronomyPicture).filter(AstronomyPicture.id == picture_id).first()
    if not picture:
        raise HTTPException(status_code=404, detail="Picture not found")
    return AstronomyPictureResponse.from_orm_with_keywords(picture)


@router.get("/date/{target_date}", response_model=AstronomyPictureResponse)
def get_picture_by_date(target_date: date, db: Session = Depends(get_db)):
    """Get astronomy picture by specific date."""
    picture = db.query(AstronomyPicture).filter(AstronomyPicture.date == target_date).first()
    if not picture:
        raise HTTPException(status_code=404, detail=f"No picture found for date {target_date}")
    return AstronomyPictureResponse.from_orm_with_keywords(picture)


@router.post("", response_model=AstronomyPictureResponse, status_code=201)
def create_picture(picture: AstronomyPictureCreate, db: Session = Depends(get_db)):
    """Create a new astronomy picture entry."""
    existing = db.query(AstronomyPicture).filter(AstronomyPicture.date == picture.date).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Picture for date {picture.date} already exists. Use PUT to update."
        )

    db_picture = AstronomyPicture(
        date=picture.date,
        title=picture.title,
        explanation=picture.explanation,
        media_url=picture.media_url,
        hd_url=picture.hd_url,
        thumbnail_url=picture.thumbnail_url,
        copyright=picture.copyright,
        keywords=picture.keywords,
        media_type=picture.media_type,
        year=picture.date.year,
        month=picture.date.month
    )

    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)

    return AstronomyPictureResponse.from_orm_with_keywords(db_picture)


@router.put("/{picture_id}", response_model=AstronomyPictureResponse)
def update_picture(
    picture_id: int,
    picture_update: AstronomyPictureUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing astronomy picture."""
    db_picture = db.query(AstronomyPicture).filter(AstronomyPicture.id == picture_id).first()
    if not db_picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    update_data = picture_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_picture, field, value)

    db.commit()
    db.refresh(db_picture)

    return AstronomyPictureResponse.from_orm_with_keywords(db_picture)


@router.delete("/{picture_id}", status_code=204)
def delete_picture(picture_id: int, db: Session = Depends(get_db)):
    """Delete an astronomy picture."""
    db_picture = db.query(AstronomyPicture).filter(AstronomyPicture.id == picture_id).first()
    if not db_picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    db.delete(db_picture)
    db.commit()

    return None


@router.get("/stats/years")
def get_years_with_pictures(db: Session = Depends(get_db)):
    """Get list of years that have pictures"""
    from sqlalchemy import func
    years = db.query(
        AstronomyPicture.year,
        func.count(AstronomyPicture.id).label('count')
    ).group_by(AstronomyPicture.year).order_by(AstronomyPicture.year.desc()).all()

    return [{"year": y.year, "count": y.count} for y in years]


@router.get("/random", response_model=AstronomyPictureResponse)
def get_random_picture(db: Session = Depends(get_db)):
    """Get a random astronomy picture"""
    import random
    count = db.query(AstronomyPicture).count()
    if count == 0:
        raise HTTPException(status_code=404, detail="No pictures in database")

    offset_val = random.randint(0, count - 1)
    picture = db.query(AstronomyPicture).offset(offset_val).limit(1).first()

    return AstronomyPictureResponse.from_orm_with_keywords(picture)
