# AI Job Search Agent — Backend

A backend system for an **AI-powered Job Search and Matching Agent** built up to **Checkpoint - I**.

This backend helps users:

- upload a resume or enter profile details manually,
- extract skills and experience,
- search the web for relevant job openings using **Tavily Search**,
- enrich job results using **Tavily Crawl**,
- structure job data with **Groq LLM**,
- store job embeddings in **ChromaDB**,
- rank and return the most relevant job matches.

---

## Checkpoint - I Scope

This backend currently supports:

- Resume upload and resume text extraction
- Resume profile parsing using Groq
- Manual profile input
- Smart query generation for job search
- Job discovery using Tavily Search
- Job content enrichment using Tavily Crawl
- Job structuring and summarization using Groq
- Embedding generation using Hugging Face
- Semantic storage and retrieval using ChromaDB
- Match scoring based on skills, role, location, and company preferences
- REST APIs using FastAPI

---

## Tech Stack

### Backend Framework

- **FastAPI**

### LLM

- **Groq**
- Model: `llama-3.3-70b-versatile`

### Embeddings

- **Hugging Face**
- Model: `sentence-transformers/all-MiniLM-L6-v2`

### Vector Database

- **ChromaDB**

### Search + Crawl

- **Tavily Search**
- **Tavily Crawl**

### Orchestration

- **LangChain Core**

### File Parsing

- **PyPDF**
- **python-docx**

---

## High-Level Flow

```text
User Resume / Manual Profile
            |
            v
   Resume/Profile Parser
            |
            v
   Search Query Generator
            |
            v
      Tavily Search
            |
            v
      Tavily Crawl
            |
            v
   Groq Job Extraction Layer
            |
            v
   HuggingFace Embeddings
            |
            v
         ChromaDB
            |
            v
   Match Scoring + Ranking
            |
            v
      API Response
```
