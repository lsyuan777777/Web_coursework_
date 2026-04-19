# CosmicLens API Presentation

## Slide 1: Title Slide

# CosmicLens API
## NASA's Astronomy Picture of the Day RESTful API

**XJCO3011 - Web Services and Web Data**
**Coursework 1: Individual Project**

[Your Name] | [Date]

---

## Slide 2: Project Overview

# What is CosmicLens API?

🌌 A **RESTful web service** for exploring NASA's iconic APOD dataset

### Key Features
- **11,186+ images** spanning 30+ years (1995-2026)
- **Full CRUD operations** for pictures and collections
- **Advanced search** and analytics capabilities
- **Interactive documentation** (Swagger UI & ReDoc)

### Why This Dataset?
- Unique and engaging theme
- Rich metadata and scientific content
- Perfect for demonstrating API capabilities

---

## Slide 3: Technology Stack

# Technology Choices

### Framework: FastAPI
- High performance (comparable to Node.js)
- Automatic API documentation
- Type safety with Pydantic

### Database: PostgreSQL
- Relational integrity for complex data
- ACID compliance
- Advanced querying capabilities

### ORM: SQLAlchemy
- Type-safe database operations
- Database-agnostic design

### Documentation: Swagger UI / ReDoc
- Auto-generated interactive docs
- Industry-standard OpenAPI

---

## Slide 4: Architecture

# System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Client/User   │────▶│   FastAPI Server │────▶│   PostgreSQL    │
│                 │◀────│                  │◀────│                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │
         │                       ▼
         │              ┌──────────────────┐
         └─────────────▶│  Swagger UI      │
                        │  Interactive Docs│
                        └──────────────────┘
