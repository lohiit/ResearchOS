# ResearchOS

ResearchOS is a full-stack collaborative research intelligence platform for collecting technical documents, searching them semantically, asking evidence-grounded questions, comparing sources, discovering relationships between concepts/papers, and generating research reports with traceable citations.

> **Mental model:** Google Drive + semantic search + RAG + research assistant + knowledge graph + collaboration.

## Project status

**Planning complete. Implementation has not yet begun.**

This repository is intentionally starting from a clean slate. The architecture will grow incrementally rather than creating every folder and service on day one.

## Problem

Research information is scattered across PDFs, papers, websites, notes, documentation, bookmarks, and URLs. Keyword search is often insufficient for conceptual questions. Generic LLMs can hallucinate or provide answers without reliable evidence. Comparing multiple papers manually is tedious, and relationships between concepts and papers remain hidden in folders.

ResearchOS centralizes the research workflow and makes evidence traceable.

## User journey

1. User opens ResearchOS.
2. User creates a workspace, e.g. `LLM Research`.
3. User uploads research documents such as PDFs.
4. The system stores the original file and creates document metadata.
5. Document processing runs as a background job.
6. Text is extracted page-by-page.
7. Text is cleaned and divided into meaningful chunks.
8. Chunks are embedded and indexed in Qdrant.
9. User performs semantic search.
10. For questions, relevant chunks are retrieved and reranked.
11. The LLM receives only the selected evidence plus instructions.
12. The answer is returned with citations.
13. Citation IDs resolve to document/chunk/page evidence.
14. Later, the user can compare papers, create notes/annotations, explore relationships, and generate research reports.

## Core architecture

```text
                         USER
                           |
                           v
                 React + TypeScript
                       Frontend
                           |
                     HTTPS / JSON
                           |
                           v
                     FastAPI API
                           |
       +-------------------+-------------------+
       |                   |                   |
       v                   v                   v
 PostgreSQL             Redis               Qdrant
       |                   |                   |
       |                   v                   |
       |                Celery                 |
       |                   |                   |
       |           +-------+-------+            |
       |           |               |            |
       |        Ingestion          AI           |
       |                           |            |
       |                           v            |
       |                          LLM           |
       |                                        |
       +------------- Object Storage -----------+
```

## Responsibilities

### React + TypeScript
Application UI, navigation, dashboard, workspace pages, document interface, search, chat, comparison, graph, notes, settings.

### FastAPI
REST API, validation, authentication, authorization, business logic, orchestration between application services.

### PostgreSQL
System of record for users, workspaces, memberships, documents, chunks, notes, annotations, conversations, messages, citations, reports, entities, and relationships.

### Qdrant
Vector retrieval engine for semantic search, filtering, and later hybrid retrieval.

### MinIO / S3-compatible storage
Stores original documents. PostgreSQL stores metadata and storage keys rather than large PDF binaries.

### Redis + Celery
Queues and executes expensive background jobs such as document processing.

### BGE-M3
Creates embeddings for document chunks and search queries.

### BGE reranker
Reranks retrieved candidates based on query-passage relevance.

### LLM provider
Generates answers and later performs structured research tasks. Use a provider abstraction rather than coupling the whole system to one vendor.

## RAG pipeline

```text
User question
    |
Query cleaning
    |
Query embedding
    |
Qdrant retrieval
    |
~30 candidates
    |
Reranker
    |
~8 evidence chunks
    |
Context builder
    |
LLM
    |
Answer + citations
```

The model must not be treated as the source of truth. Retrieved evidence is the source of truth.

## Citation model

A generated citation must resolve through a real internal mapping:

```text
citation_id
    |
message
    |
chunk_id
    |
document_id
    |
page / offsets
    |
source document
```

The frontend should eventually let users click a citation and inspect the corresponding evidence.

## Database model

Core entities:

```text
users
workspaces
workspace_members
documents
document_versions
document_chunks
notes
annotations
conversations
messages
citations
research_reports
entities
relationships
```

Workspace roles:

```text
OWNER
EDITOR
VIEWER
```

Document source types:

```text
UPLOAD
URL
ARXIV
```

## Document ingestion

Target ingestion flow:

```text
Upload
 -> Object storage
 -> PostgreSQL document record (PROCESSING)
 -> Redis/Celery job
 -> Download/read file
 -> Extract pages
 -> Clean text
 -> Structure-aware chunking
 -> Generate embeddings
 -> Store vectors + metadata in Qdrant
 -> PostgreSQL status READY
```

Initial chunking target: approximately 500-800 tokens with overlap, while attempting to preserve document structure such as sections and paragraphs. This is a tunable engineering parameter, not a permanent law.

