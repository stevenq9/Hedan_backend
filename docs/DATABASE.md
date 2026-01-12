# Database Schema Documentation

## Overview

HEDAN Backend uses PostgreSQL as its primary relational database. The schema is organized around domain concepts with proper normalization and referential integrity.

---

## Core Entities & Relationships

```
┌─────────────────┐
│     Users       │ (Authentication)
├─────────────────┤
│ id (PK)         │
│ email (U)       │
│ password_hash   │
│ role            │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:1
         │
    ┌────▼──────────────┐
    │  Psychologists    │ (Healthcare Providers)
    ├───────────────────┤
    │ id (PK)           │
    │ user_id (FK)      │ ──→ Users
    │ cedula (U)        │ (Colombian ID)
    │ name              │
    │ specialization    │
    │ created_at        │
    │ updated_at        │
    └────┬──────────────┘
         │
         │ 1:N
         │
    ┌────▼──────────────┐
    │    Children       │ (Patients)
    ├───────────────────┤
    │ id (PK)           │
    │ psychologist_id   │ ──→ Psychologists
    │ (FK)              │
    │ name              │
    │ age               │
    │ sex               │
    │ created_at        │
    │ updated_at        │
    └────┬──────────────┘
         │
         │ 1:N
         │
    ┌────▼────────────────────┐
    │   Test Sessions          │ (Assessments)
    ├────────────────────────┤
    │ id (PK)                │
    │ child_id (FK)          │ ──→ Children
    │ questionnaire_id (FK)  │ ──→ Questionnaires
    │ status                 │
    │ token                  │
    │ created_at             │
    │ answers_submitted_at   │
    │ time_taken_seconds     │
    │ updated_at             │
    └────┬───────────────────┘
         │
         │ 1:N
         │
    ┌────▼──────────────┐
    │    Answers        │ (Responses)
    ├───────────────────┤
    │ id (PK)           │
    │ test_session_id   │ ──→ TestSessions
    │ (FK)              │
    │ question_id (FK)  │ ──→ Questions
    │ answer_value      │
    │ created_at        │
    └───────────────────┘
         
┌──────────────────────────────────┐
│      Questionnaires              │ (Assessment Templates)
├──────────────────────────────────┤
│ id (PK)                          │
│ name                             │
│ description                      │
│ version                          │
│ is_active                        │
│ created_at                       │
│ updated_at                       │
└────┬─────────────────────────────┘
     │
     │ 1:N
     │
┌────▼──────────────────┐
│     Questions         │ (Assessment Items)
├───────────────────────┤
│ id (PK)               │
│ questionnaire_id (FK) │ ──→ Questionnaires
│ text                  │
│ type                  │
│ options (JSON)        │
│ sequence              │
│ created_at            │
│ updated_at            │
└───────────────────────┘

┌──────────────────────────────────┐
│      Test Reports                │ (Analysis Results)
├──────────────────────────────────┤
│ id (PK)                          │
│ test_session_id (FK)             │ ──→ TestSessions
│ analysis_data (JSONB)            │
│ summary_scores (JSONB)           │
│ interpretation                   │
│ recommendations                  │
│ generated_at                     │
│ created_at                       │
└──────────────────────────────────┘
```

---

## Table Definitions

### `users` Table

Stores all system users with role-based access.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('ADMIN', 'PSYCHOLOGIST')),
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT email_not_empty CHECK (LENGTH(email) > 0)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

**Columns:**
- `id`: Unique identifier (UUID)
- `email`: User email address (unique)
- `password_hash`: Bcrypt-hashed password
- `role`: User type (ADMIN or PSYCHOLOGIST)
- `is_active`: Account status
- `last_login`: Last authentication timestamp
- `created_at`: Record creation timestamp
- `updated_at`: Last record modification timestamp

---

### `psychologists` Table

Stores healthcare provider information.

