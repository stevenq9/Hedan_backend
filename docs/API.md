# API Documentation

## Overview

HEDAN Backend exposes two distinct FastAPI applications serving different client types:

1. **Game API** (`http://localhost:8000`) - Public API for patients completing questionnaires
2. **Web App API** (`http://localhost:8001`) - Authenticated API for psychologists and administrators

Both applications provide OpenAPI documentation at:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

---

## Authentication & Authorization

### JWT Token Flow

#### 1. Obtain Token (Login)
```http
POST /auth/login
Content-Type: application/json

{
  "email": "psychologist@example.com",
  "password": "secure_password",
  "role": "PSYCHOLOGIST"
}

Response:
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Set-Cookie: accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...; HttpOnly; Secure; SameSite=None
```

#### 2. Use Token in Authenticated Requests

**Option A: Authorization Header**
```http
GET /patients/children
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Option B: Cookie** (Automatically converted by `AuthCookieMiddleware`)
```http
GET /patients/children
Cookie: accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### User Roles

- **ADMIN**: Full system access
  - Create/manage users
  - View all psychologists
  - View all test data

- **PSYCHOLOGIST**: Patient management and assessment
  - Manage own patients
  - View own test reports
  - Create test sessions

### Authorization Guards

Route-level authorization is applied via Fastapi Security dependencies:

- `admin_only()` - Requires ADMIN role
- `psychologist_only()` - Requires PSYCHOLOGIST role  
- `psychologist_with_cedula(cedula)` - Requires matching psychologist cedula
- `psychologist_with_cedula_or_admin(cedula)` - PSYCHOLOGIST with matching cedula OR ADMIN

---

## Web App API

Full-featured API for administrative operations. All endpoints require authentication.

### Authentication Endpoints

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password",
  "role": "PSYCHOLOGIST"
}

Response 200:
{
  "accessToken": "jwt_token_here"
}

Response 401:
{
  "detail": "Invalid credentials"
}
```

#### Logout
```http
POST /auth/logout
Authorization: Bearer {token}

Response 200:
Clears accessToken cookie
```

---

### User Management Endpoints

#### Create Psychologist Account
```http
POST /users/psychologists
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "email": "new_psychologist@example.com",
  "password": "secure_password",
  "cedula": "1234567890",
  "name": "Dr. John Doe",
  "specialization": "Child Psychology"
}

Response 201:
{
  "id": "uuid",
  "email": "new_psychologist@example.com",
  "cedula": "1234567890"
}

Response 400:
{
  "detail": "User already exists"
}
```

#### Update Psychologist Profile
```http
PUT /users/psychologists/{cedula}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Updated Name",
  "specialization": "Updated Specialization",
  "phone": "555-1234"
}

Response 200:
{
  "id": "uuid",
  "cedula": "1234567890",
  "name": "Updated Name"
}

Response 403:
{
  "detail": "Not authorized to update this psychologist"
}
```

---

### Patient Management Endpoints

#### List All Psychologists
```http
GET /patients/psychologists
Authorization: Bearer {token}

Response 200:
{
  "psychologists": [
    {
      "id": "uuid",
      "cedula": "1234567890",
      "name": "Dr. John Doe",
      "email": "john@example.com"
    }
  ]
}
```

#### Get Psychologist Details
```http
GET /patients/psychologists/{cedula}
Authorization: Bearer {token}

Response 200:
{
  "id": "uuid",
  "cedula": "1234567890",
  "name": "Dr. John Doe",
  "specialization": "Child Psychology",
  "patients_count": 5
}
```

#### List Children for Psychologist
```http
GET /patients/children?psychologist_cedula=1234567890
Authorization: Bearer {token}

Response 200:
{
  "children": [
    {
      "id": "uuid",
      "name": "Juan",
      "age": 8,
      "sex": "MALE",
      "registered_at": "2024-01-12T10:30:00Z"
    }
  ]
}
```

#### Register Child Patient
```http
POST /patients/children
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Juan Pérez",
  "age": 8,
  "sex": "MALE",
  "psychologist_cedula": "1234567890"
}

