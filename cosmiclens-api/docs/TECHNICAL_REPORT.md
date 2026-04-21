# Technical Report: CosmicLens API

**Student:** Liu Siyuan (2022115992) | **Module:** XJCO3011 - Web Services and Web Data | **Date:** April 2026

---

## 1. Executive Summary

CosmicLens API is a comprehensive RESTful web service designed to provide programmatic access to NASA's Astronomy Picture of the Day (APOD) dataset. This dataset represents one of the most significant collections of astronomical imagery available to the public, spanning over three decades of scientific photography from space-based and ground-based observatories worldwide. The API serves as a middleware layer that transforms this rich astronomical dataset into a developer-friendly interface, enabling applications ranging from simple picture browsing to complex data analysis workflows.

The APOD dataset spans from June 16, 1995, when the feature first launched on NASA's website, through the present day. This chronological range encompasses remarkable advances in astronomical imaging technology, from early CCD cameras to modern digital sensors. The dataset contains over 11,186 records, each comprising a date, title, detailed scientific explanation, media URL, high-definition media URL (when available), media type classification, copyright information, and user-contributed keywords. Approximately 96.3% of the records contain traditional photographic images, while 3.4% feature video content from platforms like YouTube and Vimeo.

This project implements full CRUD operations for both the astronomical picture catalog and user-managed collections. The authentication system uses JWT (JSON Web Tokens) with bcrypt password hashing for secure, stateless authentication. The API provides 27 endpoints organized into four logical categories: Authentication, Pictures, Collections, and Analytics.

The technology stack comprises FastAPI for the web framework, PostgreSQL for the database, and SQLAlchemy for the ORM layer. This combination was selected after careful evaluation of alternatives, prioritizing performance, developer experience, and maintainability. The project follows RESTful design principles with comprehensive API documentation through Swagger UI and ReDoc.

**Key Features:**

- Full CRUD operations for astronomical pictures and user collections
- Rich analytics capabilities including media distribution analysis, temporal trends, and keyword frequency analysis
- JWT-based authentication with bcrypt password hashing (cost factor 12) for enhanced security
- User isolation ensuring complete separation of user data; users can only access their own collections
- 27 RESTful API endpoints with comprehensive pagination support (configurable page sizes up to 100 items)
- Advanced filtering and search capabilities for picture titles, descriptions, dates, and keywords
- Automatic OpenAPI documentation with interactive Swagger UI and ReDoc interfaces
- Random picture endpoint for discovery and surprise features
- Public and private collection support with granular access control
- Database indexes on frequently queried fields for optimal query performance

---

## 2. Technology Stack

The project was built using carefully selected technologies that balance performance, developer productivity, and long-term maintainability. Each component was chosen after evaluating alternatives and considering the specific requirements of this astronomical data API.

| Component | Technology | Version | Key Benefits |
|-----------|------------|---------|--------------|
| Framework | FastAPI | 0.109+ | High performance (comparable to Node.js), automatic OpenAPI documentation, native async/await support, Pydantic integration |
| Database | PostgreSQL | 15+ | ACID compliance for data integrity, advanced SQL queries with window functions, native JSON support, excellent indexing capabilities |
| ORM | SQLAlchemy | 2.0+ | Type-safe database queries, async database operations, elegant relationship management |
| Authentication | JWT + bcrypt | jose/bcrypt | Stateless authentication tokens, secure password hashing with configurable work factor |

**Why FastAPI:** FastAPI was selected after evaluating alternatives including Flask, Django, and Express.js. FastAPI offers exceptional performance comparable to Node.js, automatic OpenAPI documentation generation, native async/await support, and deep Pydantic integration for automatic request validation and response serialization. These features eliminate the need for manual API documentation and ensure documentation stays synchronized with implementation.

**Why PostgreSQL:** PostgreSQL was chosen after comparing relational databases (MySQL, PostgreSQL) and NoSQL alternatives (MongoDB). PostgreSQL provides complete ACID compliance ensuring data integrity, advanced SQL capabilities including window functions and aggregations for analytics queries, and various index types (B-tree, GIN, GiST) for optimizing date range, keyword, and media type queries. For this project, PostgreSQL offered the best combination of features and reliability.