```sql
CREATE TABLE psychologists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    specialization VARCHAR(255),
    phone VARCHAR(20),
    license_number VARCHAR(100),
    bio TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_psychologists_cedula ON psychologists(cedula);
CREATE INDEX idx_psychologists_user_id ON psychologists(user_id);
```

**Columns:**
- `id`: Unique identifier
- `user_id`: Reference to user account (1:1)
- `cedula`: Colombian national ID
- `name`: Full name
- `specialization`: Professional specialization
- `phone`: Contact number
- `license_number`: Professional license
- `bio`: Professional biography

---

### `children` Table

Stores patient (child) information.

```sql
CREATE TABLE children (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    psychologist_id UUID NOT NULL REFERENCES psychologists(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 0 AND age <= 120),
    sex VARCHAR(20) CHECK (sex IN ('MALE', 'FEMALE', 'OTHER')),
    identification_number VARCHAR(50),
    notes TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_children_psychologist_id ON children(psychologist_id);
CREATE INDEX idx_children_is_active ON children(is_active);
```

**Columns:**
- `id`: Unique identifier
- `psychologist_id`: Reference to assigned psychologist (required)
- `name`: Child's name
- `age`: Child's age in years
- `sex`: Gender/sex
- `identification_number`: Optional government ID
- `notes`: Clinical notes
- `is_active`: Active patient status

---

### `questionnaires` Table

Stores assessment templates.

```sql
CREATE TABLE questionnaires (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    estimated_duration_minutes INTEGER,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP
);

CREATE INDEX idx_questionnaires_is_active ON questionnaires(is_active);
CREATE INDEX idx_questionnaires_created_by ON questionnaires(created_by);
```

**Columns:**
- `id`: Unique identifier
- `name`: Assessment name
- `description`: Assessment description
- `version`: Version number
- `is_active`: Whether questionnaire is in use
- `estimated_duration_minutes`: Expected completion time
- `created_by`: Administrator who created it
- `published_at`: Publication timestamp

---

### `questions` Table

Stores individual assessment questions.

```sql
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    questionnaire_id UUID NOT NULL REFERENCES questionnaires(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('MULTIPLE_CHOICE', 'SHORT_ANSWER', 'RATING', 'ESSAY')),
    options JSONB,
    sequence INTEGER NOT NULL,
    points_possible INTEGER DEFAULT 1,
    is_required BOOLEAN DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_questions_questionnaire_id ON questions(questionnaire_id);
CREATE INDEX idx_questions_sequence ON questions(questionnaire_id, sequence);
```

**Columns:**
- `id`: Unique identifier
- `questionnaire_id`: Reference to parent questionnaire (required)
- `text`: Question text
- `type`: Question type (MULTIPLE_CHOICE, SHORT_ANSWER, etc.)
- `options`: JSON array of possible answers
- `sequence`: Display order
- `points_possible`: Maximum points for this question
- `is_required`: Whether answer is required

**Options Example:**
```json
["Option A", "Option B", "Option C", "Option D"]
```

---

### `test_sessions` Table

Stores assessment sessions for children.

```sql
CREATE TABLE test_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    child_id UUID NOT NULL REFERENCES children(id) ON DELETE CASCADE,
    questionnaire_id UUID NOT NULL REFERENCES questionnaires(id),
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (
        status IN ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'ABANDONED')
    ),
    invitation_token VARCHAR(255) UNIQUE,
    token_expires_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    answers_submitted_at TIMESTAMP,
    time_taken_seconds INTEGER,
    ip_address VARCHAR(45),
    user_agent TEXT,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_test_sessions_child_id ON test_sessions(child_id);
CREATE INDEX idx_test_sessions_questionnaire_id ON test_sessions(questionnaire_id);
CREATE INDEX idx_test_sessions_status ON test_sessions(status);
CREATE INDEX idx_test_sessions_token ON test_sessions(invitation_token);
```