Response 201:
{
  "id": "uuid",
  "name": "Juan Pérez",
  "age": 8,
  "sex": "MALE"
}

Events Published:
- ChildAddedEvent (triggers result analysis module)
```

---

### Questionnaire Management Endpoints

#### List Questionnaires
```http
GET /questionnaires
Authorization: Bearer {token}

Response 200:
{
  "questionnaires": [
    {
      "id": "uuid",
      "name": "Attention Assessment",
      "description": "...",
      "questions_count": 25,
      "created_at": "2024-01-12T10:30:00Z"
    }
  ]
}
```

#### Create Questionnaire
```http
POST /questionnaires
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "New Assessment",
  "description": "Assessment description",
  "questions": [
    {
      "id": "q1",
      "text": "Question 1",
      "type": "MULTIPLE_CHOICE",
      "options": ["A", "B", "C", "D"]
    }
  ]
}

Response 201:
{
  "id": "uuid",
  "name": "New Assessment"
}
```

#### Create Test Session
```http
POST /questionnaires/{questionnaire_id}/test-sessions
Authorization: Bearer {token}
Content-Type: application/json

{
  "child_id": "uuid",
  "scheduled_for": "2024-01-15T14:00:00Z"
}

Response 201:
{
  "id": "test_session_uuid",
  "status": "PENDING",
  "invitation_token": "unique_token_for_child",
  "invitation_link": "https://game.example.com/questionnaires?token=unique_token_for_child"
}
```

#### Get Test Session
```http
GET /questionnaires/test-sessions/{session_id}
Authorization: Bearer {token}

Response 200:
{
  "id": "session_uuid",
  "child_id": "child_uuid",
  "status": "IN_PROGRESS",
  "created_at": "2024-01-12T10:00:00Z",
  "answers_submitted_at": null,
  "time_taken": null
}
```

---

### Results Analysis Endpoints

#### Get Test Reports for Psychologist
```http
GET /results/{cedula}/test_reports
Authorization: Bearer {token}
Security: psychologist_with_cedula(cedula) OR admin_only

Response 200:
{
  "reports": [
    {
      "id": "report_uuid",
      "test_session_id": "session_uuid",
      "child_name": "Juan",
      "completed_at": "2024-01-15T15:30:00Z",
      "time_taken_seconds": 1800,
      "scores": {
        "attention": 85,
        "memory": 92,
        "processing_speed": 78
      }
    }
  ]
}
```

#### Get Report Details
```http
GET /results/test_reports/{report_id}
Authorization: Bearer {token}

Response 200:
{
  "id": "report_uuid",
  "test_session_id": "session_uuid",
  "child_id": "child_uuid",
  "psychologist_id": "psychologist_uuid",
  "completed_at": "2024-01-15T15:30:00Z",
  "analysis": {
    "raw_scores": [...],
    "processed_scores": [...],
    "interpretation": "...",
    "recommendations": "..."
  }
}
```

---

## Game API

Public API for patients to complete questionnaires. Minimal authentication required.

### Questionnaire Endpoints

#### Validate Questionnaire Token
```http
POST /questionnaires/validate-token
Content-Type: application/json

{
  "token": "unique_token_from_invitation"
}

Response 200:
{
  "valid": true,
  "test_session_id": "session_uuid",
  "questionnaire_id": "questionnaire_uuid"
}

Response 401:
{
  "detail": "Invalid or expired token"
}
```

#### Submit Questionnaire Answers
```http
POST /questionnaires/{token}/answers
Content-Type: application/json

{
  "answers": [
    {
      "question_id": "q1",
      "value": "A"
    },
    {
      "question_id": "q2",
      "value": "B"
    }
  ],
  "time_taken_seconds": 1800
}

