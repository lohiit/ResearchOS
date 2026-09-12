# ResearchOS — Architecture Reference

## System boundaries

### Frontend
Responsible for user interaction and presentation. It communicates with the backend over HTTPS/JSON and must not directly access PostgreSQL, Redis, Qdrant, or object storage credentials.

### API
FastAPI is the application boundary. It authenticates requests, validates input, checks authorization, calls services, and returns stable API schemas.

### Services
Business logic should live in services rather than route handlers.

### Persistence
PostgreSQL is the authoritative application database.

### Retrieval
Qdrant is the semantic retrieval system. It is not the system of record.

### Files
Object storage is the authoritative store for original binary documents.

### Async processing
Redis carries queued jobs; Celery workers execute expensive multi-step processing.

### AI
Embedding, reranking, and LLM providers live behind application interfaces.

## End-to-end upload flow

```text
React
  |
  | multipart/form-data
  v
FastAPI
  |
  +--> authenticate
  |
  +--> authorize workspace
  |
  +--> store original file
  |
  +--> create PostgreSQL document record
  |       status=PROCESSING
  |
  +--> enqueue Celery task
          |
          v
        Redis
          |
          v
      Celery Worker
          |
          +--> retrieve file
          +--> extract pages
          +--> clean text
          +--> structure-aware chunk
          +--> create embeddings
          +--> upsert Qdrant
          +--> mark PostgreSQL READY
```

## End-to-end question flow

```text
React
  |
  v
FastAPI
  |
  +--> authenticate
  +--> authorize workspace
  +--> create/load conversation
  |
  +--> embed query with BGE-M3
  |
  +--> Qdrant filter:
  |       workspace_id = current workspace
  |
  +--> retrieve candidate chunks
  |
  +--> rerank candidates
  |
  +--> build evidence context
  |
  +--> call LLM provider
  |
  +--> resolve/validate citation IDs
  |
  +--> persist message + citations
  |
  v
React renders answer + evidence
```

## Critical invariants

1. Every document belongs to a workspace.
2. Every retrieval operation is workspace-scoped.
3. A user cannot access another user's private workspace data without membership.
4. Original files are not stored as large binary values in PostgreSQL.
5. Every processed chunk retains enough metadata for evidence traceability.
6. Qdrant payload contains the identifiers needed to resolve chunks.
7. LLM output is not automatically treated as factual evidence.
8. Citation IDs must map to actual stored evidence.
9. Background processing must be retryable and observable.
10. Secrets must never be committed.

## Target backend module boundaries

```text
api/
  HTTP transport only

models/
  SQLAlchemy persistence models

schemas/
  Pydantic request/response models

services/
  business logic

ai/
  embedding/reranking/LLM interfaces and implementations

ingestion/
  file extraction and chunking

workers/
  Celery application and task entrypoints

db/
  database engine/session/migrations

core/
  configuration/security/shared infrastructure
```

## Target frontend module boundaries

```text
pages/
  route-level screens

components/
  reusable UI

api/
  HTTP client/query functions

hooks/
  reusable React logic

types/
  TypeScript API/domain types

lib/
  shared frontend utilities
```

## Security model

Authentication identifies a user.

Authorization determines whether that user can access a workspace/document.

Never rely only on frontend route guards. Backend authorization is authoritative.

Retrieval filters must include workspace scope.

## Storage model

PostgreSQL:

```text
metadata + relationships + application state
```

Object storage:

```text
PDF/DOCX/TXT/etc.
```

Qdrant:

```text
embeddings + retrieval payload
```

## Scaling path

Do not prematurely distribute everything.

Initial local environment:
- one FastAPI process
- one Celery worker
- PostgreSQL
- Redis
- Qdrant
- MinIO
- Vite dev server

Production can scale services independently later.

## Error model

Expected categories include:
- validation errors
- authentication errors
- authorization errors
- missing resources
- upload/storage errors
- extraction errors
- embedding errors
- vector-store errors
- LLM provider errors
- background-job failures

Expose stable API errors to the frontend and retain detailed server logs internally.

## Observability path

Later capture:
- request latency
- document-processing duration
- retrieval latency
- reranking latency
- LLM latency
- token usage
- failures
- queue depth
- document processing status

OpenTelemetry is a later-stage addition.