**Columns:**
- `id`: Unique identifier
- `child_id`: Reference to child (required)
- `questionnaire_id`: Reference to questionnaire (required)
- `status`: Current session status
- `invitation_token`: Unique token for child to access test
- `token_expires_at`: When invitation token expires
- `started_at`: When child began test
- `answers_submitted_at`: When answers were submitted
- `time_taken_seconds`: Duration to complete
- `ip_address`: Child's IP address (optional)
- `user_agent`: Child's browser info (optional)

---

### `answers` Table

Stores individual question responses.

```sql
CREATE TABLE answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_session_id UUID NOT NULL REFERENCES test_sessions(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES questions(id),
    answer_value TEXT NOT NULL,
    points_earned INTEGER,
    is_correct BOOLEAN,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_test_session_question UNIQUE(test_session_id, question_id)
);

CREATE INDEX idx_answers_test_session_id ON answers(test_session_id);
CREATE INDEX idx_answers_question_id ON answers(question_id);
```

**Columns:**
- `id`: Unique identifier
- `test_session_id`: Reference to test session (required)
- `question_id`: Reference to question (required)
- `answer_value`: The submitted answer
- `points_earned`: Calculated score
- `is_correct`: Whether answer was correct (if applicable)

---

### `test_reports` Table

Stores analysis results and reports.

```sql
CREATE TABLE test_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_session_id UUID NOT NULL UNIQUE REFERENCES test_sessions(id) ON DELETE CASCADE,
    raw_scores JSONB,
    processed_scores JSONB,
    percentiles JSONB,
    summary_interpretation TEXT,
    detailed_analysis TEXT,
    recommendations TEXT,
    score DECIMAL(5,2),
    score_category VARCHAR(50),
    time_taken_seconds INTEGER,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    generated_by UUID REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_test_reports_test_session_id ON test_reports(test_session_id);
CREATE INDEX idx_test_reports_generated_at ON test_reports(generated_at);
```

**Columns:**
- `id`: Unique identifier
- `test_session_id`: Reference to test session (required, unique)
- `raw_scores`: JSONB with raw score data
- `processed_scores`: JSONB with normalized scores
- `percentiles`: JSONB with percentile rankings
- `summary_interpretation`: Executive summary
- `detailed_analysis`: Detailed findings
- `recommendations`: Clinical recommendations
- `score`: Overall score
- `score_category`: Score classification (e.g., "HIGH", "MEDIUM", "LOW")
- `generated_by`: System or user that generated report

**Raw Scores Example:**
```json
{
  "attention": 85,
  "memory": 92,
  "processing_speed": 78,
  "total": 255
}
```

---

## Key Constraints & Rules

### Primary Key Strategy
- All tables use UUID (`gen_random_uuid()`) as primary key
- Provides distributed generation and better privacy

### Foreign Key Relationships
- All foreign keys are required (NOT NULL) except where optional
- CASCADE delete for owned entities (questions owned by questionnaires)
- RESTRICT delete for shared references (prevent accidental deletion)

### Unique Constraints
- `users.email`: One account per email
- `psychologists.cedula`: One psychologist per ID
- `questionnaires.name`: No duplicate questionnaire names
- `test_sessions.invitation_token`: Unique per session
- `test_reports.test_session_id`: One report per session

### Check Constraints
- `users.role IN ('ADMIN', 'PSYCHOLOGIST')`
- `children.age >= 0 AND age <= 120`
- `test_sessions.status IN (...)`
- `questions.type IN (...)`

---

## Indexing Strategy

### Performance Indexes
| Table | Column | Purpose |
|-------|--------|---------|
| users | email | Fast lookups by email |
| users | role | Filter by role |
| psychologists | cedula | Fast lookup by ID |
| children | psychologist_id | Find all children |
| test_sessions | child_id | Find sessions by child |
| test_sessions | status | Filter by status |
| test_sessions | token | Validate invitation |
| answers | test_session_id | Get answers by session |
| questions | questionnaire_id, sequence | Ordered questions |