Response 201:
{
  "test_session_id": "session_uuid",
  "status": "COMPLETED",
  "completed_at": "2024-01-15T15:30:00Z"
}

Response 400:
{
  "detail": "Invalid answers for questionnaire"
}

Response 409:
{
  "detail": "Answers already submitted for this session"
}

Events Published:
- QuestionnaireCompletedEvent
- Triggers ResultsAnalysis module to generate reports
```

#### Get Test Session Status
```http
GET /questionnaires/test-sessions/{session_id}
Query Parameters:
  - token: required (invitation token)

Response 200:
{
  "id": "session_uuid",
  "status": "COMPLETED",
  "created_at": "2024-01-15T14:00:00Z",
  "answers_submitted_at": "2024-01-15T15:30:00Z",
  "time_taken": 1800
}

Response 404:
{
  "detail": "Session not found"
}
```

---

## Common Response Formats

### Success Response (2xx)
```json
{
  "data": {...},
  "meta": {
    "timestamp": "2024-01-12T10:30:00Z",
    "version": "1.0"
  }
}
```

### Error Response (4xx, 5xx)
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "status_code": 400
}
```

### List Response
```json
{
  "items": [...],
  "total": 100,
  "skip": 0,
  "limit": 10
}
```

---

## CORS Policy

### Game API
```
Allowed Origins: GAME_URL (environment variable)
Allowed Methods: GET, POST, PUT, DELETE, OPTIONS
Allowed Headers: *
Allow Credentials: True
```

### Web App API
```
Allowed Origins: WEB_APP_URL (environment variable)
Allowed Methods: GET, POST, PUT, DELETE, OPTIONS
Allowed Headers: *
Allow Credentials: True
```

---

## Rate Limiting

Currently not implemented. Consider adding for production:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/items/")
@limiter.limit("5/minute")
async def read_items():
    return [{"item_id": "Foo"}]
```

---

## Request/Response Examples

### Complete Login Flow

**Request:**
```bash
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "psych@example.com",
    "password": "password123",
    "role": "PSYCHOLOGIST"
  }'
```

**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

**Subsequent requests with token:**
```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  http://localhost:8001/patients/children
```

### Create Test Session and Get Invitation Link

**Request:**
```bash
curl -X POST http://localhost:8001/questionnaires/123/test-sessions \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "child_id": "child-uuid-456",
    "scheduled_for": "2024-01-20T14:00:00Z"
  }'
```

**Response:**
```json
{
  "id": "session-789",
  "status": "PENDING",
  "invitation_token": "invite_token_abc123xyz",
  "invitation_link": "https://game.example.com/questionnaires?token=invite_token_abc123xyz"
}
```

**Child completes questionnaire:**
```bash
curl -X POST http://localhost:8000/questionnaires/invite_token_abc123xyz/answers \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {"question_id": "q1", "value": "Option A"},
      {"question_id": "q2", "value": "Option C"}
    ],
    "time_taken_seconds": 1800
  }'
```

---

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| INVALID_CREDENTIALS | 401 | Email/password mismatch |
| UNAUTHORIZED | 401 | Missing/invalid token |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| VALIDATION_ERROR | 400 | Invalid input data |
| CONFLICT | 409 | Resource state conflict (e.g., duplicate submission) |
| INTERNAL_ERROR | 500 | Unexpected server error |

---

## Version History

### v1.0.0 (Current)
- Initial API release
- Authentication and authorization
- User management
- Patient management
- Questionnaire workflows
- Results analysis

---

## API Monitoring

### Health Check (Planned)
```http
GET /health
Response 200:
{
  "status": "healthy",
  "timestamp": "2024-01-12T10:30:00Z"
}
```

### Metrics Endpoint (Planned)
```http
GET /metrics
```

Integrate with Prometheus for monitoring.

---

## Breaking Changes Policy

Will be documented in release notes. Minor version bumps for new features, major version for breaking changes.

