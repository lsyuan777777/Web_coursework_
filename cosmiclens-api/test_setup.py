#!/usr/bin/env python3
"""
Quick test script to verify the CosmicLens API project setup.
Run this before initializing the database to check dependencies.
"""
import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("\n📌 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} - Need 3.9+")
        return False

def check_packages():
    """Check if required packages are installed"""
    print("\n📌 Checking required packages...")
    required = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'pandas',
        'psycopg2'
    ]

    all_ok = True
    for package in required:
        try:
            __import__(package)
            print(f"   ✅ {package} - installed")
        except ImportError:
            print(f"   ❌ {package} - NOT installed")
            all_ok = False

    return all_ok

def check_data_file():
    """Check if data file exists"""
    print("\n📌 Checking data file...")
    data_file = Path(__file__).parent.parent / "data" / "nasa_apod_complete.csv"

    if data_file.exists():
        size_mb = data_file.stat().st_size / (1024 * 1024)
        print(f"   ✅ Found: {data_file.name} ({size_mb:.2f} MB)")

        # Quick check of CSV structure
        try:
            import pandas as pd
            df = pd.read_csv(data_file, nrows=3)
            print(f"   ✅ CSV columns: {list(df.columns)}")
            print(f"   ✅ Total records: ~{len(pd.read_csv(data_file))}")
        except Exception as e:
            print(f"   ⚠️  CSV read warning: {e}")
    else:
        print(f"   ❌ Data file not found: {data_file}")
        return False

    return True

def check_database_config():
    """Check database configuration"""
    print("\n📌 Checking database configuration...")
    env_file = Path(__file__).parent.parent / ".env"

    if env_file.exists():
        print(f"   ✅ .env file exists")
        with open(env_file) as f:
            content = f.read()
            if 'postgresql://' in content or 'DATABASE_URL' in content:
                print(f"   ✅ Database URL configured")
            else:
                print(f"   ⚠️  Database URL not configured in .env")
    else:
        print(f"   ⚠️  .env file not found (copy .env.example to .env)")

    return True

def main():
    print("=" * 50)
    print("  🌌 CosmicLens API - Setup Verification")
    print("=" * 50)

    results = []
    results.append(("Python Version", check_python_version()))
    results.append(("Required Packages", check_packages()))
    results.append(("Data File", check_data_file()))
    results.append(("DB Config", check_database_config()))

    print("\n" + "=" * 50)
    print("  Summary")
    print("=" * 50)

    all_ok = True
    for name, ok in results:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"   {status} - {name}")
        if not ok:
            all_ok = False

    print()
    if all_ok:
        print("🎉 All checks passed! You can now:")
        print("   1. Make sure PostgreSQL is running")
        print("   2. Create database: createdb cosmiclens")
        print("   3. Run: python -m app.scripts.init_db")
        print("   4. Start API: uvicorn app.main:app --reload")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")

    print()

if __name__ == "__main__":
    main()
