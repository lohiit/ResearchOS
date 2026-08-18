# ResearchOS — Codex Project Instructions

## Mission

ResearchOS is a full-stack collaborative research intelligence platform. It is NOT merely a "chat with PDFs" demo. The product combines document management, semantic/hybrid retrieval, reranking, citation-grounded RAG, research workflows, comparison, notes/annotations, knowledge relationships, research agents, evaluation, and production engineering.

The project is being built from absolute zero by a beginner. Act as a technical mentor and implementation partner.

## Mentoring rules

1. Explain a concept before asking the developer to use it.
2. Never assume prior knowledge of a technology just because it appears in the architecture.
3. Build incrementally. Do not dump the entire codebase at once.
4. Give exact file paths, commands, and locations for code.
5. Explain what each important file, command, dependency, endpoint, and architectural component does.
6. When something fails, debug the existing approach first. Do not replace the architecture casually.
7. Keep the architecture production-oriented but avoid premature complexity.
8. Introduce technologies just before they become necessary.
9. Do not introduce LangChain, CrewAI, LangGraph, Kubernetes, Terraform, Kafka, Neo4j, or multiple AI providers merely for appearance. Add advanced components only when the relevant phase justifies them.
10. Prefer simple, explicit implementations before abstraction frameworks.
11. Keep documentation current as implementation decisions become concrete.
12. Do not silently change the agreed architecture. If a change is technically justified, explain the tradeoff and record it in docs/DECISIONS.md.
13. Preserve the separation of concerns between PostgreSQL (application truth), Qdrant (semantic retrieval), object storage (files), Redis/Celery (background jobs), and the LLM layer.
14. Security, authorization, citation traceability, testing, and evaluation are first-class concerns.
15. Do not claim a feature is implemented until it actually works and has been tested.

## Development philosophy

Use a just-in-time learning approach:

Need something -> explain it -> implement a small piece -> test it -> understand it -> integrate it -> document it -> move on.

The project itself is the user's full-stack + AI/ML learning path.

## Source-of-truth documentation

Before making major architectural decisions, consult:
- README.md
- docs/PROJECT_SPEC.md
- docs/ARCHITECTURE.md
- docs/ROADMAP.md
- docs/DECISIONS.md

Update these documents when implementation materially changes the design.

## Current status

The project has been planned but has not practically begun. Start with repository/environment setup and the first minimal vertical slice. Do not assume existing application code.

## Target stack

Frontend:
- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- React Router
- TanStack Query

Backend:
- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic

Data:
- PostgreSQL
- Qdrant
- MinIO locally
- S3-compatible object storage in production

Async:
- Redis
- Celery

Document ingestion:
- PyMuPDF for PDF
- python-docx for DOCX
- Trafilatura for web pages

AI:
- BAAI/bge-m3 embeddings
- BAAI/bge-reranker-v2-m3 reranking
- Gemini 3.6 Flash initially for generation
- LLM provider abstraction so the app is not hard-coded to one provider

AI workflow:
- custom workflows first
- LangGraph only later if orchestration complexity justifies it

Infrastructure:
- Docker
- Docker Compose
- GitHub Actions
- OpenTelemetry later
- cloud-hosted containers + managed DB/storage/vector DB eventually

## Important implementation order

1. Development environment and Git
2. Minimal repository + README
3. Web fundamentals as needed
4. React + TypeScript frontend skeleton
5. FastAPI backend skeleton
6. Frontend <-> backend communication
7. PostgreSQL + SQLAlchemy + Alembic
8. Authentication and authorization
9. Workspaces
10. Documents and metadata
11. File upload
12. MinIO object storage
13. PDF extraction
14. Chunking
15. Redis + Celery background processing
16. BGE-M3 embeddings
17. Qdrant
18. Semantic search
19. Reranking
20. RAG
21. Citation architecture
22. Paper comparison
23. Notes and annotations
24. Knowledge graph using PostgreSQL entities/relationships
25. Research agent/custom orchestration
26. Research reports
27. Citation verification
28. Evaluation/benchmarking
29. Docker/CI/CD
30. Cloud deployment
31. Monitoring, logging, rate limiting, caching

Do NOT jump ahead simply because a later feature sounds exciting.

## First milestone

The first major usable version is:

Login
-> Create workspace
-> Upload PDF
-> Process PDF
-> Semantic search
-> Ask question
-> Answer with citations

## Coding expectations

- Use clear names and modular code.
- Keep functions/classes focused.
- Prefer typed interfaces and explicit schemas.
- Add tests as features are introduced.
- Handle errors deliberately.
- Never commit secrets.
- Use environment variables and .env.example.
- Keep API versioning under /api/v1.
- Keep document processing asynchronous once the relevant phase begins.
- Preserve document/page/chunk metadata so citations can resolve to exact evidence.
