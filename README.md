![1776601548569](image/README/1776601548569.png)![1776601553091](image/README/1776601553091.png)![1776601558981](image/README/1776601558981.png)![1776601560384](image/README/1776601560384.png)![1776602021066](image/README/1776602021066.png)# CosmicLens

A web application for exploring NASA's Astronomy Picture of the Day (APOD) dataset - featuring 30+ years of cosmic imagery and scientific explanations.

## Project Structure

```
Web_coursework_/
├── cosmiclens-api/          # FastAPI Backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # Database connection
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routers/        # API endpoints
│   │   └── services/       # Business logic
│   ├── docs/               # Documentation
│   ├── data/               # Dataset files
│   ├── requirements.txt
│   └── manage.py           # CLI management
│
├── cosmiclens-frontend/    # React Frontend
│   └── index.html
│
└── README.md               # This file
```

## Quick Start

### Prerequisites

- **Python 3.9+** installed
- **Internet connection** (for fetching NASA APOD data)

### 1. Install Dependencies

```bash
cd cosmiclens-api
pip install -r requirements.txt
```

### 2. Download Dataset (Optional)

To populate the database with NASA APOD data:

1. Download the dataset from Kaggle:
   https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026
2. Place the CSV file (`nasa_apod.csv`) in the `cosmiclens-api/data/` directory

### 3. Initialize Database

```bash
cd cosmiclens-api
python -m app.scripts.init_db
```

This will:
- Create the SQLite database
- Import data from CSV (if available)
- Show database statistics

Additional database commands:
```bash
python -m app.scripts.init_db status    # Show database status
python -m app.scripts.init_db clear     # Clear all data
python -m app.scripts.init_db reset     # Reset database
```

### 4. Start the API Server

```bash
cd cosmiclens-api
python manage.py server
```

API will be available at:
- **Base URL**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Start the Frontend

**Option A: Using Python's HTTP server**
```bash
cd cosmiclens-frontend
python3 -m http.server 3000
```
Then open http://localhost:3000

**Option B: Open directly in browser**
```bash
# Or simply open the HTML file directly
open cosmiclens-frontend/index.html
```

> **Note**: The frontend expects the API to be running on `http://localhost:8000`. If you use a different port, update the `API_BASE` constant in `index.html` (line 1030).

### Complete Setup Example

Here's a complete step-by-step example to get everything running:

```bash
# 1. Navigate to project directory
cd /path/to/Web_coursework_

# 2. Install Python dependencies
cd cosmiclens-api
pip install -r requirements.txt

# 3. Download NASA APOD dataset from Kaggle
# https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026
# Place the downloaded CSV file as: cosmiclens-api/data/nasa_apod.csv

# 4. Initialize database and import data
python -m app.scripts.init_db

# 5. Start API server (keep this terminal open)
python manage.py server

# 6. In a new terminal, start frontend
cd cosmiclens-frontend
python3 -m http.server 3000

# 7. Open browser: http://localhost:3000
```

### Troubleshooting

- **API connection error**: Make sure the API server is running on port 8000
- **No data displayed**: Run `python -m app.scripts.init_db` to import data
- **Port already in use**: Change the port number in the command (e.g., `python3 -m http.server 8080`)

## Features

### Backend API
- **CRUD Operations**: Full Create, Read, Update, Delete for pictures and collections
- **Advanced Search**: Filter by date range, media type, keywords
- **Analytics**: Statistics on media distribution, temporal trends
- **23 API Endpoints**: RESTful design with standard HTTP methods

### Frontend
- Modern dark theme with cosmic aesthetic
- Interactive picture gallery
- Search and filter functionality
- Collection management
- Responsive design for all devices

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

### Frontend
- **HTML5 / CSS3 / JavaScript**
- No build step required - runs directly in browser

## API Endpoints

### Pictures
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/pictures` | List all pictures |
| GET | `/api/v1/pictures/{id}` | Get picture by ID |
| GET | `/api/v1/pictures/search` | Search pictures |
| GET | `/api/v1/pictures/random` | Get random picture |
| POST | `/api/v1/pictures` | Create picture |
| PUT | `/api/v1/pictures/{id}` | Update picture |
| DELETE | `/api/v1/pictures/{id}` | Delete picture |

### Collections
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/collections` | List collections |
| GET | `/api/v1/collections/{id}` | Get collection |
| POST | `/api/v1/collections` | Create collection |
| PUT | `/api/v1/collections/{id}` | Update collection |
| DELETE | `/api/v1/collections/{id}` | Delete collection |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/analytics/overview` | Dataset statistics |
| GET | `/api/v1/analytics/media-types` | Media distribution |
| GET | `/api/v1/analytics/timeline` | Pictures by date |
| GET | `/api/v1/analytics/keywords` | Top keywords |

## Dataset

- **Source**: [NASA APOD](https://apod.nasa.gov/)
- **Records**: 11,186 images
- **Time Span**: June 1995 - Present
- **License**: NASA Media Usage Guidelines

## Documentation

Detailed documentation available in `cosmiclens-api/docs/`:
- `API_DOCUMENTATION.pdf` - Complete API reference
- `PRESENTATION_SLIDES.pdf` - Project presentation
- `TECHNICAL_REPORT.pdf` - Technical documentation

## License

MIT License
