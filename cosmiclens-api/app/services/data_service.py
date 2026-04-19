"""
Data import service for loading APOD data into the database
"""
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
import logging
import re

from app.models.astronomy_picture import AstronomyPicture, MediaType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataImportService:
    """Service for importing NASA APOD data into the database"""

    def __init__(self, db: Session):
        self.db = db

    def parse_media_type(self, media_url: Optional[str], csv_media_type: Optional[str] = None) -> str:
        """Determine media type from URL or CSV data"""
        # Use CSV media_type if available and valid
        if csv_media_type:
            csv_type = str(csv_media_type).lower().strip()
            if csv_type in ['image', 'video', 'other']:
                return csv_type

        # Fallback to URL detection
        if not media_url:
            return MediaType.OTHER

        lower_url = media_url.lower()

        if any(ext in lower_url for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']) or 'image' in lower_url:
            return MediaType.IMAGE
        elif any(ext in lower_url for ext in ['.mp4', '.youtube', 'vimeo', 'video']):
            return MediaType.VIDEO
        return MediaType.OTHER

    def clean_explanation(self, text: str) -> str:
        """Clean up explanation text by removing extra headers"""
        if not text:
            return ""
        # Remove "Today's Picture: XX/XX/XXXX" header if present
        text = re.sub(r"Today's Picture:.*?(?=Explanation:)", "", text, flags=re.IGNORECASE | re.DOTALL)
        # Remove "Explanation:" prefix
        text = re.sub(r"Explanation:\s*", "", text, flags=re.IGNORECASE)
        # Clean up multiple spaces
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def import_from_csv(self, csv_path: str) -> dict:
        """
        Import astronomy pictures from a CSV file.

        Expected CSV columns:
        - date, explanation, hdurl, media_type, service_version, title, url, copyright

        Args:
            csv_path: Path to the CSV file

        Returns:
            Dictionary with import statistics
        """
        logger.info(f"Starting import from {csv_path}")

        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} records from CSV")
            logger.info(f"Columns: {list(df.columns)}")
        except Exception as e:
            logger.error(f"Failed to read CSV: {e}")
            return {"success": False, "error": str(e)}

        imported = 0
        updated = 0
        errors = 0

        for _, row in df.iterrows():
            try:
                # Parse date
                date_str = str(row.get('date', '')).strip()
                if not date_str or date_str == 'nan':
                    errors += 1
                    continue

                # Handle different date formats
                try:
                    date = pd.to_datetime(date_str).date()
                except:
                    logger.warning(f"Could not parse date: {date_str}")
                    errors += 1
                    continue

                # Get media_type from CSV
                csv_media_type = row.get('media_type') if pd.notna(row.get('media_type')) else None

                # Check if already exists
                existing = self.db.query(AstronomyPicture).filter(
                    AstronomyPicture.date == date
                ).first()

                if existing:
                    # Update existing record
                    existing.title = str(row.get('title', ''))[:500]
                    existing.explanation = self.clean_explanation(str(row.get('explanation', '')))
                    existing.media_url = str(row.get('url', '')) if pd.notna(row.get('url')) else None
                    existing.hd_url = str(row.get('hdurl', '')) if pd.notna(row.get('hdurl')) else None
                    existing.copyright = str(row.get('copyright', '')) if pd.notna(row.get('copyright')) else None
                    existing.media_type = self.parse_media_type(
                        row.get('url'),
                        csv_media_type
                    )
                    updated += 1
                else:
                    # Create new record
                    media_type = self.parse_media_type(
                        row.get('url'),
                        csv_media_type
                    )

                    picture = AstronomyPicture(
                        date=date,
                        title=str(row.get('title', ''))[:500],
                        explanation=self.clean_explanation(str(row.get('explanation', ''))),
                        media_url=str(row.get('url', '')) if pd.notna(row.get('url')) else None,
                        hd_url=str(row.get('hdurl', '')) if pd.notna(row.get('hdurl')) else None,
                        thumbnail_url=None,
                        copyright=str(row.get('copyright', '')) if pd.notna(row.get('copyright')) else None,
                        keywords=None,
                        media_type=media_type,
                        year=date.year,
                        month=date.month
                    )
                    self.db.add(picture)
                    imported += 1

                # Commit in batches
                if (imported + updated) % 100 == 0:
                    self.db.commit()
                    logger.info(f"Progress: {imported} imported, {updated} updated, {errors} errors")

            except Exception as e:
                logger.error(f"Error processing row: {e}")
                errors += 1
                continue

        # Final commit
        self.db.commit()

        logger.info(f"Import complete: {imported} imported, {updated} updated, {errors} errors")

        return {
            "success": True,
            "imported": imported,
            "updated": updated,
            "errors": errors,
            "total": imported + updated
        }

    def get_import_status(self) -> dict:
        """Get current database status"""
        total = self.db.query(AstronomyPicture).count()
        images = self.db.query(AstronomyPicture).filter(
            AstronomyPicture.media_type == MediaType.IMAGE
        ).count()
        videos = self.db.query(AstronomyPicture).filter(
            AstronomyPicture.media_type == MediaType.VIDEO
        ).count()
        other = self.db.query(AstronomyPicture).filter(
            AstronomyPicture.media_type == MediaType.OTHER
        ).count()

        return {
            "total_pictures": total,
            "images": images,
            "videos": videos,
            "other": other
        }

    def clear_database(self) -> dict:
        """Clear all pictures from database"""
        count = self.db.query(AstronomyPicture).delete()
        self.db.commit()
        return {"deleted": count}
