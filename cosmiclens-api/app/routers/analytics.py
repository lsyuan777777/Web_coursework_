"""
Analytics API endpoints - statistics and insights from the APOD dataset
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from collections import Counter

from app.database import get_db
from app.models.astronomy_picture import AstronomyPicture, MediaType

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    """
    Get overall statistics about the APOD dataset.

    Returns total picture count, media type distribution, date range, and more.
    """
    total_pictures = db.query(func.count(AstronomyPicture.id)).scalar()

    if total_pictures == 0:
        return {
            "total_pictures": 0,
            "message": "No pictures in database. Please run the data import script."
        }

    # Media type distribution
    media_counts = db.query(
        AstronomyPicture.media_type,
        func.count(AstronomyPicture.id).label('count')
    ).group_by(AstronomyPicture.media_type).all()

    media_distribution = {
        m.media_type: m.count for m in media_counts
    }

    # Date range
    earliest = db.query(func.min(AstronomyPicture.date)).scalar()
    latest = db.query(func.max(AstronomyPicture.date)).scalar()

    # Year range
    earliest_year = db.query(func.min(AstronomyPicture.year)).scalar()
    latest_year = db.query(func.max(AstronomyPicture.year)).scalar()

    # Pictures with HD URLs
    with_hd = db.query(func.count(AstronomyPicture.id)).filter(
        AstronomyPicture.hd_url.isnot(None)
    ).scalar()

    # Pictures with copyright
    with_copyright = db.query(func.count(AstronomyPicture.id)).filter(
        AstronomyPicture.copyright.isnot(None)
    ).scalar()

    return {
        "total_pictures": total_pictures,
        "media_distribution": media_distribution,
        "pictures_with_hd": with_hd,
        "pictures_with_copyright": with_copyright,
        "date_range": {
            "earliest": earliest.isoformat() if earliest else None,
            "latest": latest.isoformat() if latest else None
        },
        "year_range": {
            "start": earliest_year,
            "end": latest_year
        }
    }


@router.get("/media-types")
def get_media_type_distribution(db: Session = Depends(get_db)):
    """
    Get detailed media type distribution statistics.

    Returns count and percentage for each media type.
    """
    total = db.query(func.count(AstronomyPicture.id)).scalar()

    if total == 0:
        return {"media_types": [], "total": 0}

    media_counts = db.query(
        AstronomyPicture.media_type,
        func.count(AstronomyPicture.id).label('count')
    ).group_by(AstronomyPicture.media_type).all()

    media_types = []
    for m in media_counts:
        percentage = round((m.count / total) * 100, 2)
        media_types.append({
            "type": m.media_type,
            "count": m.count,
            "percentage": percentage
        })

    return {
        "media_types": media_types,
        "total": total
    }


@router.get("/timeline")
def get_timeline(
    granularity: str = Query("year", regex="^(year|month)$", description="year or month"),
    db: Session = Depends(get_db)
):
    """
    Get picture count timeline by year or month.

    - **granularity**: Group by 'year' or 'month'
    """
    if granularity == "year":
        results = db.query(
            AstronomyPicture.year,
            func.count(AstronomyPicture.id).label('count')
        ).group_by(AstronomyPicture.year).order_by(AstronomyPicture.year).all()

        timeline = [{"period": str(r.year), "count": r.count} for r in results]
    else:
        results = db.query(
            AstronomyPicture.year,
            AstronomyPicture.month,
            func.count(AstronomyPicture.id).label('count')
        ).group_by(
            AstronomyPicture.year,
            AstronomyPicture.month
        ).order_by(
            AstronomyPicture.year,
            AstronomyPicture.month
        ).all()

        timeline = [
            {"period": f"{r.year}-{r.month:02d}", "year": r.year, "month": r.month, "count": r.count}
            for r in results
        ]

    return {"granularity": granularity, "timeline": timeline}


@router.get("/keywords")
def get_top_keywords(
    limit: int = Query(20, ge=1, le=100, description="Number of top keywords to return"),
    db: Session = Depends(get_db)
):
    """
    Extract and count most common keywords across all pictures.

    - **limit**: Maximum number of keywords to return (default: 20)
    """
    pictures = db.query(AstronomyPicture.keywords).filter(
        AstronomyPicture.keywords.isnot(None)
    ).all()

    all_keywords = []
    for pic in pictures:
        if pic.keywords:
            keywords = [k.strip().lower() for k in pic.keywords.split(',') if k.strip()]
            all_keywords.extend(keywords)

    if not all_keywords:
        return {"top_keywords": [], "total_unique_keywords": 0}

    keyword_counts = Counter(all_keywords)
    top_keywords = keyword_counts.most_common(limit)

    return {
        "top_keywords": [
            {"keyword": kw, "count": count}
            for kw, count in top_keywords
        ],
        "total_unique_keywords": len(keyword_counts)
    }


@router.get("/copyrights")
def get_copyright_distribution(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get distribution of copyright holders.

    - **limit**: Maximum number of copyright holders to return
    """
    results = db.query(
        AstronomyPicture.copyright,
        func.count(AstronomyPicture.id).label('count')
    ).filter(
        AstronomyPicture.copyright.isnot(None)
    ).group_by(
        AstronomyPicture.copyright
    ).order_by(
        func.count(AstronomyPicture.id).desc()
    ).limit(limit).all()

    return {
        "copyright_holders": [
            {"copyright": r.copyright, "count": r.count}
            for r in results
        ],
        "total_unique_copyrights": db.query(
            func.count(func.distinct(AstronomyPicture.copyright))
        ).filter(AstronomyPicture.copyright.isnot(None)).scalar()
    }


@router.get("/monthly-stats")
def get_monthly_statistics(db: Session = Depends(get_db)):
    """
    Get statistics grouped by month (1-12) to identify best months for astronomy.
    """
    results = db.query(
        AstronomyPicture.month,
        func.count(AstronomyPicture.id).label('count')
    ).group_by(AstronomyPicture.month).order_by(AstronomyPicture.month).all()

    return {
        "monthly_distribution": [
            {"month": r.month, "count": r.count}
            for r in results
        ]
    }


@router.get("/year-summary/{year}")
def get_year_summary(year: int, db: Session = Depends(get_db)):
    """
    Get summary statistics for a specific year.

    - **year**: The year to summarize
    """
    pictures = db.query(AstronomyPicture).filter(AstronomyPicture.year == year).all()

    if not pictures:
        return {"year": year, "message": f"No pictures found for year {year}"}

    total = len(pictures)

    # Media type breakdown
    media_breakdown = {}
    for pic in pictures:
        mt = pic.media_type
        media_breakdown[mt] = media_breakdown.get(mt, 0) + 1

    # Monthly distribution
    monthly = {}
    for pic in pictures:
        monthly[pic.month] = monthly.get(pic.month, 0) + 1

    # First and last picture dates
    sorted_pics = sorted(pictures, key=lambda p: p.date)
    first_date = sorted_pics[0].date
    last_date = sorted_pics[-1].date

    return {
        "year": year,
        "total_pictures": total,
        "media_breakdown": media_breakdown,
        "monthly_distribution": monthly,
        "first_picture": first_date.isoformat(),
        "last_picture": last_date.isoformat()
    }
