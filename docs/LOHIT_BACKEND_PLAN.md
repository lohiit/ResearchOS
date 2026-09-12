# Lohit's Backend Build Plan

This is the ordered plan for the `feature/backend-foundation` branch. Build one
step at a time: understand the goal, make the smallest change, run it, test it,
commit it, and only then continue.

## Working rules

1. Work only on `feature/backend-foundation`.
2. Keep backend code inside `backend/`.
3. Start every session with `git branch --show-current` and `git status`.
4. Do not merge or pull Shiva's frontend branch.
5. Never commit `.venv`, secrets, `.env`, databases, or generated files.
6. Make one focused commit after every working milestone.

## Phase 0 — Environment check

**Goal:** Confirm the local Python environment and Git branch are ready.

**You will learn:** virtual environments, Python packages, Git status.

**Done when:** Python runs from `.venv`, FastAPI is importable, and Git is clean.

## Phase 1 — FastAPI foundation

**Goal:** Start a minimal FastAPI application.

**You will learn:** Python packages, application entry points, ASGI, Uvicorn,
and Swagger/OpenAPI.

**Build:**

- `backend/app/main.py`
- a versioned `GET /api/v1/health` endpoint
- one automated test for that endpoint

**Done when:** `/docs` opens locally and `/api/v1/health` returns a small JSON
response.

## Phase 2 — Configuration and environment variables

**Goal:** Give the backend one typed, central location for configuration.

**You will learn:** environment variables, `.env.example`, Pydantic settings,
and why secrets must not be hard-coded.

**Build:**

- `backend/app/core/config.py`
- settings for the app name, environment, API prefix, and database URL
- a safe `.env.example` update with placeholder values only

**Done when:** the API starts using values from the environment without exposing
secrets.

## Phase 3 — API structure and error handling

**Goal:** Establish a consistent API structure before adding business features.

**You will learn:** routers, request/response schemas, HTTP status codes, and
validation errors.

**Build:**

- `api/v1` router registration
- a shared API error format
- a small example request/response schema

**Done when:** routes are versioned under `/api/v1` and invalid input produces a
clear JSON error.

## Phase 4 — Database foundation

**Goal:** Connect FastAPI to PostgreSQL safely.

**You will learn:** relational databases, connection URLs, SQLAlchemy sessions,
migrations, and why PostgreSQL is the system of record.

**Build:**

- SQLAlchemy engine and session setup
- Alembic migration setup
- a database health/readiness check

**Done when:** a migration can create and remove a simple test table locally.

## Phase 5 — Users and authentication

**Goal:** Identify users securely.

**You will learn:** password hashing, JWT access tokens, authentication versus
authorization, and Pydantic validation.

**Build:**

- `users` database model and migration
- register, login, and current-user endpoints
- password hashing and token creation
- tests for registration, login, and invalid credentials

**Done when:** a user can register, log in, and retrieve their own profile.

## Phase 6 — Workspaces and membership roles

**Goal:** Create the collaboration boundary for all research data.

**You will learn:** foreign keys, ownership, role-based access, and service-layer
logic.

**Build:**

- `workspaces` and `workspace_members` models and migrations
- OWNER, EDITOR, and VIEWER roles
- create/list/read/update workspace endpoints
- authorization checks

**Done when:** one user cannot access a workspace unless they are a member.

## Phase 7 — Document metadata

**Goal:** Model documents before handling physical file uploads.

**You will learn:** resource-oriented APIs, database relationships, enums, and
document-processing states.

**Build:**

- `documents` model and migration
- document source and processing-status fields
- create/list/get/delete metadata endpoints scoped to a workspace

**Done when:** a workspace can own document records and they are authorization
protected.

## Phase 8 — File upload and object storage

**Goal:** Store original PDFs outside PostgreSQL.

**You will learn:** multipart uploads, MIME/size validation, object storage, and
storage keys.

**Build:**

- MinIO local configuration
- validated PDF upload endpoint
- storage service abstraction
- document metadata updates after upload

**Done when:** a PDF is stored in MinIO while PostgreSQL stores only its metadata
and storage key.

## Phase 9 — PDF extraction and chunking

**Goal:** Convert a document into traceable, searchable content.

**You will learn:** PyMuPDF, page extraction, text cleaning, token-based chunking,
and provenance metadata.

**Build:**

- page-aware PDF extraction
- structure-aware chunking
- chunk metadata: document, page range, index, text, and content hash
- tests using a small fixture PDF

**Done when:** a PDF can be inspected page-by-page and chunk-by-chunk.

## Phase 10 — Background processing

**Goal:** Run expensive document processing outside the web request.

**You will learn:** synchronous versus asynchronous work, Redis, Celery, retries,
and processing states.

**Build:**

- Redis and Celery configuration
- document-processing task
- `PENDING`, `PROCESSING`, `READY`, and `FAILED` status transitions
- retry/error handling

**Done when:** upload returns quickly while a background worker processes the PDF.

## Phase 11 — Embeddings and Qdrant

**Goal:** Index document chunks for semantic retrieval.

**You will learn:** embeddings, vectors, cosine similarity, Qdrant collections,
and payload filters.

**Build:**

- embedding provider interface
- BGE-M3 implementation
- Qdrant collection and upsert logic
- workspace/document/page payload metadata

**Done when:** processed chunks are stored in Qdrant with enough information to
resolve their source evidence.

## Phase 12 — Semantic search

**Goal:** Return relevant chunks for a natural-language query.

**You will learn:** query embeddings, top-K retrieval, relevance scores, and
workspace-scoped filtering.

**Build:**

- `POST /api/v1/search`
- query validation
- Qdrant retrieval filtered by workspace ID
- response schemas containing evidence metadata

**Done when:** users receive relevant results without seeing chunks from another
workspace.

## Phase 13 — Reranking and grounded answers

**Goal:** Improve search precision and answer only from retrieved evidence.

**You will learn:** first-stage retrieval, reranking, context construction, LLM
provider interfaces, and hallucination controls.

**Build:**

- reranker interface and BGE reranker implementation
- LLM provider abstraction
- conversation/message models
- evidence-context builder
- answer endpoint that records citations

**Done when:** an answer links every important claim to stored document evidence.

## Phase 14 — Research workspace features

**Goal:** Add research-specific product value after the core pipeline works.

**Build, one feature at a time:**

- notes and annotations
- paper comparison
- entities and relationships in PostgreSQL
- research reports

**Done when:** each feature has its own API, authorization checks, tests, and a
clear evidence trail where relevant.

## Phase 15 — Quality and deployment

**Goal:** Make the backend reproducible and observable.

**You will learn:** Docker, environment separation, CI, logs, metrics, rate
limiting, and production-safe deployment.

**Build:**

- Docker and Docker Compose
- database migrations in deployment
- GitHub Actions tests
- structured logging and health/readiness checks
- rate limiting, backups, and monitoring as needed

**Done when:** a fresh machine can run the backend with documented commands and
tests pass automatically.

## Commit rhythm

Use a focused commit only after a step works, for example:

```text
Add health endpoint
Add application settings
Set up database session
Add workspace authorization
```

Avoid combining unrelated work in one commit. Before every commit, run the
relevant tests and inspect `git status`.
