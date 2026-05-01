# 🚀 AI Job Search Agent (Production-Optimized)

A **production-grade AI-powered job discovery and application intelligence system** that combines:

* 🔍 Smart Job Search (Checkpoint I)
* 🧠 Resume Intelligence & Market Analysis (Checkpoint II)
* 🎯 Job-Specific Resume Matching (Checkpoint III)

Built using **FastAPI + LangChain Core (LCEL) + Groq LLM + Tavily + HuggingFace + React (Vite)** with **deployment-ready optimizations for low latency, low RPM, and high reliability**.

---

# 🧠 Core Philosophy

This system follows a **two-phase intelligence architecture**:

```text
Broad Search (Fast, Cheap)
        ↓
Deep Analysis (Selective, Expensive)
```

👉 This ensures:

* ⚡ Fast responses
* 📉 Low API cost (RPM/TPM optimized)
* 🚫 No timeouts on cloud platforms (Render)
* 🎯 High-quality results only when needed

---

# 📌 Features by Checkpoint

## ✅ Checkpoint I – AI Job Search

### Input:

* Resume OR manual skills
* Role
* Location
* Optional filters (package, companies)

### Process:

* Extract user profile
* Generate 2 search queries
* Tavily Search (no crawling)
* LLM extracts job details

### Output:

* Job list (max 6)
* Match score
* Missing skills
* Apply link

---

## ✅ Checkpoint II – Resume Analysis

### Input:

* Resume

### Process:

* Resume parsing (LLM)
* Market requirement search (no crawling)
* Learning resources search
* Gap analysis using Groq

### Output:

* Resume score
* Missing skills
* Market expectations
* Learning resources
* Improvement suggestions

---

## ✅ Checkpoint III – Job-Specific Matching

### Input:

* Selected job
* Resume

### Process:

* Crawl only selected job
* Extract full JD
* Compare resume vs JD
* Generate fit score

### Output:

* 🎯 Job Fit Score
* ✅ Strengths
* ❌ Missing skills
* 📊 Recommendation (Apply / Improve)

---

# 🏗️ Architecture

```text
┌───────────────────────────────┐
│   React + Vite Frontend      │
└───────────────┬──────────────┘
                │ API Calls
┌───────────────▼──────────────┐
│       FastAPI Backend        │
│                              │
│  ┌────────────────────────┐  │
│  │ Profile Extraction     │  │
│  │ Job Search Service     │  │
│  │ Analysis Service       │  │
│  │ Job Match Service      │  │
│  └────────────────────────┘  │
│            │                 │
│   ┌────────▼────────┐        │
│   │ LangChain LCEL  │        │
│   └────────┬────────┘        │
│            │                 │
│   ┌────────▼────────┐        │
│   │ Groq LLM        │        │
│   └────────┬────────┘        │
│            │                 │
│   ┌────────▼────────┐        │
│   │ Tavily Search   │        │
│   │ Tavily Crawl    │        │
│   └─────────────────┘        │
└──────────────────────────────┘
```

---

# ⚙️ Optimization Strategy (Key Highlight)

## ❌ Before (Problematic)

```text
Search → Crawl multiple jobs → LLM → Store → Return
```

Issues:

* High RPM (Tavily)
* High TPM (Groq)
* Timeouts (Render)
* Slow response

---

## ✅ Now (Optimized)

```text
Search (lightweight) → Return jobs
        ↓
User selects job → Crawl only that job → Deep analysis
```

### Benefits:

* 🚀 Faster response
* 📉 Reduced API calls
* 💰 Lower cost
* ⚡ No timeouts

---

# 🔁 Request Flow

## 1️⃣ Job Search Flow

```text
User Input → Profile Service
        ↓
Query Builder
        ↓
Tavily Search (2 queries only)
        ↓
Job Extraction (LLM)
        ↓
Match Score
        ↓
Return Jobs
```

🚫 No crawling here

---

## 2️⃣ Resume Analysis Flow

```text
Resume → Profile Extraction
        ↓
Market Research (Tavily search only)
        ↓
Learning Resources Search
        ↓
LLM Analysis
        ↓
Return insights
```

🚫 No crawling here

---

## 3️⃣ Job Match Flow

```text
User selects job
        ↓
Crawl ONLY that job (force=True)
        ↓
Extract JD
        ↓
Compare with resume
        ↓
Return fit score
```

✅ Crawling happens ONLY here

---

# 📁 Code Structure Explained

## Backend (`AI Job Search Agent - API`)

### 🔹 `app/main.py`

* FastAPI entry point
* Router registration
* CORS configuration

---

### 🔹 `config.py`

Controls:

* API limits
* crawling flags
* token limits

Example:

```python
enable_job_crawling = False
max_tavily_queries = 2
llm_max_tokens = 900
```

---

### 🔹 `profile_service.py`

* Extracts structured profile from resume
* Uses Groq LLM

---

### 🔹 `job_search_service.py`

* Builds search queries
* Calls Tavily search
* Extracts jobs using LLM
* Computes match score

---

### 🔹 `tavily_service.py`

Handles:

* Tavily search
* Tavily crawl
* Domain blocking (LinkedIn, etc.)

---

### 🔹 `market_research_service.py`

* Finds market expectations
* Uses search only (no crawl)

---

### 🔹 `learning_resource_service.py`

* Finds GitHub/docs resources
* No crawling

---

### 🔹 `job_detail_service.py`

* Crawls selected job ONLY
* Extracts full JD

---

### 🔹 `job_fit_service.py`

* Compares resume vs JD
* Generates final recommendation

---

# 📊 Configuration Controls

## Environment Variables

```env
MAX_SEARCH_RESULTS=6
MAX_TAVILY_QUERIES=2
ENABLE_JOB_CRAWLING=false
MAX_CRAWL_PAGES=1
MAX_CONTENT_CHARS=6000
LLM_MAX_TOKENS=900
ENABLE_CHROMA_WRITES=false
```

## What they control

| Variable            | Purpose                |
| ------------------- | ---------------------- |
| MAX_TAVILY_QUERIES  | Limits API calls       |
| ENABLE_JOB_CRAWLING | Prevents bulk crawling |
| MAX_CONTENT_CHARS   | Controls token usage   |
| LLM_MAX_TOKENS      | Controls response size |

---

# ⚡ Best Practices Followed

## 1. Controlled Crawling

* Crawl only when necessary
* Avoid heavy domains (LinkedIn, Medium)

## 2. Token Optimization

* Truncate large text
* Limit LLM output tokens

## 3. API Rate Optimization

* Limit Tavily queries
* Deduplicate results

## 4. Fail-safe Design

* fallback job builder
* safe JSON parsing
* retry logic

## 5. Modular Architecture

* Service-based structure
* Clean separation of concerns

## 6. Production Awareness

* Designed for Render limitations
* Handles timeouts and memory limits

---

# 🌐 Deployment

## Backend (Render)

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Frontend (Render)

```bash
npm install && npm run build
```

---

# 🚀 Future Enhancements

* Auto Apply Assistant
* Job Tracker Dashboard
* Resume Rewriter (JD-based)
* Chrome Extension
* Async processing (Celery)

---

# 👨‍💻 Author

**Rohith Ganesh**

* Systems Engineer
* Focus: GenAI, RAG, Agentic Systems

---

# ⭐ Final Note

This project is not just a demo.

It demonstrates:

* **Real-world AI system design**
* **Production optimization thinking**
* **Agentic workflow architecture**

---

If you found this useful, ⭐ the repo!
