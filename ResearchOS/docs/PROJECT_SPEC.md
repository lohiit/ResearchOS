# ResearchOS — Complete Project Specification

## 1. Product definition

ResearchOS is a full-stack research information system. The AI layer uses RAG, semantic search, reranking, agents, and eventually ML/evaluation, but the product itself is broader than an AI chatbot.

One-line definition:

> ResearchOS is a collaborative research workspace that lets users collect technical documents, search them semantically, ask evidence-grounded questions, compare sources, discover relationships between concepts/papers, and generate research reports with traceable citations.

Mental model:

> Google Drive + semantic search + RAG + research assistant + knowledge graph + collaboration.

## 2. Problems solved

### Information fragmentation
Research knowledge is distributed across PDFs, websites, papers, notes, documentation, bookmarks, and URLs.

### Keyword-search limitations
Conceptual questions often do not contain the exact words used in the source. Semantic retrieval is needed.

### LLM hallucination
Answers must be grounded in retrieved evidence and expose the evidence to the user.

### Manual comparison
Comparing methodology, datasets, performance, limitations, and other criteria across multiple papers is tedious.

### Hidden relationships
Papers and concepts have relationships that are not visible when files are simply stored in folders.

## 3. Product surfaces

### Dashboard
Shows workspaces and counts such as documents, notes, comparisons.

### Workspace
Contains:
- Documents
- Search
- AI Researcher
- Notes
- Graph
- Comparisons

### Documents
Initial upload support: PDF.
Later: URL, arXiv paper, DOCX, TXT, web pages.

### Search
Natural-language semantic search with evidence snippets.

### AI Researcher
Question answering over the workspace with citations.

### Comparison
Select multiple documents and criteria; generate an evidence-backed comparison.

### Reports
Generate structured technical research reports with references.

### Notes and annotations
Personal or workspace research knowledge.

### Graph
Visualize entities and relationships.

## 4. Ingestion architecture

### Upload
Frontend sends multipart/form-data to FastAPI.

### Storage
Original file goes to object storage.

### Metadata
PostgreSQL stores:
- document ID
- workspace ID
- filename
- title
- storage key
- MIME type
- size
- source type
- source URL if applicable
- processing status
- page count
- timestamps

### Processing
A Celery task processes the document asynchronously.

### Extraction
PDF -> PyMuPDF.
DOCX -> python-docx.
Web -> Trafilatura.

### Structured representation
Do not retain only a giant document string. Preserve pages:

```text
document
  pages[]
    page_number
    text
```

This is required for later page-level evidence.

### Chunking
Prefer structure-aware chunking:
section -> paragraphs -> chunks.

Initial target:
- approximately 500-800 tokens
- overlap
- preserve page and section metadata
- tune experimentally

Chunk fields include:
- document ID
- chunk index
- text
- page start
- page end
- section title
- token count
- content hash

## 5. Embeddings

Use BAAI/bge-m3 initially.

Pipeline:

```text
chunk
 -> BGE-M3
 -> 1024-dimensional vector
```

The query is embedded using the same retrieval representation.

## 6. Vector database

Qdrant stores:
- vector
- payload metadata

Payload should include enough information to filter and trace evidence, including:
- workspace ID
- document ID
- page
- section
- chunk index

Workspace filtering is mandatory.

## 7. Retrieval

Initial:

```text
question
 -> embedding
 -> Qdrant
 -> top 20/30 candidates
```

Then rerank:

```text
30 candidates
 -> BGE-reranker-v2-m3
 -> top 8
```

The reranker receives query + passage and produces a direct relevance score.

Later hybrid search:

```text
dense retrieval + lexical/BM25
 -> fusion
 -> reranker
 -> final evidence
```

Hybrid retrieval is not a day-one requirement.

## 8. RAG

Context builder creates a prompt containing:

System role:
- research assistant
- answer only from supplied evidence
- never invent citations
- say when evidence is insufficient
- cite important factual claims

Then evidence blocks containing:
- document title
- page
- section
- chunk text

Then the user question.

LLM generates answer.

## 9. LLM abstraction

Create a provider abstraction:

```python
class LLMProvider:
    def generate(self, prompt, context):
        ...
```

Providers may eventually include:
- GeminiProvider
- OpenAIProvider
- LocalProvider

Initial generation provider: Gemini 3.6 Flash.

Do not make the rest of the application depend directly on Gemini-specific calls.

## 10. Citation architecture

Citation IDs must map to real evidence.

Recommended conceptual model:

```text
citation_id
chunk_id
document_id
page
character offsets
```

A message citation maps:

```text
message -> citation -> document chunk -> document/page
```

The frontend should be able to display:

```text
[1] FlashAttention — Page 4
```

and eventually open the source at the relevant location.

## 11. Data model

### users

```text
id PK
email UNIQUE
password_hash
name
created_at
```

### workspaces

```text
id PK
name
owner_id FK
created_at
```

### workspace_members

```text
workspace_id FK
user_id FK
role
```

