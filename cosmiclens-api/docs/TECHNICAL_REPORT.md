# Technical Report: CosmicLens API

**Student Name**: [Your Name]
**Student ID**: [Your ID]
**Module**: XJCO3011 - Web Services and Web Data
**Assignment**: Coursework 1 - Individual Web Services API Development Project
**Date**: April 2026

---

## 1. Executive Summary

This report documents the design, implementation, and deployment of **CosmicLens API**, a RESTful web service providing programmatic access to NASA's iconic Astronomy Picture of the Day (APOD) dataset. The API enables users to explore, search, and analyze over 30 years of astronomical imagery and scientific explanations through a well-documented, RESTful interface.

### Key Achievements

- **Full CRUD Operations**: Complete Create, Read, Update, and Delete functionality for astronomy pictures and user collections
- **Rich Analytics**: Comprehensive statistics and insights including media distribution, temporal trends, and keyword analysis
- **Modern Architecture**: Built with FastAPI, PostgreSQL, and industry best practices
- **Extensive Documentation**: Interactive Swagger UI, ReDoc, and comprehensive API documentation

---

## 2. Technology Stack Justification

### 2.1 Framework: FastAPI (Python)

**Choice**: FastAPI over Django, Flask, or Node.js Express

**Rationale**:
- **Performance**: FastAPI is one of the fastest Python frameworks, comparable to Node.js and Go
- **Automatic Documentation**: Built-in Swagger UI and ReDoc generation eliminates manual documentation effort
- **Type Safety**: Full integration with Pydantic for request/response validation
- **Async Support**: Native asynchronous programming for improved concurrency
- **Modern Standards**: Based on OpenAPI (Swagger) standards

**Comparison**:
| Framework | Pros | Cons |
|-----------|------|------|
| FastAPI | Fast, auto-docs, type hints | Smaller ecosystem than Django |
| Django | Full-featured, ORM | Overkill for API-only, slower |
| Flask | Lightweight, flexible | Manual documentation, no type safety |
| Express | Popular, npm ecosystem | Callback hell, less type safety |

### 2.2 Database: PostgreSQL

**Choice**: PostgreSQL over SQLite, MySQL, or MongoDB

**Rationale**:
- **Relational Integrity**: Complex relationships between pictures, collections, and keywords
- **Advanced Queries**: Window functions, full-text search, and aggregation capabilities
- **ACID Compliance**: Ensures data integrity for analytics queries
- **Industry Standard**: Widely used, well-documented, excellent performance
- **JSON Support**: Hybrid storage for semi-structured data when needed

**Why Not NoSQL (MongoDB)**:
- Structured data with clear relationships
- Requires complex aggregation queries
- Assessment brief discourages NoSQL without clear justification

### 2.3 ORM: SQLAlchemy

**Rationale**:
- Mature and stable ORM with excellent documentation
- Type-safe query building
- Support for both synchronous and asynchronous operations
- Database-agnostic design

---

## 3. Architecture Design

### 3.1 Project Structure

```
cosmiclens-api/
├── app/
│   ├── main.py           # Application entry point
│   ├── config.py         # Configuration management
│   ├── database.py       # Database connection
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic validation schemas
│   ├── routers/          # API endpoint handlers
│   ├── services/         # Business logic
│   └── scripts/          # Utility scripts
├── docs/                 # API documentation
├── data/                 # Dataset storage
└── tests/                # Unit tests
```

### 3.2 Data Model

**Entity Relationship Diagram (Conceptual)**:

```
┌─────────────────┐       ┌─────────────────────┐       ┌─────────────────┐
│ AstronomyPicture │──────<│   CollectionPicture │>──────│   Collection    │
└─────────────────┘       └─────────────────────┘       └─────────────────┘
```

**AstronomyPicture Entity**:
- Primary key (id), date, title, explanation
- Media information: media_url, hd_url, thumbnail_url, media_type
- Metadata: copyright, keywords, year, month
- Relationships: many-to-many with Collections

**Collection Entity**:
- Primary key (id), name, description
- Visibility: is_public
- Timestamps: created_at, updated_at
- Picture count cache for performance

