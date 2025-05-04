
# 🚀 Chrome RAG Agent – Smart Browsing with AI-Powered Memory 🧠

<p align="center">
  <img src="https://img.shields.io/badge/Type-Chrome_Extension-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Tech-RAG | FAISS | Redis | FastAPI-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Bonus-In_Browser_RAG-red?style=for-the-badge" />
</p>

---

## 🧠 Problem Statement

Build a cutting-edge Chrome extension that transforms your browser into a context-aware, AI-assisted platform using **Retrieval-Augmented Generation (RAG)** and **vector search**.

### 🔧 Core Features

- 🌍 **Auto-Embedding for Public Pages**  
  For each non-confidential website you visit (excluding Gmail, WhatsApp, etc.), extract page content and generate **semantic embeddings** using [Nomic Embeddings](https://docs.nomic.ai) or a local model.

- 📦 **Efficient Indexing**  
  Store each embedding with its source URL in a **FAISS index**. You can generate this index locally or via **Google Colab**, and then download the index file for use.

- 🔍 **Semantic Search + Navigation**  
  Add a search bar in your extension that:
  - Accepts natural language queries.
  - Finds relevant URLs via FAISS index.
  - Opens the page and highlights the matched content.

### 💡 Bonus Challenge

Surprise us with something creative and powerful using local or browser-native RAG:
- 🔄 On-page summarization  
- 🧠 LLM-powered memory  
- ⚡ WebAssembly-based agents  
Be fast, private, and smart.

---

## 🧩 Chrome Extensions

### 1. Chrome_Extension_Session7

**Purpose**: Interacts with the backend RAG agent from within Chrome.

**Features**:
- Sends user queries to FastAPI backend.
- Displays responses in a popup.

**Files**:
- `manifest.json` – Extension metadata  
- `popup.html` – Interface layout  
- `popup.js` – Sends/receives data from backend

---

### 2. Chrome_Extension_Session7_Search

**Purpose**: Enables semantic search based on user-highlighted content.

**Features**:
- Captures highlighted text.
- Queries the backend and shows context-aware answers.

**Files**:
- `manifest.json` – Permissions and config  
- `content.js` – Injected for highlight detection  
- `background.js` – Communication logic

---

## 🔍 Search APIs

### 1. `fastapi_server.py`

**Purpose**: Handles user queries and returns RAG-generated answers.

**Endpoint**:
- `POST /query` – Process user questions via the agent

---

### 2. `fastapi_server_indexer.py`

**Purpose**: Embeds and indexes uploaded documents.

**Endpoint**:
- `POST /index` – Add new docs to FAISS or Redis vector store

---

### 3. `fastapi_redis_server_indexer.py`

**Purpose**: Works similarly to `fastapi_server_indexer.py` but integrates with **Redis** for high-speed, scalable vector storage.

**Rationale for Using Redis**:
- 🧠 **Memory & Speed**: Redis (via `redis-py` and `redis-vector`) supports **low-latency semantic search** and can store large vector datasets in-memory.
- 🌐 **Scalability**: Ideal for real-time RAG systems where speed matters.
- 🔌 **Persistence**: Redis supports optional on-disk persistence and recovery unlike in-memory-only systems.

**Endpoint**:
- `POST /redis_index` – Index documents into Redis for semantic retrieval

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Shivdutta/EAG-Session7-RAG_based_Agent.git
cd EAG-Session7-RAG_based_Agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scriptsctivate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 5. Install & Run Redis

```bash
# macOS
brew install redis

# Ubuntu
sudo apt-get install redis-server

# Start server
redis-server
```

### 6. Launch FastAPI Server

```bash
uvicorn fastapi_server:app --reload
```

### 7. Load Chrome Extensions

1. Go to `chrome://extensions/`
2. Enable **Developer mode**
3. Click **Load unpacked** and choose:
   - `Chrome_Extension_Session7` or  
   - `Chrome_Extension_Session7_Search`

---

## 🧠 Additional Components

- `agent.py` – Defines the RAG agent logic  
- `embedding.py` – Handles OpenAI/Nomic embedding generation  
- `memory.py` – Manages conversation/session memory  
- `redis_jobs.py` – Redis vector database helpers

---

## 📎 References

- [Nomic Embeddings](https://docs.nomic.ai)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Redis](https://redis.io/)
- [FastAPI](https://fastapi.tiangolo.com/)

---