## Search

Initial search:

```text
query
 -> embedding
 -> Qdrant
 -> top-K
```

Later:

```text
                query
                  |
        +---------+---------+
        |                   |
   dense search         lexical/BM25
        |                   |
        +---------+---------+
                  |
                fusion
                  |
              reranker
                  |
             top chunks
```

Hybrid retrieval is a later improvement.

## Research comparison

Users can select multiple documents and criteria such as:

- methodology
- performance
- datasets
- limitations
- memory behavior
- computational characteristics

The comparison output should be evidence-backed wherever possible.

## Knowledge graph

Initially use PostgreSQL:

```text
entities
- id
- workspace_id
- name
- type

relationships
- source_id
- target_id
- relationship_type
```

Example:

```text
FlashAttention
  |-- improves --> Attention
  |-- builds_on --> Transformer
  |-- related_to --> FlashAttention-2
```

Do not introduce Neo4j unless graph requirements later justify it.

## Research agent

Only after basic RAG is reliable.

Example orchestration:

```text
Research request
      |
    Planner
      |
+-----+---------+---------+
|               |         |
Search        Compare   Timeline
|               |         |
+---------------+---------+
        |
Evidence verification
        |
Report generation
```

Roles should be explicit: planner, researcher, analyst, verifier, writer. Agents are not added merely because "agents are cool."

## Evaluation

Eventually create a benchmark dataset such as:

```json
[
  {
    "question": "What is the complexity of self-attention?",
    "expected_sources": ["attention_paper.pdf"]
  }
]
```

Measure:

### Retrieval
- Precision@K
- Recall@K
- MRR
- nDCG

### Generation
- citation correctness
- answer faithfulness
- answer relevance
- completeness

### System
- latency
- token usage
- cost
- failure rate

## Security

Eventually implement:

- password hashing
- JWT authentication
- workspace authorization
- role-based permissions
- input validation
- file validation
- secret management through environment variables
- rate limiting
- safe object-storage access
- tenant/workspace filters in retrieval

A retrieval query must not leak chunks from another workspace.

## API target

Authentication:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

Workspaces:

```text
POST   /api/v1/workspaces
GET    /api/v1/workspaces
GET    /api/v1/workspaces/{id}
PATCH  /api/v1/workspaces/{id}
DELETE /api/v1/workspaces/{id}
```

Documents:

```text
POST   /api/v1/workspaces/{id}/documents
GET    /api/v1/workspaces/{id}/documents
GET    /api/v1/documents/{id}
DELETE /api/v1/documents/{id}
POST   /api/v1/documents/{id}/upload
```

Search:

```text
POST /api/v1/search
```

Chat:

```text
POST /api/v1/conversations/{id}/messages
```

Research:

```text
POST /api/v1/research/compare
POST /api/v1/research/reports
GET  /api/v1/research/reports/{id}
```

## Target repository structure

The final target shape is approximately:

```text
researchos/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── workspaces.py
│   │   │   ├── documents.py
│   │   │   ├── search.py
│   │   │   ├── chat.py
│   │   │   └── research.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── workspace.py
│   │   │   ├── document.py
│   │   │   └── message.py
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── document_service.py
│   │   │   ├── search_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── citation_service.py
│   │   │   └── research_service.py
│   │   ├── ai/
│   │   │   ├── embeddings.py
│   │   │   ├── reranker.py
│   │   │   ├── llm.py
│   │   │   └── prompts/
│   │   ├── ingestion/
│   │   │   ├── pdf.py
│   │   │   ├── docx.py
│   │   │   ├── web.py
│   │   │   ├── chunker.py
│   │   │   └── pipeline.py
│   │   ├── workers/
│   │   │   ├── celery_app.py
│   │   │   └── tasks.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   └── migrations/
│   │   └── core/
│   │       ├── config.py
│   │       └── security.py
│   └── tests/
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── hooks/
│       ├── api/
│       ├── types/
│       └── lib/
├── docker/
├── compose.yaml
├── .github/
│   └── workflows/
├── docs/
├── .env.example
├── .gitignore
└── README.md
```

This is a target architecture. Do not create all directories on day one.

## Development roadmap

See `docs/ROADMAP.md`.

## Architecture details

See `docs/ARCHITECTURE.md`.

## Project specification

See `docs/PROJECT_SPEC.md`.

## Architecture decision log

See `docs/DECISIONS.md`.

## First implementation milestone

Start with environment verification, Git repository setup, minimal README/docs, frontend skeleton, backend skeleton, and a `/health` endpoint.

Do not implement AI/RAG first.