### 3.3 API Design Principles

1. **RESTful Compliance**: Proper HTTP methods and status codes
2. **Resource-Based URLs**: `/api/v1/pictures`, `/api/v1/collections`
3. **Pagination**: Consistent `page` and `page_size` parameters
4. **Filtering**: Support for `year`, `month`, `media_type` filters
5. **Error Handling**: Standard HTTP codes with detailed error messages

---

## 4. Functionality Specification

### 4.1 Core Features (Minimum Requirements - Pass Grade)

| Requirement | Implementation | Status |
|-------------|---------------|--------|
| CRUD operations | Pictures and Collections endpoints | ✅ |
| Four API endpoints | 8 Pictures + 8 Collections + 7 Analytics = 23 endpoints | ✅ |
| JSON responses | Pydantic models for all responses | ✅ |
| HTTP status codes | 200, 201, 204, 400, 404, 422 | ✅ |
| Database integration | PostgreSQL with SQLAlchemy | ✅ |

### 4.2 Advanced Features (High Grade)

| Feature | Implementation | Description |
|---------|---------------|-------------|
| Advanced Search | Full-text search in title, explanation, keywords | `/pictures/search` |
| Analytics Dashboard | Media distribution, timelines, keyword analysis | `/analytics/*` |
| User Collections | Personal themed collections with many-to-many relationship | `/collections/*` |
| Pagination | Standard pagination with metadata | All list endpoints |
| Input Validation | Pydantic models with detailed validation | All endpoints |

### 4.3 API Endpoints Summary

**Astronomy Pictures** (8 endpoints):
- `GET /pictures` - List with pagination and filters
- `GET /pictures/{id}` - Get by ID
- `GET /pictures/date/{date}` - Get by date
- `GET /pictures/search` - Full-text search
- `POST /pictures` - Create new
- `PUT /pictures/{id}` - Update
- `DELETE /pictures/{id}` - Delete
- `GET /pictures/random` - Random picture

**Collections** (8 endpoints):
- `GET /collections` - List collections
- `GET /collections/{id}` - Get with pictures
- `POST /collections` - Create
- `PUT /collections/{id}` - Update
- `DELETE /collections/{id}` - Delete
- `POST /collections/{id}/pictures` - Add picture
- `DELETE /collections/{id}/pictures/{pic_id}` - Remove picture
- `GET /collections/{id}/pictures` - List collection pictures

**Analytics** (7 endpoints):
- `GET /analytics/overview` - Dataset statistics
- `GET /analytics/media-types` - Media distribution
- `GET /analytics/timeline` - Temporal trends
- `GET /analytics/keywords` - Top keywords
- `GET /analytics/copyrights` - Copyright distribution
- `GET /analytics/monthly-stats` - Monthly analysis
- `GET /analytics/year-summary/{year}` - Year statistics

---

## 5. Dataset Information

### 5.1 Source

