# CosmicLens API

## API Documentation

**Version**: 1.0.0  
**Base URL**: `http://localhost:8000/api/v1`

---

## Table of Contents

1. [Astronomy Pictures](#astronomy-pictures)
2. [Collections](#collections)
3. [Analytics](#analytics)
4. [Error Codes](#error-codes)

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
