# ResearchOS — Learning + Build Roadmap

## Guiding rule

Never "learn everything first."

For every phase:

```text
Concept
 -> tiny exercise
 -> ResearchOS implementation
 -> test
 -> document
```

---

## Phase 0 — Environment and Git

### Learn
- terminal basics
- directories/files
- Git concepts
- repository basics
- environment variables
- Python/Node versioning

### Build
- create repository
- create README
- create AGENTS.md
- create docs/
- add .gitignore
- add .env.example
- verify Git status

### Milestone
Clean repository with project documentation and no application logic.

---

## Phase 1 — Frontend fundamentals

### Learn just in time
- HTML structure
- CSS
- JavaScript basics
- TypeScript types/interfaces
- React components
- props/state
- Vite
- browser/client-server model
- HTTP
- JSON

### Build
Minimal React app with:
- ResearchOS title
- navigation placeholder
- basic workspace/dashboard placeholder

### Milestone
Frontend runs locally.

---

## Phase 2 — Backend fundamentals

### Learn
- Python project structure
- FastAPI
- routes
- GET/POST
- request/response
- status codes
- Pydantic
- dependency injection
- OpenAPI/Swagger

### Build
```text
GET /api/v1/health
```

Potential later practice:
```text
GET /api/v1/users
POST /api/v1/users
```

### Milestone
Backend runs and returns a health response.

---

## Phase 3 — Frontend ↔ Backend

### Learn
- fetch/HTTP client
- CORS
- API responses
- frontend environment variables

### Build
Frontend calls `/api/v1/health` and displays backend status.

### Milestone
First full-stack request works.

---

## Phase 4 — PostgreSQL

### Learn
- database/table
- primary key
- foreign key
- joins
- indexes
- transactions
- normalization
- SQLAlchemy 2.x
- Alembic

### Build
Start with:
- users
- workspaces
- workspace_members

### Milestone
FastAPI reads/writes real PostgreSQL data through SQLAlchemy.

---

## Phase 5 — Authentication + authorization

### Learn
- password hashing
- JWT
- bearer tokens
- authentication vs authorization
- role-based access

### Build
- register
- login
- current-user endpoint
- workspace access checks
- OWNER/EDITOR/VIEWER

### Milestone
User A cannot access User B's unauthorized workspace.

---

## Phase 6 — Documents + file upload

### Learn
- multipart/form-data
- file validation
- object storage
- MinIO
- storage keys

### Build
- create document metadata
- upload PDF
- store original file in MinIO
- save metadata in PostgreSQL
- document listing

### Milestone
A PDF can be uploaded and listed in a workspace.

---

## Phase 7 — PDF ingestion

### Learn
- PyMuPDF
- page-based extraction
- text cleaning
- chunking
- token concepts
- overlap
- content hashing

### Build
```text
PDF
 -> pages
 -> clean text
 -> chunks
```

Store chunks in PostgreSQL initially if useful for debugging and traceability.

### Milestone
A document can be inspected page-by-page and chunk-by-chunk.

---

## Phase 8 — Background jobs

### Learn
- synchronous vs asynchronous work
- queues
- workers
- Redis
- Celery
- retries
- task status

### Build
```text
upload
 -> PROCESSING
 -> Redis
 -> Celery
 -> extraction/chunking
 -> READY
```

### Milestone
HTTP upload returns without waiting for full document processing.

---

## Phase 9 — Embeddings + Qdrant

### Learn
- vectors
- embeddings
- cosine similarity
- vector databases
- payload filtering

### Build
```text
chunk
 -> BGE-M3
 -> Qdrant
```

Payload includes workspace/document/page/chunk metadata.

### Milestone
Indexed chunks can be retrieved semantically.

---

## Phase 10 — Semantic search

### Build
```text
query
 -> embedding
 -> Qdrant
 -> ranked chunks
```

Create a search UI with:
- query input
- result text
- document
- page
- similarity score
- evidence metadata

### Milestone
Natural-language questions retrieve conceptually relevant passages.

---

## Phase 11 — Reranking

### Learn
- first-stage retrieval vs reranking
- precision/recall tradeoffs

### Build
```text
Qdrant top 30
 -> BGE reranker
 -> top 8
```

### Milestone
Measure retrieval quality before/after reranking.

---

## Phase 12 — RAG

### Learn
- context windows
- prompt construction
- grounded generation
- hallucination controls

### Build
```text
question
 -> retrieve
 -> rerank
 -> context builder
 -> LLM
 -> answer
```

Use an LLM provider abstraction.

### Milestone
User can ask questions and receive evidence-grounded answers.

---

## Phase 13 — Citations

### Learn
- provenance
- citation mapping
- evidence traceability

### Build
- citation IDs
- citation persistence
- chunk/document/page resolution
- clickable evidence UI

### Milestone
Every important factual answer can point back to source evidence.

---

## Phase 14 — Paper comparison

### Build
```text
select documents
 -> criteria
 -> retrieve relevant evidence
 -> normalize
 -> generate comparison
 -> attach evidence
```

### Milestone
Multi-paper comparison works.

---

## Phase 15 — Notes + annotations

### Build
- notes
- selected-text annotations
- comments
- workspace association
- user association

### Milestone
ResearchOS becomes a research workspace rather than only an AI interface.

---

## Phase 16 — Knowledge graph

### Build
- entities
- relationships
- graph API
- graph visualization

Start with PostgreSQL.

Later optionally add AI-assisted extraction.

### Milestone
User can visualize relationships between papers/concepts/models.

---

## Phase 17 — Research agent

### Learn
- workflow orchestration
- planning
- tool use
- structured outputs
- verification

### Build custom orchestration first:
```text
Planner
 -> Researcher
 -> Analyst
 -> Verifier
 -> Writer
```

Use LangGraph only if the custom implementation becomes unnecessarily complex.

### Milestone
Broad research questions can trigger multiple coordinated retrieval/analysis steps.

---

## Phase 18 — Research reports

### Build
```text
question
 -> plan
 -> retrieve
 -> rerank
 -> claims
 -> verify
 -> outline
 -> sections
 -> citations
 -> validation
 -> report
```

### Milestone
Generate technical research reports with traceable references.

---

## Phase 19 — Evaluation

### Build benchmark dataset

Example:

```json
{
  "question": "...",
  "expected_sources": ["..."]
}
```

### Measure
- Precision@K
- Recall@K
- MRR
- nDCG
- citation correctness
- faithfulness
- relevance
- completeness
- latency
- cost
- failure rate

### Milestone
ResearchOS has measurable retrieval and generation quality.

---

## Phase 20 — Production engineering

### Learn/build
- Docker
- Docker Compose
- GitHub Actions
- CI
- automated tests
- deployment
- logging
- monitoring
- rate limiting
- caching
- secrets
- backups
- health checks

### Milestone
Reproducible production deployment.

---

## Final portfolio milestone

A user can:

```text
Register
 -> Create workspace
 -> Upload papers
 -> Watch processing status
 -> Search naturally
 -> Ask questions
 -> Inspect citations
 -> Compare papers
 -> Take notes
 -> Annotate evidence
 -> Explore graph
 -> Run research workflow
 -> Generate report
 -> Inspect evaluation metrics
```