```

### Project Structure
```
cosmiclens-api/
├── app/
│   ├── models/      # Database models
│   ├── schemas/    # Validation schemas
│   ├── routers/    # API endpoints
│   └── services/   # Business logic
├── docs/           # Documentation
└── data/           # Dataset files
```

---

## Slide 5: Data Model

# Database Design

### AstronomyPicture Entity
| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key |
| date | DATE | APOD date (unique) |
| title | VARCHAR(500) | Picture title |
| explanation | TEXT | Scientific description |
| media_url | VARCHAR(1000) | Media URL |
| hd_url | VARCHAR(1000) | HD version URL |
| media_type | ENUM | image/video/other |
| copyright | VARCHAR(500) | Copyright holder |
| keywords | TEXT | Comma-separated tags |

### Collection Entity
- User-created themed collections
- Many-to-many relationship with pictures
- Public/private visibility

---

## Slide 6: API Endpoints

# Core Endpoints

### Pictures CRUD (8 endpoints)
```
GET    /api/v1/pictures          # List all
GET    /api/v1/pictures/{id}     # Get by ID
GET    /api/v1/pictures/date/{d} # Get by date
GET    /api/v1/pictures/search   # Search
POST   /api/v1/pictures          # Create
PUT    /api/v1/pictures/{id}     # Update
DELETE /api/v1/pictures/{id}     # Delete
GET    /api/v1/pictures/random   # Random pick
```

### Collections (8 endpoints)
- Full CRUD for personal collections
- Add/remove pictures from collections

### Analytics (7 endpoints)
- Overview statistics
- Media type distribution
- Temporal trends
- Keyword analysis

---

## Slide 7: Demo - Search

# Live Demo: Search Functionality

### Example Request
```bash
curl "http://localhost:8000/api/v1/pictures/search?q=nebula&media_type=image"
```

### Example Response
```json
{
  "total": 1523,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": 4521,
      "date": "2024-03-15",
      "title": "The Orion Nebula in Infrared",
      "media_type": "image",
      "keywords_list": ["nebula", "orion", "infrared", "stars"]
    }
  ]
}
```

### Features
- Full-text search in title, explanation, keywords
- Date range filtering
- Media type filtering
- Pagination support

---

## Slide 8: Analytics

# Analytics & Insights

### Overview Statistics
```json
{
  "total_pictures": 11186,
  "media_distribution": {
    "image": 10754,
    "video": 432
  },
  "pictures_with_hd": 9520,
  "year_range": { "start": 1995, "end": 2026 }
}
```

### Available Analytics
- **Media Types**: Distribution of image/video content
- **Timeline**: Pictures by year/month
- **Keywords**: Most common topics
- **Copyrights**: Top contributors
- **Year Summary**: Detailed yearly statistics

---

## Slide 9: Version Control

# Git Repository Structure

### Commit History
```
🔧 Initial project setup
📄 Added README and documentation
🗄️  Created database models
📡 Implemented Pictures CRUD endpoints
📚 Added Collections endpoints
📊 Implemented Analytics endpoints
🔍 Added search functionality
📝 Updated technical report
🎨 Final polish and testing
```

### Best Practices
- Meaningful commit messages
- Consistent versioning
- Feature-based commits

---

## Slide 10: Testing

# Testing Approach

### Manual Testing via Swagger UI
- ✅ CRUD operations verified
- ✅ Pagination working correctly
- ✅ Search filters functional
- ✅ Error handling validated

### Database Integration
- ✅ PostgreSQL connection confirmed
- ✅ Data import successful
- ✅ Relationships working

### Error Codes
| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | Deleted |
| 404 | Not Found |
| 422 | Validation Error |

---

## Slide 11: Challenges

# Challenges & Solutions

### Challenge 1: Database Setup
**Problem**: Configuring PostgreSQL connection
**Solution**: Environment variables + clear documentation

### Challenge 2: Data Import
**Problem**: 11,000+ records with various formats
**Solution**: Robust CSV parser with batch commits

### Challenge 3: Media Type Detection
**Problem**: Classifying content as image/video
**Solution**: URL extension analysis

### Challenge 4: API Documentation
**Problem**: Manual docs become outdated
**Solution**: Auto-generated Swagger UI

---

## Slide 12: Future Work

# Limitations & Future Enhancements

### Current Limitations
- No user authentication
- No rate limiting
- Limited search (no fuzzy matching)

### Future Enhancements
1. **JWT Authentication** - User accounts & authorization
2. **Rate Limiting** - Prevent API abuse
3. **Redis Caching** - Faster query performance
4. **Elasticsearch** - Advanced full-text search
5. **WebSocket** - Real-time updates
6. **ML Recommendations** - Personalized suggestions

---

## Slide 13: Conclusion

# Summary

### What We Built
✅ Full CRUD RESTful API with **23 endpoints**
✅ PostgreSQL database with **11,186 records**
✅ Interactive documentation with **Swagger UI**
✅ Analytics dashboard with **7 endpoints**
✅ User collections with **many-to-many relationships**

### Key Achievements
- Modern FastAPI framework
- Comprehensive error handling
- Professional documentation
- Clean, modular code architecture

### Learning Outcomes
- RESTful API design principles
- SQL database management
- FastAPI development
- Documentation best practices

---

## Slide 14: Questions

# Q&A Session

## Thank You!

### Links
- **GitHub**: [Repository URL]
- **API Docs**: [Swagger URL]
- **Dataset**: [Kaggle URL]

### Contact
[Your Email]
[University Name]

---

## Slide 15: References

# References

1. FastAPI Documentation. (2024). https://fastapi.tiangolo.com/
2. SQLAlchemy Documentation. (2024). https://docs.sqlalchemy.org/
3. NASA APOD Dataset. Kaggle.
4. NASA APOD Official. https://apod.nasa.gov/
5. REST API Design Rulebook. O'Reilly Media

### Tools Used
- **GenAI (ChatGPT)**: Code generation, debugging, documentation
- **GitHub Copilot**: Code completion assistance
- **FastAPI**: Web framework
- **PostgreSQL**: Database
- **SQLAlchemy**: ORM
- **Swagger UI**: API documentation