Roles:
- OWNER
- EDITOR
- VIEWER

### documents

```text
id PK
workspace_id FK
title
filename
mime_type
storage_key
source_type
source_url
status
page_count
created_at
```

Source types:
- UPLOAD
- URL
- ARXIV

### document_chunks

```text
id PK
document_id FK
chunk_index
text
page_start
page_end
section_title
token_count
content_hash
```

Vector data can remain in Qdrant.

### notes

```text
id PK
workspace_id FK
user_id FK
title
content
created_at
updated_at
```

### annotations

```text
id PK
document_id FK
user_id FK
page
start_offset
end_offset
selected_text
comment
```

### conversations

```text
id PK
workspace_id FK
user_id FK
title
created_at
```

### messages

```text
id PK
conversation_id FK
role
content
created_at
```

### citations

```text
id PK
message_id FK
chunk_id FK
page
citation_index
```

### entities

```text
id
workspace_id
name
type
```

### relationships

```text
source_id
target_id
relationship_type
```

## 12. Knowledge graph

Start with PostgreSQL.

Example:

```text
Transformer       CONCEPT
Attention         CONCEPT
FlashAttention    PAPER
BERT              PAPER
GPT               MODEL
```

Relationships:

```text
FlashAttention -> improves -> Attention
FlashAttention -> builds_on -> Transformer
FlashAttention -> related_to -> FlashAttention-2
```

Initially relationships can be manually created. Later use AI-assisted entity/relation extraction followed by validation.

Do not add Neo4j unless scale/requirements justify it.

## 13. Research agent

Add only after basic RAG.

Broad request:

> Explain how efficient attention evolved from the original Transformer to modern approaches.

Potential workflow:

```text
Research request
 -> Planner
 -> Search / Compare / Timeline subtasks
 -> Evidence verification
 -> Report generation
```

Potential roles:
- Planner
- Researcher
- Analyst
- Verifier
- Writer

The agent system must be designed around responsibilities, not hype.

Start with custom orchestration. Evaluate LangGraph later.

## 14. Research reports

Target pipeline:

```text
Question
 -> Plan
 -> Retrieve
 -> Rerank
 -> Extract claims
 -> Verify claims
 -> Build outline
 -> Generate sections
 -> Attach citations
 -> Validate citations
 -> Final report
```

## 15. Citation verification

Potential later pipeline:

```text
claim
 -> retrieve supporting evidence
 -> evaluate support
 -> SUPPORTED / WEAKLY SUPPORTED / UNSUPPORTED
```

This becomes an AI evaluation layer.

## 16. Evaluation

Create a benchmark dataset with questions and expected sources.

Measure retrieval:
- Precision@K
- Recall@K
- MRR
- nDCG

Generation:
- citation correctness
- answer faithfulness
- answer relevance
- completeness

System:
- latency
- token usage
- cost
- failure rate

Do not describe the system as "good" without eventually measuring it.

## 17. API design

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

Comparison:
```text
POST /api/v1/research/compare
```

Reports:
```text
POST /api/v1/research/reports
GET  /api/v1/research/reports/{id}
```

## 18. Production architecture

Target:

```text
Internet
   |
Cloudflare / DNS / CDN
   |
+-------------------------------+
| React Frontend | FastAPI API |
+-------------------------------+
                  |
      +-----------+-----------+
      |           |           |
 PostgreSQL     Redis       Qdrant
                  |
                Celery
                  |
           +------+------+
           |             |
       Ingestion         AI
                           |
                          LLM
```

Object storage holds the source files.

Later add:
- Docker
- CI/CD
- cloud deployment
- logging
- monitoring
- rate limiting
- caching

## 19. What makes ResearchOS different from basic RAG

Basic:

```text
PDF
 -> embedding
 -> vector DB
 -> LLM
 -> chatbot
```

ResearchOS:

```text
Full-stack application
+ Authentication
+ Authorization
+ PostgreSQL
+ Document management
+ Object storage
+ Background processing
+ Semantic retrieval
+ Hybrid retrieval
+ Reranking
+ RAG
+ Citation evidence
+ Notes
+ Relationships
+ Comparisons
+ Reports
+ Research agents
+ Evaluation
+ Production engineering
```

## 20. Explicit non-goals for the beginning

Do not begin with:
- LangChain
- CrewAI
- LangGraph
- Kubernetes
- Terraform
- Kafka
- Neo4j
- many AI models

The first objective is understanding and building the underlying system.

## 21. Final product progression

### First usable
```text
Login
 -> Workspace
 -> Upload PDF
 -> Process PDF
 -> Semantic search
 -> Question
 -> Answer with citations
```

### Serious final
```text
Full-stack SaaS
+ Document ingestion
+ Semantic/hybrid retrieval
+ Reranking
+ Citation-grounded RAG
+ Paper comparison
+ Knowledge graph
+ Research agents
+ Report generation
+ AI evaluation
+ Recommendations
+ Collaboration
+ Background processing
+ Caching
+ Docker
+ CI/CD
+ Cloud deployment
```
