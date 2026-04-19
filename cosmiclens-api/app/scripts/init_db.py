"""
Database initialization script

This script:
1. Creates all database tables
2. Optionally imports data from CSV
3. Shows import statistics
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.database import Base, engine, SessionLocal
from app.models import AstronomyPicture, Collection
from app.services.data_service import DataImportService


def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def import_data(csv_path: str = None):
    """
    Import data from CSV file.

    Args:
        csv_path: Path to CSV file. If None, will look for default location.
    """
    if csv_path is None:
        # Default path relative to project root
        csv_path = Path(__file__).parent.parent.parent / "data" / "nasa_apod.csv"

    csv_path = Path(csv_path)

    if not csv_path.exists():
        print(f"\n⚠️  CSV file not found at: {csv_path}")
        print("\nTo import data, you need to:")
        print("1. Download the NASA APOD dataset from Kaggle:")
        print("   https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026")
        print("2. Place the CSV file in the data/ directory")
        print("3. Run this script again: python -m app.scripts.init_db")
        return None

    db = SessionLocal()
    try:
        service = DataImportService(db)

        print(f"\n📥 Importing data from: {csv_path}")
        result = service.import_from_csv(str(csv_path))

        if result["success"]:
            print(f"\n✅ Import completed successfully!")
            print(f"   - New records imported: {result['imported']}")
            print(f"   - Records updated: {result['updated']}")
            print(f"   - Errors: {result['errors']}")
            print(f"   - Total records: {result['total']}")

            # Show current status
            status = service.get_import_status()
            print(f"\n📊 Current database status:")
            print(f"   - Total pictures: {status['total_pictures']}")
            print(f"   - Images: {status['images']}")
            print(f"   - Videos: {status['videos']}")
            print(f"   - Other: {status['other']}")
        else:
            print(f"\n❌ Import failed: {result['error']}")

        return result
    finally:
        db.close()


def show_status():
    """Show current database status"""
    db = SessionLocal()
    try:
        service = DataImportService(db)
        status = service.get_import_status()

        print("\n📊 Current database status:")
        print(f"   - Total pictures: {status['total_pictures']}")
        print(f"   - Images: {status['images']}")
        print(f"   - Videos: {status['videos']}")
        print(f"   - Other: {status['other']}")

        return status
    finally:
        db.close()


def clear_data():
    """Clear all data from database"""
    db = SessionLocal()
    try:
        service = DataImportService(db)
        result = service.clear_database()
        print(f"\n🗑️  Cleared {result['deleted']} records from database")
        return result
    finally:
        db.close()


def main():
    """Main function for command line usage"""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "init":
            init_db()
        elif command == "import":
            csv_path = sys.argv[2] if len(sys.argv) > 2 else None
            import_data(csv_path)
        elif command == "status":
            show_status()
        elif command == "clear":
            confirm = input("Are you sure you want to clear all data? (yes/no): ")
            if confirm.lower() == "yes":
                clear_data()
        elif command == "reset":
            confirm = input("This will delete all data. Continue? (yes/no): ")
            if confirm.lower() == "yes":
                init_db()
                clear_data()
                print("Database reset complete.")
        else:
            print(f"Unknown command: {command}")
            print_help()
    else:
        # Interactive mode
        print("\n🌌 CosmicLens API - Database Setup")
        print("=" * 40)

        init_db()
        print()

        csv_path = Path(__file__).parent.parent.parent / "data" / "nasa_apod.csv"
        if csv_path.exists():
            import_data(str(csv_path))
        else:
            print("\n📁 No data file found. Please download the dataset first.")
            print("   Run 'python -m app.scripts.init_db import <csv_path>' after downloading.")

        show_status()


def print_help():
    """Print usage help"""
    print("\nUsage:")
    print("  python -m app.scripts.init_db           # Interactive setup")
    print("  python -m app.scripts.init_db init      # Initialize database")
    print("  python -m app.scripts.init_db import    # Import from default CSV")
    print("  python -m app.scripts.init_db import <path>  # Import from specific CSV")
    print("  python -m app.scripts.init_db status    # Show database status")
    print("  python -m app.scripts.init_db clear      # Clear all data")
    print("  python -m app.scripts.init_db reset      # Reset database")


if __name__ == "__main__":
    main()
