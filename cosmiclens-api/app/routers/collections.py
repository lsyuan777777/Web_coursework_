"""
Collections API endpoints - CRUD operations for user collections
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.collection import Collection, collection_pictures
from app.models.astronomy_picture import AstronomyPicture
from app.schemas.collection import (
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
    CollectionDetailResponse,
    CollectionListResponse,
    CollectionPictureSummary,
    AddPictureToCollection
)

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.get("", response_model=CollectionListResponse)
def list_collections(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    public_only: bool = Query(False, description="Only show public collections"),
    db: Session = Depends(get_db)
):
    """
    List all collections with pagination.

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20)
    - **public_only**: Filter to show only public collections
    """
    query = db.query(Collection)

    if public_only:
        query = query.filter(Collection.is_public == 1)

    total = query.count()
    total_pages = (total + page_size - 1) // page_size

    collections = query.order_by(Collection.created_at.desc()) \
                       .offset((page - 1) * page_size) \
                       .limit(page_size) \
                       .all()

    return CollectionListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[CollectionResponse.model_validate(c) for c in collections]
    )


@router.get("/{collection_id}", response_model=CollectionDetailResponse)
def get_collection(collection_id: int, db: Session = Depends(get_db)):
    """
    Get a specific collection with its pictures.

    - **collection_id**: Unique identifier of the collection
    """
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Get picture summaries
    picture_links = db.query(collection_pictures).filter(
        collection_pictures.c.collection_id == collection_id
    ).all()

    picture_summaries = []
    for link in picture_links:
        picture = db.query(AstronomyPicture).filter(AstronomyPicture.id == link.picture_id).first()
        if picture:
            picture_summaries.append(CollectionPictureSummary(
                id=picture.id,
                date=picture.date,
                title=picture.title,
                media_type=picture.media_type.value if hasattr(picture.media_type, 'value') else picture.media_type,
                media_url=picture.media_url,
                added_at=link.added_at
            ))

    return CollectionDetailResponse(
        id=collection.id,
        name=collection.name,
        description=collection.description,
        is_public=bool(collection.is_public),
        picture_count=collection.picture_count,
        created_at=collection.created_at,
        updated_at=collection.updated_at,
        pictures=picture_summaries
    )


@router.post("", response_model=CollectionResponse, status_code=201)
def create_collection(collection_data: CollectionCreate, db: Session = Depends(get_db)):
    """
    Create a new collection.

    - **name**: Collection name (required)
    - **description**: Collection description
    - **is_public**: Whether collection is public (default: true)
    """
    db_collection = Collection(
        name=collection_data.name,
        description=collection_data.description,
        is_public=1 if collection_data.is_public else 0
    )

    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)

    return CollectionResponse.model_validate(db_collection)


@router.put("/{collection_id}", response_model=CollectionResponse)
def update_collection(
    collection_id: int,
    collection_update: CollectionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing collection.

    - **collection_id**: ID of the collection to update
    """
    db_collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    update_data = collection_update.model_dump(exclude_unset=True)

    if 'is_public' in update_data:
        update_data['is_public'] = 1 if update_data['is_public'] else 0

    for field, value in update_data.items():
        setattr(db_collection, field, value)

    db_collection.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_collection)

    return CollectionResponse.model_validate(db_collection)


@router.delete("/{collection_id}", status_code=204)
def delete_collection(collection_id: int, db: Session = Depends(get_db)):
    """
    Delete a collection.

    - **collection_id**: ID of the collection to delete
    """
    db_collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    db.delete(db_collection)
    db.commit()

    return None


@router.post("/{collection_id}/pictures", status_code=201)
def add_picture_to_collection(
    collection_id: int,
    picture_data: AddPictureToCollection,
    db: Session = Depends(get_db)
):
    """
    Add a picture to a collection.

    - **collection_id**: ID of the collection
    - **picture_id**: ID of the picture to add
    """
    # Verify collection exists
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Verify picture exists
    picture = db.query(AstronomyPicture).filter(
        AstronomyPicture.id == picture_data.picture_id
    ).first()
    if not picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    # Check if already in collection
    existing = db.query(collection_pictures).filter(
        collection_pictures.c.collection_id == collection_id,
        collection_pictures.c.picture_id == picture_data.picture_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Picture already exists in this collection"
        )

    # Add to collection
    db.execute(
        collection_pictures.insert().values(
            collection_id=collection_id,
            picture_id=picture_data.picture_id
        )
    )

    # Update picture count
    collection.picture_count = db.query(collection_pictures).filter(
        collection_pictures.c.collection_id == collection_id
    ).count()
    collection.updated_at = datetime.utcnow()

    db.commit()

    return {"message": "Picture added to collection successfully"}


@router.delete("/{collection_id}/pictures/{picture_id}", status_code=204)
def remove_picture_from_collection(
    collection_id: int,
    picture_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove a picture from a collection.

    - **collection_id**: ID of the collection
    - **picture_id**: ID of the picture to remove
    """
    # Verify collection exists
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Remove from collection
    result = db.execute(
        collection_pictures.delete().where(
            collection_pictures.c.collection_id == collection_id,
            collection_pictures.c.picture_id == picture_id
        )
    )

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Picture not found in this collection"
        )

    # Update picture count
    collection.picture_count = db.query(collection_pictures).filter(
        collection_pictures.c.collection_id == collection_id
    ).count()
    collection.updated_at = datetime.utcnow()

    db.commit()

    return None


@router.get("/{collection_id}/pictures", response_model=list[CollectionPictureSummary])
def get_collection_pictures(
    collection_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all pictures in a collection.

    - **collection_id**: ID of the collection
    """
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    picture_links = db.query(collection_pictures).filter(
        collection_pictures.c.collection_id == collection_id
    ).all()

    picture_summaries = []
    for link in picture_links:
        picture = db.query(AstronomyPicture).filter(
            AstronomyPicture.id == link.picture_id
        ).first()
        if picture:
            picture_summaries.append(CollectionPictureSummary(
                id=picture.id,
                date=picture.date,
                title=picture.title,
                media_type=picture.media_type.value if hasattr(picture.media_type, 'value') else picture.media_type,
                media_url=picture.media_url,
                added_at=link.added_at
            ))

    return picture_summaries
