# ResearchOS — Architecture Decision Log

This file records deliberate architectural decisions. Add entries when implementation changes the agreed plan.

## ADR-001 — PostgreSQL + Qdrant

**Decision:** Use PostgreSQL as the application system of record and Qdrant as the semantic retrieval engine.

**Reason:** They solve different problems. PostgreSQL stores transactional relational state; Qdrant performs vector retrieval and filtering.

---

## ADR-002 — Object storage for original documents

**Decision:** Store PDFs and other original files in S3-compatible object storage rather than PostgreSQL.

**Local:** MinIO.

**Production:** S3-compatible service such as Cloudflare R2 or AWS S3.

---

## ADR-003 — Background document processing

**Decision:** Process uploaded documents asynchronously using Redis + Celery.

**Reason:** PDF extraction, chunking, embeddings, and indexing can be expensive and should not block API requests.

---

## ADR-004 — Local embeddings/reranking

**Decision:** Use BAAI/bge-m3 for embeddings and BAAI/bge-reranker-v2-m3 for reranking rather than calling a hosted embedding/reranking API by default.

**Reason:** The project should contain genuine retrieval/ML components and avoid unnecessary API dependence.

---

## ADR-005 — LLM provider abstraction

**Decision:** Hide the generation model behind an application interface.

**Initial provider:** Gemini 3.6 Flash.

**Reason:** Prevent vendor lock-in and make later provider/local-model changes manageable.

---

## ADR-006 — No agent framework at the beginning

**Decision:** Implement basic workflows manually before adopting LangGraph or another orchestration framework.

**Reason:** The developer should understand the workflow mechanics first, and frameworks should solve demonstrated complexity rather than add abstraction prematurely.

---

## ADR-007 — PostgreSQL for initial graph

**Decision:** Store entities and relationships in PostgreSQL initially.

**Reason:** Avoid adding Neo4j before graph scale/requirements justify a dedicated graph database.

---

## ADR-008 — Hybrid retrieval later

**Decision:** Start with dense semantic retrieval, then add lexical/BM25 hybrid retrieval and fusion later.

**Reason:** Reduce initial complexity and establish a measurable baseline before optimization.

---

## ADR-009 — Incremental repository structure

**Decision:** Do not create every final folder/service on day one.

**Reason:** The architecture should grow with real requirements, while keeping the beginner's working context manageable.

---

## ADR-010 — Evidence-first RAG

**Decision:** Treat retrieved source evidence as the basis for factual answers and make citation mapping a backend responsibility.

**Reason:** ResearchOS must be distinguishable from an ordinary chatbot and should make claims traceable to documents.
