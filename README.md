# 🚀 AI Job Search Agent

An **AI-powered job search and resume intelligence platform** that helps users:

* 🔍 Discover relevant jobs (Checkpoint I)
* 🧠 Analyze their resume against market expectations (Checkpoint II)
* 🎯 Match their resume to a specific job and get a fit score (Checkpoint III)

Built using **FastAPI + LangChain + Groq + Tavily + React (Vite)**.

---

## 📌 Features Overview

### ✅ Checkpoint I – AI Job Search

* Upload resume OR manually enter skills
* Fetch relevant jobs using **Tavily Search**
* Extract:

  * Job title, company, location
  * Required skills
  * Match score
* Display:

  * Match reasons
  * Missing skills

---

### ✅ Checkpoint II – Resume Analysis

* Upload resume
* AI analyzes:

  * Skills vs market expectations
  * Tools/framework gaps
  * ATS keyword coverage
* Outputs:

  * Resume scores
  * Gap analysis
  * Resume improvement suggestions
  * Learning resources

---

### ✅ Checkpoint III – Job-Specific Resume Match

* Click **"Analyze Resume for This Job"**
* Upload resume
* System:

  * Fetches full Job Description (Tavily Crawl)
  * Compares resume vs job
* Outputs:

  * 🎯 Job Fit Score
  * ✅ Strengths
  * ❌ Missing Skills
  * 🛠 Resume Improvements
  * 📊 Recommendation (Apply / Improve)

---

## 🏗️ Architecture

```text
Frontend (React + Vite)
        ↓
FastAPI Backend
        ↓
LangChain Core (Agents + Pipelines)
        ↓
Groq LLM (Llama 3.3 70B)
        ↓
Tavily Search + Tavily Crawl
        ↓
HuggingFace Embeddings + ChromaDB
```

---

## 🛠 Tech Stack

### Backend

* FastAPI
* LangChain Core
* Groq (LLM)
* Tavily (Search + Crawl)
* HuggingFace Embeddings
* ChromaDB

### Frontend

* React (Vite)
* Modern UI with modular components

---

## 📁 Project Structure

```text
AI Job Search Agent
│
├── AI Job Search Agent - API      # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── core/
│   │   └── utils/
│
├── AI Job Search Agent - UI       # React Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── api/
│   │   └── styles/
│
└── .gitignore
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Job-Search-Agent.git
cd AI-Job-Search-Agent
```

---

## 🧠 Backend Setup

```bash
cd "AI Job Search Agent - API"

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### Create `.env`

```env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key

LLM_MODEL_NAME=llama-3.3-70b-versatile
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```

### Run Backend

```bash
python run.py
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🎨 Frontend Setup

```bash
cd "AI Job Search Agent - UI"

npm install
npm run dev
```

Open:

```
http://localhost:5173
```

---

## 🌐 Deployment (Render)

### Backend (Web Service)

* Root Directory: `AI Job Search Agent - API`
* Build:

```bash
pip install -r requirements.txt
```

* Start:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

### Frontend (Static Site)

* Root Directory: `AI Job Search Agent - UI`
* Build:

```bash
npm install && npm run build
```

* Publish:

```
dist
```

---

### Environment Variables

#### Backend

```env
GROQ_API_KEY=...
TAVILY_API_KEY=...
ALLOWED_ORIGINS=https://your-frontend-url
```

#### Frontend

```env
VITE_API_BASE_URL=https://your-backend-url/api/v1
```

---

## 🚨 Known Deployment Optimizations

To avoid timeouts on Render:

```env
TAVILY_MAX_RESULTS=3
MAX_CRAWL_URLS=1
MAX_ANALYSIS_MARKET_RESULTS=2
MAX_RESOURCE_RESULTS=2
```

Also:

* Skip LinkedIn crawling
* Avoid heavy Chroma writes in production

---

## 📊 Example Flow

### Job Search

```text
Resume → Skills → Tavily → Jobs → Match Score
```

### Resume Analysis

```text
Resume → AI → Market Comparison → Suggestions
```

### Job Match

```text
Job Click → JD Fetch → Resume Upload → Fit Score
```

---

## 📈 Future Improvements

* Async job processing (Celery / queue)
* Streaming responses
* Resume ranking across multiple jobs
* User authentication
* Saved job dashboards

---

## 🤝 Contributing

Feel free to fork, improve, and raise PRs 🚀

---

## 📜 License

MIT License

---

## 💡 Author

**Rohith Ganesh Adigopula**

* Backend Engineer | AI Systems | Cloud
* Focus: GenAI, RAG, Agentic Systems

---

⭐ If you found this useful, consider starring the repo!