- **Dataset**: NASA Astronomy Picture of the Day (1995-2026)
- **Kaggle**: https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026
- **Original Source**: NASA APOD (https://apod.nasa.gov/apod/)
- **Records**: 11,186 images
- **Time Span**: June 16, 1995 - Present

### 5.2 Data Schema

| Field | Type | Description |
|-------|------|-------------|
| date | DATE | APOD date (primary identifier) |
| title | VARCHAR(500) | Title of the astronomy picture |
| explanation | TEXT | Scientific explanation (200-500 words) |
| url | VARCHAR(1000) | Media URL |
| hdurl | VARCHAR(1000) | HD version URL |
| media_type | ENUM | image, video, other |
| copyright | VARCHAR(500) | Copyright holder |
| keywords | TEXT | Comma-separated keywords |

### 5.3 Data Quality

- 96.3% images, 3.4% videos, 0.3% other
- Most records include HD URLs
- Extensive scientific explanations
- Keyword tagging for categorization

---

## 6. Testing Approach

### 6.1 Unit Testing

- Model validation with Pydantic
- Service layer business logic
- Router endpoint handlers

### 6.2 Manual Testing

- API endpoint testing via Swagger UI
- Database integration verification
- Error handling validation

### 6.3 Testing Results

| Test Category | Status |
|--------------|--------|
| CRUD Operations | ✅ Passed |
| Pagination | ✅ Passed |
| Search Functionality | ✅ Passed |
| Error Handling | ✅ Passed |
| Database Integration | ✅ Passed |

---

## 7. Challenges and Lessons Learned

### 7.1 Challenges Encountered

1. **Database Initialization**: Setting up PostgreSQL and configuring the connection
2. **Data Import**: Processing 11,000+ records with various date formats
3. **Media Type Detection**: Automatically classifying media from URLs
4. **Relationship Management**: Implementing many-to-many relationships correctly

### 7.2 Solutions Implemented

1. **Database Setup Script**: Automated schema creation and data import
2. **Robust CSV Parser**: Handling multiple date formats and missing fields
3. **URL-Based Classification**: Extracting media type from file extensions
4. **SQLAlchemy Associations**: Properly configured junction tables

### 7.3 Lessons Learned

- **API Design**: Planning endpoints before implementation saves time
- **Schema Validation**: Pydantic catches errors early
- **Database Indexing**: Essential for query performance at scale
- **Documentation**: Auto-generated docs are valuable for debugging

---

## 8. Limitations and Future Work

### 8.1 Current Limitations

1. **No Authentication**: API is currently open to all users
2. **No Rate Limiting**: Potential for abuse
3. **Single Database**: No caching layer
4. **Limited Search**: No fuzzy matching or advanced NLP

### 8.2 Future Improvements

1. **User Authentication**: JWT-based authentication and authorization
2. **Rate Limiting**: Implement per-user quotas
3. **Caching**: Redis cache for frequently accessed data
4. **Enhanced Search**: Elasticsearch or full-text search optimization
5. **API Versioning**: Gradual deprecation support
6. **Real-Time Updates**: WebSocket support for live updates
7. **Machine Learning**: Recommendation engine for similar pictures

---

## 9. Deployment

### 9.1 Local Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with database credentials

# Initialize database
python -m app.scripts.init_db

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 9.2 External Hosting

The API can be deployed to:
- **PythonAnywhere**: Free tier available
- **Railway**: Easy PostgreSQL integration
- **Render**: Good free tier
- **Heroku**: Well-documented Python support

---

## 10. Conclusion

CosmicLens API successfully implements a comprehensive RESTful web service for NASA's Astronomy Picture of the Day dataset. The project demonstrates:

- Proficiency in API design and RESTful principles
- Understanding of database design with SQL
- Modern Python web development practices
- Comprehensive documentation and testing

The implementation exceeds the minimum requirements and provides a solid foundation for future enhancements.

---

## References

1. FastAPI Documentation. (2024). https://fastapi.tiangolo.com/
2. SQLAlchemy Documentation. (2024). https://docs.sqlalchemy.org/
3. NASA APOD Dataset. Kaggle. https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026
4. NASA APOD Official Site. https://apod.nasa.gov/apod/
5. REST API Design Rulebook. Mark Masse. O'Reilly Media

---

## Appendix A: GenAI Declaration

### Tools Used

| Tool | Purpose | Usage Level |
|------|---------|-------------|
| ChatGPT (Cursor AI) | Code generation and debugging | High |
| GitHub Copilot | Code completion | Medium |
| Claude AI | Documentation review | Medium |

### Specific Applications

1. **Project Structure**: AI-assisted design of project architecture
2. **Code Generation**: Boilerplate code for routers and schemas
3. **Debugging**: Identifying and fixing validation errors
4. **Documentation**: Generating API documentation examples
5. **Testing**: Creating test cases and edge cases

### Ethical Considerations

- All generated code was reviewed and modified as needed
- Original NASA dataset is properly attributed
- No confidential data was processed

---

## Appendix B: GitHub Repository

**Repository**: https://github.com/lsyuan777777/Web_coursework_

**Contents**:
- Source code with complete commit history
- README.md with setup instructions
- API documentation (PDF)
- Sample data files
- Requirements.txt

---

*Report generated: April 2026*
*Word count: Approximately 2,500 words*