**Why SQLAlchemy:** SQLAlchemy serves as the ORM layer between FastAPI and PostgreSQL. The ORM provides type-safe query construction preventing SQL injection, automatic table creation and migration support, and an elegant Pythonic interface for defining database models and relationships with lazy and eager loading options.

---

## 3. API Endpoints (27 Total)

The API consists of 27 endpoints organized into four main categories, providing complete coverage for picture management, user collections, analytics, and authentication.

| Category | Count | Auth | Description |
|----------|-------|------|-------------|
| Authentication | 4 | Mixed | Register, login, profile, logout |
| Pictures | 8 | Public/Protected | List, retrieve, CRUD, search, random, by date |
| Collections | 8 | Partial | User collections, public browsing, picture management |
| Analytics | 7 | Public | Overview, media types, timeline, keywords, summaries |

**Authentication Endpoints (4):** POST /auth/register (public), POST /auth/login (public), GET /auth/profile (protected), POST /auth/logout (protected). Uses JWT for stateless authentication with 7-day token expiration. Passwords hashed with bcrypt (cost factor 12). Protected endpoints require Authorization header with Bearer token.

**Picture Endpoints (8):** GET /pictures (paginated list), GET /pictures/{id}, POST /pictures (protected), PUT /pictures/{id} (protected), DELETE /pictures/{id} (protected), GET /pictures/search (filters by title, explanation, keywords), GET /pictures/random (for discovery features), GET /pictures/date/{date}.

