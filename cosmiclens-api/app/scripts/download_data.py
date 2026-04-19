"""
Data download script for NASA APOD dataset

This script helps download the dataset from Kaggle.
You need to have a Kaggle account and API token.

Usage:
    python -m app.scripts.download_data
"""
import os
import sys
from pathlib import Path

def check_kaggle_installed():
    """Check if kaggle package is installed"""
    try:
        import kaggle
        return True
    except ImportError:
        return False

def download_dataset():
    """Download NASA APOD dataset from Kaggle"""
    if not check_kaggle_installed():
        print("Installing kaggle package...")
        os.system("pip install kaggle")

    from kaggle.api.kaggle_api_extended import KaggleApi

    print("Authenticating with Kaggle...")
    api = KaggleApi()
    api.authenticate()

    # Dataset identifier
    dataset = "ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026"

    # Get data directory
    script_dir = Path(__file__).parent.parent.parent
    data_dir = script_dir / "data"
    data_dir.mkdir(exist_ok=True)

    print(f"\nDownloading dataset: {dataset}")
    print(f"Destination: {data_dir}")

    # Download dataset
    api.dataset_download_files(
        dataset,
        path=str(data_dir),
        unzip=True
    )

    print("\n✅ Download complete!")

    # List files
    print("\nDownloaded files:")
    for f in data_dir.iterdir():
        if f.is_file():
            size = f.stat().st_size / (1024 * 1024)  # MB
            print(f"  - {f.name} ({size:.2f} MB)")

def manual_download_instructions():
    """Print instructions for manual download"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║           Manual Download Instructions                          ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  1. Go to: https://www.kaggle.com/datasets/ahsanneural/         ║
║     nasa-astronomy-picture-of-the-day-1995-2026                ║
║                                                                ║
║  2. Click the "Download" button                                ║
║                                                                ║
║  3. Extract the ZIP file                                       ║
║                                                                ║
║  4. Copy the CSV file to the data/ directory:                 ║
║                                                                ║
║     cosmiclens-api/data/                                       ║
║                                                                ║
║  5. Run the import script:                                     ║
║     python -m app.scripts.init_db                              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

Dataset Information:
- Name: NASA Astronomy Picture of the Day (1995-2026)
- Records: 11,186+ images
- Source: NASA APOD (Astronomy Picture of the Day)
- License: NASA Media Usage Guidelines
""")

if __name__ == "__main__":
    print("\n🌌 CosmicLens API - Data Download")
    print("=" * 40)

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        manual_download_instructions()
    else:
        try:
            download_dataset()
        except Exception as e:
            print(f"\n⚠️  Automatic download failed: {e}")
            print("\nThis is likely because:")
            print("  - Kaggle API is not configured")
            print("  - You don't have a Kaggle account")
            print("\nPlease follow the manual download instructions.\n")
            manual_download_instructions()
