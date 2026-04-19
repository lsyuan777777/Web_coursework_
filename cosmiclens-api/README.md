# CosmicLens API

A RESTful API for exploring NASA's Astronomy Picture of the Day (APOD) dataset - featuring 30+ years of cosmic imagery and scientific explanations.

## Overview

CosmicLens API provides comprehensive access to NASA's iconic APOD collection, allowing developers and enthusiasts to explore, analyze, and integrate astronomical imagery into their applications. The API supports full CRUD operations for personal collections and offers advanced filtering, search, and analytics capabilities.

## Features

- **CRUD Operations**: Full Create, Read, Update, Delete functionality for personal collections
- **Advanced Search**: Filter by date range, media type, keywords, and more
- **Analytics Endpoints**: Statistics on media distribution, temporal trends, and popularity metrics
- **User Collections**: Save favorite astronomy pictures to personal collections
- **RESTful Design**: Industry-standard HTTP methods and status codes
- **Interactive Documentation**: Swagger UI and ReDoc for easy API exploration

## Technology Stack

- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Documentation**: Auto-generated Swagger UI
- **Validation**: Pydantic models

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Kaggle account (for dataset download)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cosmiclens-api.git
cd cosmiclens-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Initialize the database:
```bash
python -m app.scripts.init_db
```

6. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. Access the API:
- API Base URL: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Astronomy Pictures
- `GET /api/v1/pictures` - List all pictures (paginated)
- `GET /api/v1/pictures/{id}` - Get picture by ID
- `POST /api/v1/pictures` - Add new picture
- `PUT /api/v1/pictures/{id}` - Update picture
- `DELETE /api/v1/pictures/{id}` - Delete picture
- `GET /api/v1/pictures/search` - Search pictures

### Collections
- `GET /api/v1/collections` - List user collections
- `GET /api/v1/collections/{id}` - Get collection details
- `POST /api/v1/collections` - Create collection
- `PUT /api/v1/collections/{id}` - Update collection
- `DELETE /api/v1/collections/{id}` - Delete collection
- `POST /api/v1/collections/{id}/pictures` - Add picture to collection
- `DELETE /api/v1/collections/{id}/pictures/{picture_id}` - Remove picture from collection

### Analytics
- `GET /api/v1/analytics/overview` - Dataset overview statistics
- `GET /api/v1/analytics/media-types` - Media type distribution
- `GET /api/v1/analytics/timeline` - Pictures timeline by year/month
- `GET /api/v1/analytics/keywords` - Most common keywords

## Dataset Source

This project uses the NASA Astronomy Picture of the Day dataset from Kaggle:
- **Source**: [NASA Astronomy Picture of the Day (1995-2026)](https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026)
- **Records**: 11,186 images
- **Time Span**: June 1995 - Present

## Project Structure

```
cosmiclens-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── astronomy_picture.py
│   │   └── collection.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── astronomy_picture.py
│   │   └── collection.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── pictures.py
│   │   ├── collections.py
│   │   └── analytics.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── data_service.py
│   └── scripts/
│       ├── __init__.py
│       └── init_db.py
├── data/
│   └── (dataset CSV files)
├── .env.example
├── requirements.txt
└── README.md
```

## Environment Variables

Create a `.env` file with:

```
DATABASE_URL=postgresql://username:password@localhost:5432/cosmiclens
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=cosmiclens
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
API_TITLE=CosmicLens API
API_VERSION=1.0.0
API_DESCRIPTION=A RESTful API for NASA's Astronomy Picture of the Day
```

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- NASA for providing the APOD dataset
- Kaggle for hosting the dataset
- FastAPI team for the excellent framework
