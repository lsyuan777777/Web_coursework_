# CosmicLens API

## API Documentation

**Version**: 1.0.0  
**Base URL**: `http://localhost:8000/api/v1`

---

## Table of Contents

1. [Astronomy Pictures](#astronomy-pictures)
2. [Collections](#collections)
3. [Analytics](#analytics)
4. [Authentication](#authentication)
5. [Error Codes](#error-codes)

---

## Astronomy Pictures

### List Pictures

Get a paginated list of astronomy pictures with optional filtering.

**Endpoint**: `GET /api/v1/pictures`

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number |
| page_size | integer | 20 | Items per page (max 100) |
| year | integer | - | Filter by year (1995-2030) |
| month | integer | - | Filter by month (1-12) |
| media_type | string | - | Filter by type: `image`, `video`, `other` |

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/pictures?page=1&page_size=10&year=2024"
```

**Example Response**:
```json
{
  "total": 11186,
  "page": 1,
  "page_size": 10,
  "total_pages": 1119,
  "items": [
    {
      "id": 1,
      "date": "2024-01-01",
      "title": "The Dark Tower in Camelot",
      "explanation": "A mysterious nebula shaped like a castle...",
      "media_url": "https://apod.nasa.gov/apod/image/2401/tower.jpg",
      "hd_url": "https://apod.nasa.gov/apod/image/2401/tower_hd.jpg",
      "media_type": "image",
      "copyright": "NASA",
      "year": 2024,
      "month": 1,
      "keywords_list": ["nebula", "stars", "cosmos"]
    }
  ]
}
```

---

### Search Pictures

Search pictures by title, explanation, or keywords.

**Endpoint**: `GET /api/v1/pictures/search`

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| q | string | Yes | Search query |
| start_date | date | No | Filter from date (YYYY-MM-DD) |
| end_date | date | No | Filter until date (YYYY-MM-DD) |
| media_type | string | No | Filter by media type |

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/pictures/search?q=nebula&media_type=image"
```

---

### Get Picture by ID

Retrieve a specific astronomy picture by its ID.

**Endpoint**: `GET /api/v1/pictures/{id}`

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/pictures/1"
```

---

### Get Picture by Date

Retrieve the astronomy picture for a specific date.

**Endpoint**: `GET /api/v1/pictures/date/{date}`

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/pictures/date/2024-01-01"
```

---

### Create Picture

Add a new astronomy picture to the database.

**Endpoint**: `POST /api/v1/pictures`

**Request Body**:
```json
{
  "date": "2024-01-15",
  "title": "New Discovery",
  "explanation": "Scientists observed a new phenomenon...",
  "media_url": "https://example.com/image.jpg",
  "hd_url": "https://example.com/image_hd.jpg",
  "copyright": "NASA",
  "keywords": "discovery, science, astronomy"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/pictures" \
  -H "Content-Type: application/json" \
  -d '{"date":"2024-01-15","title":"New Discovery","explanation":"Scientists observed..."}'
```

---

### Update Picture

Update an existing astronomy picture.

**Endpoint**: `PUT /api/v1/pictures/{id}`

**Example Request**:
```bash
curl -X PUT "http://localhost:8000/api/v1/pictures/1" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title","keywords":"updated, new"}'
```

---

### Delete Picture

Remove an astronomy picture from the database.

**Endpoint**: `DELETE /api/v1/pictures/{id}`

**Example Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/pictures/1"
```

**Response**: `204 No Content`

---

### Get Random Picture

Get a random astronomy picture for discovery.

**Endpoint**: `GET /api/v1/pictures/random`

---

### Get Years with Pictures

Get a list of years that have pictures, with picture counts for each year.

**Endpoint**: `GET /api/v1/pictures/stats/years`

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/pictures/stats/years"
```

**Example Response**:
```json
[
  {"year": 2026, "count": 111},
  {"year": 2025, "count": 365},
  {"year": 2024, "count": 366}
]
```

---

## Collections

### List Collections

Get all collections with pagination.

**Endpoint**: `GET /api/v1/collections`

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number |
| page_size | integer | 20 | Items per page |
| public_only | boolean | false | Show only public collections |

---

### Get Collection

Get a specific collection with its pictures.

**Endpoint**: `GET /api/v1/collections/{id}`

---

### Create Collection

Create a new collection.

**Endpoint**: `POST /api/v1/collections`

**Request Body**:
```json
{
  "name": "My Favorites",
  "description": "My favorite astronomy pictures",
  "is_public": true
}
```

---

### Update Collection

Update a collection's details.

**Endpoint**: `PUT /api/v1/collections/{id}`

---

### Delete Collection

Delete a collection.

**Endpoint**: `DELETE /api/v1/collections/{id}`

---

### Add Picture to Collection

Add an astronomy picture to a collection.

**Endpoint**: `POST /api/v1/collections/{id}/pictures`

**Request Body**:
```json
{
  "picture_id": 123
}
```

---

### Remove Picture from Collection

Remove a picture from a collection.

**Endpoint**: `DELETE /api/v1/collections/{id}/pictures/{picture_id}`

---

### Get Collection Pictures

Get all pictures in a specific collection.

**Endpoint**: `GET /api/v1/collections/{id}/pictures`

**Headers** (optional):
```
Authorization: Bearer <access_token>
```

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/collections/1/pictures"
```

**Example Response**:
```json
[
  {
    "id": 1,
    "date": "2024-01-01",
    "title": "The Dark Tower in Camelot",
    "media_type": "image",
    "media_url": "https://apod.nasa.gov/apod/image/2401/tower.jpg",
    "added_at": "2026-04-20T10:30:00"
  }
]
```

**Note**: Users can only access pictures from their own collections or public collections.

---

## Analytics

### Overview

Get overall statistics about the dataset.

**Endpoint**: `GET /api/v1/analytics/overview`

**Example Response**:
```json
{
  "total_pictures": 11186,
  "media_distribution": {
    "image": 10807,
    "video": 379
  },
  "pictures_with_hd": 9520,
  "pictures_with_copyright": 8234,
  "date_range": {
    "earliest": "1995-06-16",
    "latest": "2026-04-19"
  }
}
```

---

### Media Types

Get media type distribution statistics.

**Endpoint**: `GET /api/v1/analytics/media-types`

---

### Timeline

Get picture count timeline by year or month.

**Endpoint**: `GET /api/v1/analytics/timeline`

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| granularity | string | year | `year` or `month` |

---

### Top Keywords

Get most common keywords.

**Endpoint**: `GET /api/v1/analytics/keywords`

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 20 | Number of keywords to return |

---

### Copyright Distribution

Get distribution of copyright holders.

**Endpoint**: `GET /api/v1/analytics/copyrights`

---

### Year Summary

Get statistics for a specific year.

**Endpoint**: `GET /api/v1/analytics/year-summary/{year}`

---

### Monthly Statistics

Get picture count distribution by month (1-12) to identify the best months for astronomy.

**Endpoint**: `GET /api/v1/analytics/monthly-stats`

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/monthly-stats"
```

**Example Response**:
```json
{
  "monthly_distribution": [
    {"month": 1, "count": 935},
    {"month": 2, "count": 847},
    {"month": 3, "count": 930}
  ]
}
```

---

## Authentication

The API uses JWT (JSON Web Token) for authentication. After successful login, you will receive an access token that must be included in subsequent requests.

### Register

Create a new user account.

**Endpoint**: `POST /api/v1/auth/register`

**Request Body**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | Yes | 3-50 characters, unique |
| email | string | Yes | Valid email address, unique |
| password | string | Yes | Minimum 6 characters |

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","email":"john@example.com","password":"securepassword123"}'
```

**Example Response** (201 Created):
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-04-21T10:30:00"
}
```

**Error Responses**:
- `400 Bad Request`: Username or email already registered

---

### Login

Authenticate and receive an access token.

**Endpoint**: `POST /api/v1/auth/login`

**Note**: If the user is already logged in (valid Authorization header provided), returns 400 Bad Request.

**Request Body** (form-urlencoded):
```
username=john_doe&password=securepassword123
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | Yes | Your username |
| password | string | Yes | Your password |

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=securepassword123"
```

**Example Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Using the Token**:
Include the token in the `Authorization` header for subsequent requests:
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Error Responses**:
- `400 Bad Request`: Already logged in (user is already authenticated)
- `401 Unauthorized`: Invalid username or password

---

### Get Current User

Get information about the currently authenticated user.

**Endpoint**: `GET /api/v1/auth/me`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Example Response** (200 OK):
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-04-21T10:30:00"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token

---

### Logout

Log out the current user. Note: JWT tokens are stateless, so the server doesn't actually invalidate the token. The client should remove the token from local storage.

**Endpoint**: `POST /api/v1/auth/logout`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Example Response** (200 OK):
```json
{
  "message": "Successfully logged out"
}
```

---

## Base Endpoints

### Root Endpoint

Get API information and available endpoints.

**Endpoint**: `GET /`

**Example Request**:
```bash
curl -X GET "http://localhost:8000/"
```

**Example Response**:
```json
{
  "name": "CosmicLens API",
  "version": "1.0.0",
  "description": "A RESTful API for NASA's Astronomy Picture of the Day",
  "documentation": {
    "swagger_ui": "/docs",
    "redoc": "/redoc",
    "openapi_json": "/openapi.json"
  },
  "endpoints": {
    "pictures": "/api/v1/pictures",
    "collections": "/api/v1/collections",
    "analytics": "/api/v1/analytics",
    "auth": "/api/v1/auth"
  },
  "dataset_source": "https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026"
}
```

---

### Health Check

Check the API health status.

**Endpoint**: `GET /health`

**Example Request**:
```bash
curl -X GET "http://localhost:8000/health"
```

**Example Response**:
```json
{
  "status": "healthy",
  "service": "CosmicLens API",
  "version": "1.0.0"
}
```

---

## Error Codes

The API uses standard HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (successful delete) |
| 400 | Bad Request |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

**Error Response Format**:
```json
{
  "detail": "Error message",
  "errors": [
    {
      "field": "field_name",
      "message": "Error description",
      "type": "value_error"
    }
  ]
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production deployment, consider adding rate limiting middleware.

---

## Dataset Source

This API uses the **NASA Astronomy Picture of the Day** dataset from Kaggle:

- **Dataset**: [NASA APOD (1995-2026)](https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026)
- **Original Source**: [NASA APOD](https://apod.nasa.gov/apod/astropix.html)
- **License**: NASA Media Usage Guidelines

---

## License

MIT License
