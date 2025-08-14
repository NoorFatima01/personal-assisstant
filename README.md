# 🗓️ Week Plan Chat
*A LangChain + RAG-based web app to chat with your weekly goals.*

## 📌 Overview
**Week Plan Chat** is an AI-powered weekly planner that allows users to upload their weekly goal PDFs categorized as **Work**, **Personal**, and **Health**. Users can interact with them using natural language queries.  
The app uses **LangChain** and **RAG (Retrieval-Augmented Generation)** to fetch relevant context from uploaded documents and answer questions conversationally.

**Key Features:**
- 📂 Upload **4 weekly schedule PDFs** (Work Goals, Personal Goals, Health Goals).
- 💬 Chat with an **LLM** about your goals and schedules.
- 🔍 **Filtered Vector search** with (based on week and question type) **Qdrant** for relevant context retrieval.
- ⚡ Real-time answers via **Server-Sent Events (SSE)** streaming.
- 🛠️ **Background jobs** with **Celery** for heavy tasks.
- ⏰ **Cron jobs** (Celery Beat) for scheduled tasks.
- 🏗️ **OOP-based FastAPI architecture** for cleaner, modular, and maintainable backend code.
---

## 🛠️ Tech Stack

**Frontend:**
- React.js
- TailwindCSS
- Zod + React Hook Form (form validation)

**Backend:**
- FastAPI
- LangChain
- Qdrant Vector Database
- Supabase (auth + storage + database)
- Redis (caching + Celery broker)

**Background & Scheduled Jobs:**
- Celery (background processing)
- Celery Beat (cron jobs)

**Other:**
- Server-Sent Events (SSE) for streaming responses

---

## 🚀 How It Works
1. **Upload PDFs** – Users upload weekly goal PDFs for Work, Personal, and Health.
2. **Process & Store** – Documents are chunked, embedded, and stored in **Qdrant** for retrieval.
3. **Ask Questions** – Users type questions like:  
   > "What are my Monday work deadlines?"
4. **Get AI Answers** – The app retrieves relevant chunks and generates an LLM response in real time.

---

## ⚡ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/weekwise.git
cd week-plan-chat

# Backend setup
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --reload-dir app

#running celery
celery -A app.config.celery_app.celery_app worker --beat --loglevel=info

# Frontend setup
cd frontend
npm install
npm run dev
```
---

## 📅 Background & Cron Jobs
**Background Jobs**: Heavy document processing (chunking, embedding) is offloaded to Celery workers.
**Cron Jobs**: Periodic tasks (e.g., sending weekly summaries or reminders) run on schedule via Celery Beat.

---

## 🖥️ Windows Redis Setup (via Docker)
If you are running this project on **Windows**, it’s recommended to run Redis inside Docker instead of installing it manually.

**Steps:**
1. Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
2. Open a terminal (PowerShell or Command Prompt) and run:

```bash
# Pull the latest Redis image
docker pull redis

# Run Redis container
docker run --name redis-server -p 6379:6379 -d redis

# Stop Redis container
docker stop redis-server

# Start Redis container again
docker start redis-server
```

--- 
## 📈 Improvements
1. Put a limit on number of messages in a single chat.
2. Use langchain-qdrant package instead of qdrant package for better integration.