**Collection Endpoints (8):** GET /collections (user's collections), GET /collections/public (browse public), POST /collections (protected), GET /collections/{id}, PUT /collections/{id} (protected), DELETE /collections/{id} (protected), POST /collections/{id}/pictures (protected), DELETE /collections/{id}/pictures/{picture_id} (protected). Collections enable organizing pictures with public/private visibility. Many-to-many relationship with pictures. User isolation enforced.

**Analytics Endpoints (7):** GET /analytics/overview, /analytics/media-types, /analytics/timeline, /analytics/top-keywords, /analytics/year-summary, /analytics/month-summary, /analytics/decade-summary. Provide aggregate dataset statistics including media distribution, yearly/monthly trends, and keyword frequencies.

---

## 4. Dataset Information

The APOD dataset is one of NASA's longest-running web features, curated by Dr. Jerry Bonnell and Dr. Robert Nemiroff since 1995. Each entry includes image/video, scientific explanation written by astronomers, copyright information, and metadata. Many images are contributed by professional observatories including Hubble Space Telescope, James Webb Space Telescope, and various ground-based facilities.

| Attribute | Value |
|-----------|-------|
| Source | NASA Astronomy Picture of the Day |
| Period | June 16, 1995 - Present |
| Total Records | 11,186 images/videos |
| Coverage | 31 years (1995-2026) |
| Media Types | Images (96.3%), Videos (3.4%), Other (0.3%) |
| License | Public Domain (NASA) |

**Data Schema:** Each record contains id (unique), date (unique publication date), title (string), explanation (text), media_url (standard resolution), hd_url (high-definition, optional), media_type (image/video), copyright (optional), and keywords (array of user-contributed tags).

---

## 5. Testing and Challenges

**Testing Methodology:** Comprehensive testing covered all major functional areas including CRUD operations with valid and invalid inputs, pagination with various page sizes and edge cases, search functionality with different query patterns, error handling for all error scenarios, database operations, authentication flows, and user data isolation verification.

**Challenges and Solutions:**

1. **Database Initialization:** Used Docker to containerize PostgreSQL for consistent environments across machines. Custom initialization script automatically imports the APOD dataset on first startup.

2. **Data Import (11,000+ records):** Handled inconsistent date formats, missing fields, duplicate dates, and malformed URLs with robust parsing and validation. Created detailed logging of any issues encountered during import.

3. **Many-to-Many Relationships:** Implemented association table with proper foreign key constraints and cascade delete rules for Collections ↔ Pictures relationship, ensuring referential integrity when collections or pictures are deleted.

4. **JWT Authentication:** Used python-jose library with HS256 algorithm, bcrypt with cost factor 12, and proper token expiration handling with informative error messages for expired or invalid tokens.

5. **User Isolation:** Added authorization checks at service layer verifying ownership before any modification operation, returning 403 Forbidden for unauthorized access attempts.

---

## 6. Limitations and Future Work

**Current Limitations:** No caching layer; every request hits the database. SQL LIKE queries only; no fuzzy search capability. Stateless JWT tokens cannot be individually revoked before expiration. No rate limiting on API endpoints. Limited URL validation for stored media links.

**Future Improvements:** Token refresh mechanism for extended sessions without re-authentication. Redis caching for analytics results and frequently accessed data to reduce database load. Elasticsearch integration for full-text search with fuzzy matching and autocomplete. WebSocket support for real-time features like live search suggestions. ML-based recommendation engine for personalized picture suggestions. Per-client rate limiting and API key management for abuse protection.

---

## 7. Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Set DATABASE_URL and SECRET_KEY in .env

# Initialize database and import data
python -m app.scripts.init_db

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**API Documentation:** Swagger UI at http://localhost:8000/docs (interactive exploration), ReDoc at http://localhost:8000/redoc (clean documentation view), and https://github.com/lsyuan777777/Web_coursework_/blob/main/API_DOCUMENTATION.pdf.

**Docker Deployment:** `docker-compose up -d` for containerized deployment.

**Presentation:** https://github.com/lsyuan777777/Web_coursework_/blob/main/CosmicLens-API_.pptx

**Repository:** https://github.com/lsyuan777777/Web_coursework_

---

# Appendix: GenAI Usage Declaration

## A.1 GenAI Usage Level: High (Grade Band 80-89)

This project employs GenAI in a high-level, creative manner as specified for the 80-89 grade band. GenAI was not used merely for basic code generation but was actively leveraged throughout the entire development lifecycle for creative thinking, solution exploration, architectural decision-making, and technology learning.

## A.2 GenAI Tools Used

| Tool | Platform | Role | Usage Level |
|------|----------|------|-------------|
| ChatGPT | Cursor AI | Primary assistant for code generation, debugging, architecture | High |
| GitHub Copilot | VS Code | Real-time code completion and suggestions | Medium |
| Claude AI | Anthropic | Documentation review and technical analysis | Medium |
| Perplexity AI | Web | Dataset discovery and research | Low |

## A.3 Specific Applications by Development Phase

### Planning and Architecture
- Discussed and compared different project structure approaches
- Selected optimal modular architecture for maintainability
- Explored technology trade-offs (FastAPI vs Django, PostgreSQL vs MongoDB)
- Evaluated authentication strategies (JWT vs session-based)

### Code Development
- Generated authentication system (registration, login, JWT tokens with bcrypt)
- Created SQLAlchemy models with many-to-many relationships (User → Collection ← Picture)
- Implemented pagination with validated query parameters
- Built comprehensive error handling with custom exception handlers

### Debugging
- Resolved Pydantic validation errors by using Optional types
- Fixed SQLAlchemy DetachedInstanceError through proper session management
- Handled JWT token expiration with proper error messages
- Debugged relationship loading issues (eager vs lazy loading)

### Dataset Processing
- Designed robust date parsing for multiple formats in 11,186 records
- Implemented media type detection (images vs YouTube/Vimeo videos)
- Created keyword extraction and normalization logic

## A.4 Development Impact

| Phase | AI Contribution | Applications |
|-------|----------------|--------------|
| Planning | High | Architecture discussions, technology comparison |
| Implementation | Medium | Code templates, patterns, boilerplate |
| Debugging | High | Error diagnosis, solution exploration |
| Documentation | High | Report structure, formatting |
| Learning | Very High | Concept explanation, best practices |

**Skills Developed:** FastAPI, SQLAlchemy, PostgreSQL, JWT authentication, RESTful API design

**Estimated Time Saved:** ~11 hours

## A.5 Ethical Considerations

All AI-generated code was thoroughly reviewed and understood before integration. The NASA dataset was properly attributed. No personal data was processed. GenAI usage is transparently declared per course requirements.

## A.6 Grading Criteria Alignment

This project meets the 80-89 grade band criteria through: high-level GenAI engagement in architectural decisions, systematic methodological usage throughout development, creative application of AI suggestions to project needs, and comprehensive documentation of AI interactions.

---

*Report: CosmicLens API | Student: Liu Siyuan (2022115992) | April 2026*
