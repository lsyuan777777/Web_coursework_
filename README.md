# CosmicLens

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

### 1. Start the API Server

```bash
cd cosmiclens-api
python manage.py server
```

API will be available at:
- **Base URL**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 2. Start the Frontend (optional)

```bash
cd cosmiclens-frontend
python3 -m http.server 3000
```

Then open http://localhost:3000

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
