# HEDAN Backend - Technical Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Technology Stack](#technology-stack)
5. [Key Design Patterns](#key-design-patterns)
6. [Module Description](#module-description)
7. [API Structure](#api-structure)
8. [Database Design](#database-design)
9. [Getting Started](#getting-started)
10. [Development Guide](#development-guide)

---

## Overview

HEDAN Backend is a sophisticated Python-based backend system designed to manage psychological assessments, patient data, and questionnaire processing. The system is built on a **modular architecture** with clean separation of concerns, implementing Domain-Driven Design (DDD) principles and the CQRS (Command Query Responsibility Segregation) pattern.

The backend exposes two distinct FastAPI applications:
- **Game API**: Handles game-based questionnaire interactions for patients
- **Web App API**: Manages administrative operations for psychologists and users

---

## Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                       │
│              (Game Frontend / Web Dashboard)                 │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
   ┌────▼──────┐      ┌──────▼────┐
   │  Game API │      │ Web App API│
   │ (FastAPI) │      │ (FastAPI)  │
   └────┬──────┘      └──────┬────┘
        │                     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   Core Application  │
        │   Layer (Mediator)  │
        └──────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼────┐  ┌──────▼─────┐  ┌────▼──────┐
│ Modules │  │ Event Bus  │  │ Dependency│
│         │  │ (In-Memory)│  │ Injection │
└───┬────┘  └────────────┘  └───────────┘
    │
    ├─ Patients Module
    ├─ Questionnaires Module
    ├─ Results Analysis Module
    └─ Users Management Module
            │
            ▼
    ┌──────────────────┐
    │  SQLAlchemy ORM  │
    │  + PostgreSQL    │
    └──────────────────┘
```

### Architectural Layers

#### 1. **Presentation Layer (API)**
- REST endpoints exposed through FastAPI routers
- Request/Response DTOs for data validation
- JWT-based authentication and authorization
- CORS and middleware management

#### 2. **Application Layer**
- **CQRS Pattern Implementation**:
  - **Commands**: Write operations that modify state
  - **Queries**: Read operations that fetch data
- **Mediator Pattern**: Routes commands and queries to appropriate handlers
- **Integration Event Handlers**: Processes events from the event bus

#### 3. **Domain Layer**
- Business logic and validation
- Domain Models:
  - **Aggregate Roots**: Cluster of entities with a single entry point
  - **Entities**: Objects with identity and lifecycle
  - **Value Objects**: Immutable objects representing values
  - **Domain Services**: Business rules that don't fit in entities
- Domain Events: Represent state changes

#### 4. **Infrastructure Layer**
- **Persistence**: SQLAlchemy ORM with PostgreSQL
- **Event Bus**: In-memory pub/sub for domain events
- **Token Management**: JWT authentication and authorization
- **Logging**: Structured logging to Better Stack
- **Hashing**: Password encryption using bcrypt

---

## Project Structure

```
hedan-backend/
├── src/
│   ├── apps/                          # FastAPI application instances
│   │   ├── game_api/                  # Game API application
│   │   │   ├── main.py                # Entry point
│   │   │   ├── setup.py               # FastAPI app configuration
│   │   │   └── modules.py             # Loaded modules for Game API
│   │   └── web_page_api/              # Web Page API application
│   │       ├── main.py                # Entry point
│   │       ├── setup.py               # FastAPI app configuration
│   │       └── modules.py             # Loaded modules for Web API
│   │
│   ├── common/                        # Shared infrastructure & patterns
│   │   ├── api/
│   │   │   ├── authorization.py       # JWT & role-based access control
│   │   │   ├── auth_cookie_handler.py # Cookie to header middleware
│   │   │   ├── di.py                  # Dependency injection setup
│   │   │   ├── handler_factory.py     # Command/Query handler factory
│   │   │   ├── module_installer.py    # Dynamic module installation
│   │   │   └── router_installer.py    # Router installation pattern
│   │   │
│   │   ├── application/               # Core application patterns
│   │   │   ├── command.py             # Command base class
│   │   │   ├── command_handler.py     # Command handler pattern
│   │   │   ├── query.py               # Query base class
│   │   │   ├── query_handler.py       # Query handler pattern
│   │   │   ├── query_service.py       # Query execution pattern
│   │   │   ├── event_bus.py           # Event bus abstraction
│   │   │   ├── event.py               # Event base class
│   │   │   ├── integration_event.py   # Integration event pattern
│   │   │   ├── integration_event_handler.py  # Handler pattern
│   │   │   ├── user_role.py           # User role enumeration
│   │   │   └── write_service.py       # Write operation pattern
│   │   │
│   │   ├── domain/                    # Domain-Driven Design patterns
│   │   │   ├── aggregate_root.py      # Aggregate root abstraction
│   │   │   ├── entity.py              # Entity pattern
│   │   │   ├── value_object.py        # Value object pattern
│   │   │   ├── domain_service.py      # Domain service pattern
│   │   │   ├── validators/            # Common validators
│   │   │   └── value_objects/         # Reusable value objects
│   │   │       ├── cedula.py          # Colombian ID document
│   │   │       ├── email.py           # Email value object
│   │   │       └── sex.py             # Gender/Sex value object
│   │   │
│   │   ├── infrastructure/
│   │   │   ├── persistence/
│   │   │   │   ├── memory/            # In-memory implementations
│   │   │   │   └── sqlalchemy/        # SQLAlchemy implementations
│   │   │   │       ├── models/        # ORM models
│   │   │   │       ├── repositories/  # Repository pattern
│   │   │   │       └── query_services/# Query service implementations
│   │   │   │
│   │   │   ├── bus/
│   │   │   │   └── memory/            # In-memory event bus
│   │   │   │
│   │   │   ├── logging/               # Logging infrastructure
│   │   │   │   └── logging_middleware.py  # Request/response logging
│   │   │   │
│   │   │   └── token/                 # Token management
│   │   │       └── access_security.py # JWT configuration
│   │   │
│   │   ├── event_bus_setup.py         # Event bus handler registration
│   │   ├── mediator_setup.py          # Mediator handler registration
│   │   └── module.py                  # Module base class
│   │
│   └── modules/                       # Feature modules (modular architecture)
│       ├── patients/
│       │   ├── patients_module.py     # Module configuration
│       │   ├── api/                   # HTTP endpoints
│       │   │   ├── routers.py         # Router aggregation
│       │   │   └── psychologist/      # Psychologist endpoints
│       │   ├── application/           # Use cases & handlers
│       │   │   ├── interactors/       # Business logic
│       │   │   └── integration_events_handlers/
│       │   ├── domain/                # Domain models
│       │   │   ├── child/             # Child aggregate
│       │   │   └── psychologist/      # Psychologist aggregate
│       │   └── infrastructure/        # Persistence layer
│       │       └── persistence/
│       │
│       ├── questionnaires/
│       │   ├── questionnaires_module.py   # Web app module
│       │   ├── game_questionnaires_module.py  # Game API module
│       │   ├── api/
│       │   │   ├── questionnaires/    # Admin questionnaire endpoints
│       │   │   └── questionnaires_children/  # Game endpoints
│       │   ├── application/
│       │   │   ├── interactors/
│       │   │   │   ├── set_test_answers/
│       │   │   │   ├── validate_questionnaire_token/
│       │   │   │   └── get_test_session_*/
│       │   │   └── invitation_link/   # Token generation logic
│       │   ├── domain/
│       │   │   └── test_session/      # Test session aggregate
│       │   └── infrastructure/
│       │       └── persistence/
│       │           └── sqlalchemy/
│       │
│       ├── results_analysis/
│       │   ├── results_analysis_module.py  # Web app module
│       │   ├── game_results_analysis_module.py  # Game API module
│       │   ├── api/
│       │   │   └── test_reports/      # Report endpoints
│       │   ├── application/
│       │   │   └── interactors/
│       │   ├── domain/
│       │   │   └── test_report/       # Report aggregate
│       │   └── infrastructure/
│       │
│       └── users_management/
│           ├── users_management_module.py # Module configuration
│           ├── api/
│           │   ├── auth/              # Authentication endpoints
│           │   └── users/             # User management endpoints
│           ├── application/
│           │   ├── interactors/
│           │   │   ├── login/         # Login logic
│           │   │   ├── add_psychologist_user/
│           │   │   └── update_psychologist_user/
│           │   ├── hashing/           # Password hashing
│           │   └── token/             # Token generation
│           ├── domain/
│           │   └── user/              # User aggregate
│           └── infrastructure/
│               ├── hashing/           # bcrypt implementation
│               ├── token/             # JWT implementation
│               └── persistence/
│
├── alembic/                           # Database migrations
│   ├── env.py                         # Alembic environment
│   ├── script.py.mako                 # Migration template
│   └── versions/                      # Migration files
│       ├── cdf38d148e35_initial_database_tables.py
│       ├── 84f17ee79218_upgrade_test_session_columns.py
│       └── 428c5429419c_add_time_taken_field_to_reports_table.py
│
├── docs/                              # Documentation
├── requirements.txt                   # Production dependencies
├── requirements-dev.txt               # Development dependencies
└── README.md                          # This file
```

---

## Technology Stack

### Core Frameworks
- **FastAPI** (v0.110.3): Modern async Python web framework
- **SQLAlchemy** (v2.0.29): SQL toolkit and ORM
- **asyncpg** (v0.29.0): Async PostgreSQL driver

### Application Patterns
- **MediaTR** (v1.3.2): Mediator pattern implementation for CQRS
- **Injector** (v0.21.0): Dependency injection framework
- **fastapi-injector** (v0.5.4): FastAPI DI integration

### Authentication & Security
- **PyJWT** (v2.3.0): JWT token handling
- **fastapi-jwt** (v0.3.0): FastAPI JWT integration
- **Authlib** (v1.3.0): OAuth and security toolkit
- **bcrypt** (v4.1.3): Password hashing

### Database & Migrations
- **Alembic** (v1.13.1): Database migration tool
- **PostgreSQL**: Primary database

### Utilities
- **Pydantic** (v2.7.1): Data validation using Python type hints
- **uvicorn** (v0.29.0): ASGI server
- **loguru** (v0.6.0): Logging library
- **logtail-python** (v0.3.0): Better Stack logging integration
- **Starlette**: Underlying web framework components

---

## Key Design Patterns

### 1. **CQRS (Command Query Responsibility Segregation)**

Commands and Queries separate write and read operations:

```
User Request
    ↓
    ├─ Write Operation? → Command → CommandHandler → Repository → Database
    │
    └─ Read Operation?  → Query   → QueryHandler  → QueryService → Database
```

**Benefits**:
- Clear separation of concerns
- Optimized read and write paths
- Better scalability

### 2. **Mediator Pattern**

Central dispatcher routes commands and queries to handlers:

```
Endpoint → Mediator → Handler Registry → Specific Handler
```

**Implementation**: Uses MediaTR library for clean handler registration.

### 3. **Domain-Driven Design (DDD)**

Organizes code around business domains:

- **Aggregate Roots**: Root entities that manage a cluster
- **Entities**: Objects with identity and lifecycle
- **Value Objects**: Immutable objects without identity
- **Domain Services**: Business logic outside entities
- **Domain Events**: Represent significant business events

### 4. **Repository Pattern**

Abstracts data access:

```
Domain Logic → Repository Interface → Repository Implementation → ORM → Database
```

Allows switching persistence implementations without affecting business logic.

### 5. **Event-Driven Architecture**

In-memory event bus for cross-module communication:

```
Event Publisher → Event Bus → Event Handlers (in same process)
```

**Use Cases**:
- Decoupling modules
- Triggering side effects
- Eventual consistency

### 6. **Dependency Injection**

All dependencies injected via Injector framework:

```
Module.install(injector)
    ├─ Bind Interface → Implementation
    └─ Bind Scope (singleton, request_scope)
```

### 7. **Modular Architecture**

Self-contained feature modules with:
- Own API routes
- Own business logic
- Own persistence layer
- Own domain models

**Module Structure**:
```
module/
  ├── {module}_module.py      (Configuration)
  ├── api/                    (HTTP Layer)
  ├── application/            (Use Cases)
  ├── domain/                 (Business Logic)
  └── infrastructure/         (Persistence)
```

---

## Module Description

### 1. **Patients Module** (`src/modules/patients/`)

Manages patient (child) and psychologist information.

**Key Aggregates**:
- **Child**: Patient being assessed
- **Psychologist**: Healthcare provider

**Key Operations**:
- Register children for psychologists
- Fetch children list
- Fetch psychologist details
- Manage psychologist-child relationships

**Integration Events**:
- `ChildAddedEvent`: Published when a new child is registered

---

### 2. **Questionnaires Module** (`src/modules/questionnaires/`)

Manages psychological assessment questionnaires and test sessions.

**Key Aggregates**:
- **TestSession**: Assessment session for a child
- **Questionnaire**: Set of assessment questions
- **Answer**: Response to a question

**Key Operations**:
- Create test sessions with questionnaires
- Validate questionnaire access tokens
- Record answers to questionnaires
- Retrieve test session details
- Manage invitation links for test access

**Implementations**:
- `questionnaires_module.py`: Web API for questionnaire management
- `game_questionnaires_module.py`: Game API for patient questionnaire responses

**Integration Events**:
- `QuestionnaireReleasedEvent`: When a questionnaire is released
- Events consumed from other modules

---

### 3. **Results Analysis Module** (`src/modules/results_analysis/`)

Analyzes and reports on assessment results.

**Key Aggregates**:
- **TestReport**: Analysis results of a completed test session

**Key Operations**:
- Generate reports from test responses
- Fetch reports for a psychologist
- Calculate assessment metrics

**Implementations**:
- `results_analysis_module.py`: Web API for report viewing
- `game_results_analysis_module.py`: Game API integration

---

### 4. **Users Management Module** (`src/modules/users_management/`)

Handles user authentication and authorization.

**Key Aggregates**:
- **User**: System user (psychologist or admin)
- **Credentials**: Authentication information

**Key Operations**:
- User login with email and password
- User logout (token invalidation)
- Create psychologist accounts
- Update psychologist profiles
- Role-based access control

**User Roles**:
- `ADMIN`: Full system access
- `PSYCHOLOGIST`: Limited to own patients and assessments
- (Game API specific roles as needed)

---

## API Structure

### Game API (`src/apps/game_api/`)

Public API for child patients to complete questionnaires.

**Loaded Modules**:
- `GameQuestionnairesModule`
- `GameResultsAnalysisModule`

**Endpoints**:
- `POST /questionnaires/validate-token`: Validate questionnaire access token
- `POST /questionnaires/{token}/answers`: Submit questionnaire answers
- Game-specific endpoints for assessment

**CORS**: Restricted to `GAME_URL`

---

### Web API (`src/apps/web_page_api/`)

Authenticated API for administrative operations.

**Loaded Modules**:
- `PatientsModule`
- `QuestionnairesModule`
- `ResultsAnalysisModule`
- `UsersManagementModule`

**Key Endpoints**:
- `POST /auth/login`: User authentication
- `POST /auth/logout`: User logout
- `POST /users/psychologists`: Create psychologist account
- `PUT /users/psychologists/{cedula}`: Update psychologist profile
- `GET /results/{cedula}/test_reports`: Fetch assessment reports
- `GET /patients/psychologists`: List psychologists
- `GET /patients/children`: List patient children

**CORS**: Restricted to `WEB_APP_URL`

---

## Database Design

### Core Concepts

The database uses **normalized relational design** with:
- Strong foreign key relationships
- Temporal tracking (created_at, updated_at)
- Audit trails for compliance

### Key Tables

```
users (Users)
  ├── id (PK)
  ├── email (Unique)
  ├── password_hash
  ├── role (admin | psychologist)
  └── timestamps

psychologists (Healthcare Providers)
  ├── id (PK)
  ├── cedula (Colombian ID)
  ├── user_id (FK → users)
  ├── professional_data
  └── timestamps

children (Patients)
  ├── id (PK)
  ├── name
  ├── age
  ├── sex
  ├── psychologist_id (FK → psychologists)
  └── timestamps

test_sessions (Assessment Sessions)
  ├── id (PK)
  ├── child_id (FK → children)
  ├── questionnaire_id (FK)
  ├── status (pending | in_progress | completed)
  ├── answers_submitted_at
  ├── time_taken
  └── timestamps

answers (Questionnaire Responses)
  ├── id (PK)
  ├── test_session_id (FK → test_sessions)
  ├── question_id
  ├── answer_value
  └── timestamps

test_reports (Analysis Results)
  ├── id (PK)
  ├── test_session_id (FK → test_sessions)
  ├── analysis_data (JSON)
  ├── generated_at
  └── timestamps
```

### Migration History

```
cdf38d148e35_initial_database_tables.py
  └─ Creates base schema (users, psychologists, children, etc.)

84f17ee79218_upgrade_test_session_columns.py
  └─ Adds/modifies test_session tracking fields

428c5429419c_add_time_taken_field_to_reports_table.py
  └─ Adds time_taken tracking to reports
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip

### Installation

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd hedan-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

4. **Configure environment**
   - Create `.env` file with required configuration
   - Set database connection string
   - Configure JWT secret keys
   - Set API URLs for CORS

5. **Initialize database**
   ```bash
   alembic upgrade head
   ```

6. **Run application**
   ```bash
   uvicorn src.apps.game_api.main:app --reload      # Game API
   uvicorn src.apps.web_page_api.main:app --reload  # Web API
   ```

---

## Development Guide

### Adding a New Module

1. **Create module directory**
   ```
   src/modules/new_module/
     ├── new_module_module.py
     ├── api/
     ├── application/
     ├── domain/
     └── infrastructure/
   ```

2. **Define domain models** in `domain/`
   - Create aggregates extending `AggregateRoot`
   - Define value objects extending `ValueObject`
   - Create repository interfaces

3. **Create handlers** in `application/`
   - Command handlers extending `CommandHandler`
   - Query handlers extending `QueryHandler`
   - Service implementations

4. **Create endpoints** in `api/`
   - Define routers with FastAPI
   - Use `@Injected()` for dependency injection

5. **Implement persistence** in `infrastructure/`
   - Create SQLAlchemy models
   - Implement repositories
   - Create query services

6. **Register module** in app setup
   - Add to modules list in `app_api/modules.py`
   - Module automatically installed via `ModuleInstaller`

### Creating a Command Handler

```python
from src.common.application.command import Command
from src.common.application.command_handler import CommandHandler

@dataclass(frozen=True)
class MyCommand(Command[str]):
    param: str

class MyCommandHandler(CommandHandler[MyCommand, str]):
    async def handle(self, command: MyCommand) -> str:
        # Business logic here
        return "result"
```

### Creating a Query Handler

```python
from src.common.application.query import Query
from src.common.application.query_handler import QueryHandler

@dataclass(frozen=True)
class MyQuery(Query[str]):
    param: str

class MyQueryHandler(QueryHandler[MyQuery, str]):
    async def handle(self, query: MyQuery) -> str:
        # Query logic here
        return "result"
```

### Publishing Domain Events

```python
from src.common.application.event_bus import EventBus

class MyAggregate(AggregateRoot):
    def do_something(self, event_bus: EventBus):
        # Business logic
        event_bus.publish(MyDomainEvent(...))
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

### Testing

- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- Use pytest framework

---

## Authentication & Authorization

### JWT Token Flow

1. **Login**: User provides email/password → Receives JWT token
2. **Authenticated Requests**: Token included in `Authorization: Bearer <token>` header or `accessToken` cookie
3. **Validation**: JWT verified at handler level
4. **Authorization**: Role-based access control applied

### Available Authorization Functions

- `admin_only()`: Requires ADMIN role
- `psychologist_only()`: Requires PSYCHOLOGIST role
- `psychologist_with_cedula()`: Requires matching cedula
- `psychologist_with_cedula_or_admin()`: Flexible access control

### Cookie Management

The `AuthCookieMiddleware` automatically converts cookies to headers for seamless authentication across client types.

---

## Logging & Monitoring

### Logging Levels

- **INFO**: Normal operations logged
- **WARNING**: Potential issues
- **ERROR**: Failure conditions
- **DEBUG**: Detailed diagnostic info

### Log Destinations

- Console output during development
- Better Stack service for production (via logtail-python)
- Request/response logging via middleware

---

## Performance Considerations

### Async/Await

All database operations are async using:
- `asyncpg` for PostgreSQL driver
- `SQLAlchemy async sessions`
- Async handlers throughout

### Connection Pooling

SQLAlchemy manages connection pools automatically.

### Query Optimization

- Use repository pattern to encapsulate queries
- Create query services for complex reads
- Leverage SQLAlchemy query optimization

---

## Error Handling

### HTTP Exception Mapping

Domain exceptions map to HTTP responses:
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Authentication failures
- `403 Forbidden`: Authorization failures
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Unhandled exceptions

### Domain Exceptions

Create custom exceptions in domain layer:

```python
class InvalidCredentialsException(Exception):
    pass
```

---

## API Documentation

Both APIs expose auto-generated documentation:

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

URLs configured via environment variables.

---

## Contributing

1. Create feature branch from `main`
2. Follow modular architecture
3. Add tests for new functionality
4. Ensure async/await patterns
5. Document public APIs
6. Submit pull request

---

## License

[Insert License Information]

---

## Support

For questions or issues, please contact the development team.