### Indexes Not Applied (Avoid Over-Indexing)
- Foreign keys not separately indexed (used mainly for joins)
- Rarely filtered columns
- Columns in complex composite queries (handled by query optimizer)

---

## JSONB Fields

The schema uses JSONB for flexible data storage:

### questionnaires.options
```json
["Option A", "Option B", "Option C", "Option D"]
```

### test_reports.raw_scores
```json
{
  "attention": 85,
  "memory": 92,
  "processing_speed": 78,
  "total": 255
}
```

### test_reports.processed_scores
```json
{
  "attention_normalized": 0.85,
  "memory_normalized": 0.92,
  "processing_speed_normalized": 0.78
}
```

---

## Migration History

### Migration 1: `cdf38d148e35_initial_database_tables.py`
Initial schema creation with core tables:
- users
- psychologists
- children
- questionnaires
- questions
- test_sessions
- answers

### Migration 2: `84f17ee79218_upgrade_test_session_columns.py`
Enhancements to test_sessions table:
- Added `ip_address` for tracking
- Added `user_agent` for browser tracking
- Added `started_at` timestamp
- Modified status check constraints

### Migration 3: `428c5429419c_add_time_taken_field_to_reports_table.py`
Added timing tracking to reports:
- Added `time_taken_seconds` to test_reports
- Added `token_expires_at` to test_sessions

---

## Views (Useful Queries)

### Active Psychologists with Patient Count
```sql
CREATE VIEW psychologist_stats AS
SELECT 
    p.id,
    p.name,
    p.cedula,
    COUNT(DISTINCT c.id) as patient_count,
    COUNT(DISTINCT ts.id) as total_assessments
FROM psychologists p
LEFT JOIN children c ON p.id = c.psychologist_id
LEFT JOIN test_sessions ts ON c.id = ts.child_id
WHERE u.is_active = true
GROUP BY p.id, p.name, p.cedula;
```

### Recent Assessment Results
```sql
SELECT 
    c.name as child_name,
    q.name as questionnaire_name,
    tr.score,
    tr.score_category,
    ts.answers_submitted_at
FROM test_reports tr
JOIN test_sessions ts ON tr.test_session_id = ts.id
JOIN children c ON ts.child_id = c.id
JOIN questionnaires q ON ts.questionnaire_id = q.id
ORDER BY ts.answers_submitted_at DESC
LIMIT 20;
```

---

## Backup Strategy

### Daily Backups
```bash
# Full backup
pg_dump hedan_dev > hedan_backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump hedan_dev | gzip > hedan_backup_$(date +%Y%m%d).sql.gz

# Restore
psql hedan_dev < hedan_backup_20240112.sql
```

### Point-in-Time Recovery
Ensure WAL (Write-Ahead Logging) is enabled for production:
```
wal_level = replica
archive_mode = on
```

---

## Performance Considerations

### Connection Pooling
SQLAlchemy async with asyncpg handles connection pooling:
- Default pool size: 10
- Max overflow: 10
- Pool timeout: 30 seconds

### Query Optimization
- Use indexes for WHERE clauses
- Use selectinload for relationships
- Avoid N+1 queries with eager loading
- Pagination for large result sets

### JSONB Performance
- JSONB fields support GIN indexes for complex queries
- Example: `CREATE INDEX idx_scores ON test_reports USING gin(processed_scores)`

---

## Data Retention Policy

### Recommended Retention
- User accounts: Keep indefinitely
- Test sessions: Keep 7 years (regulatory)
- Answers: Keep with test sessions
- Reports: Keep 10 years (medical records)
- Audit logs: Keep 3 years

### Anonymization
```sql
-- Anonymize old completed sessions
UPDATE children SET name = 'ANON_' || SUBSTRING(id::text, 1, 8)
WHERE created_at < NOW() - INTERVAL '5 years';
```

---

## Monitoring Queries

### Table Sizes
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Index Usage
```sql
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

### Slow Queries
```sql
SELECT 
    query,
    calls,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

