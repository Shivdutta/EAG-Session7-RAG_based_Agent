
# 🚀 Chrome RAG Agent – Smart Browsing with AI-Powered Memory 🧠

<p align="center">
  <img src="https://img.shields.io/badge/Type-Chrome_Extension-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Tech- FAISS | FastAPI-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Bonus- RAG | REDIS-red?style=for-the-badge" />
</p>

---

## 🧠 Problem Statement

Build a cutting-edge Chrome extension that transforms your browser into a context-aware, AI-assisted platform using **Retrieval-Augmented Generation (RAG)** and **vector search**.

### 🔧 Core Features

- 🌍 **Auto-Embedding for Public Pages**  
  For each non-confidential website you visit (excluding Gmail, WhatsApp, etc.), extract page content and generate **semantic embeddings** using Gemini Flash model.

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
- 🌍 RAG based search
- 🧠 REDIS for scaling concurrent request.
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

**Purpose**: Send the entire HTML page content of currrent tab to backed for indexing.

**Features**:
- Embedding are generates for entire page

**Files**:
- `manifest.json` – Permissions and config  
- `content.js` – Injected for highlight detection  
- `background.js` – Communication logic

---

## 🔍 Search APIs

### 1. `fastapi_server.py`

**Purpose**: Handles user queries and returns RAG-generated answers.

**Endpoint**:
- `POST /search` – Process user questions via the agent

---

### 2. `fastapi_server_indexer.py`

**Purpose**: Embeds and indexes uploaded documents.

**Endpoint**:
- `POST /add_to_index` – Add new docs to FAISS  vector store

---

### 3. `fastapi_redis_server_indexer.py`

**Purpose**: Works similarly to `fastapi_server_indexer.py` but integrates with **Redis Queue** for scaling the concurrent input request.

**Rationale for Using Redis**:
- 🌐 **Scalability**: This helps handle concurrent requests that come in rapidly due to the user's fast browsing movements across multiple tabs/browsers

**Endpoint**:
- `POST /add_to_index` – Index documents into FAISS via Redis for semantic/tag enabled retrieval

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
GEMINI_API_KEY=your_openai_key
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 5. Install & Run Redis

```bash
# Ubuntu
refer requirements.txt

# Start server
redis-server
```
### 6. Launch FastAPI Server(Indexer)

```bash
uvicorn fastapi_redis_server_indexer:app --reload --log-level debug --port 8001
```

### 7. Launch MCP Server

```bash
python mcp_server.py
```
### 8. Launch Redis job

```bash
rq worker mcp-tasks
```

### 9. Launch FastAPI Server(Search)

```bash
uvicorn fastapi_server:app --reload --log-level debug --port 8000
```

### 10. Load Chrome Extensions

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


## 🧠 Code Architecture Deep Dive

### 📁 `agent.py` – RAG Agent Logic  
This is the **brain** of the system. It defines a class like `RAGAgent` that:  
- Receives user queries  
- Retrieves relevant information using semantic search (e.g., via FAISS or Redis)  
- Integrates retrieved context with the query  
- Uses an LLM (OpenAI or local) to generate a final response  

**Key functions**:  
- `run(query)`: Main method to process user input  
- `retrieve_context(query)`: Finds relevant vector chunks  
- `generate_response(context, query)`: Creates a contextual answer using the LLM  

---

### 📁 `memory.py` – Conversation Memory Management  
Handles session persistence and continuity.  
- Tracks previous interactions  
- Uses  in-memory storage  
- Critical for multi-turn chat context  

**Key features**:  
- `MemoryBuffer` or `SessionManager` classes  
- Enables context carry-over and temporal awareness  

---

### 📁 `perception.py` – Input Understanding & Preprocessing  
Prepares user input before retrieval or generation.  
- May extract key phrases or topics  

**Impact**: Improves semantic search accuracy and LLM relevance  

---

### 📁 `decision.py` – Agent Planning & Reasoning  
Acts as the agent's **planner**:  
- Determines whether to clarify, search, or answer  
- Can rank retrieved content or defer decisions  

**Example behaviors**:  
- Follows up on ambiguous queries  
- Weighs conflicting context sources  

---

### 📁 `action.py` – Execution Layer  
- Executes commands based on agent decisions  

**Possible actions**:  
- Save or pin relevant info  

---

### 📁 `mcp_tools.py` – Multi-Component Processing Utilities  
A shared utility layer that supports all modules.  

**Key utilities**:  
- `split_into_chunks(text, max_tokens)`  
- `count_tokens(text)`  
- `sanitize_input(raw_html)`  

Forms the backbone of processes like `Perceive → Chunk → Embed → Store`  

---

### 🛠️ MCP Tools – Modular Commands for Document Intelligence  

#### 🔍 `@mcp.tool()` – Exposed Utilities  

```python
search_documents(query: str) -> list[str]
```
- Embeds the query using a vector model
- Searches the FAISS index for top 5 similar chunks
- Retrieves context snippets with associated metadata (doc name, URL, chunk ID)
- Generates a context-aware answer using Gemini LLM
- Returns the result in strict format:   FINAL_ANSWER: ["<summary answer>", "<source URL>"]

---

```python
process_documents()
```

- Ingests and embeds local files  
- Converts Markdown, PDF, HTML  
- Skips unchanged files via hashing  
- Outputs to `index.bin` + `metadata.json`  

---

```python
process_html(url: str, title: str, text: str = "")
```

- Adds browser content on-the-fly  
- Chunks and embeds web text  
- Avoids reprocessing via hash deduplication  


## 📎 References

- [Nomic Embeddings](https://docs.nomic.ai)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Redis](https://redis.io/)
- [FastAPI](https://fastapi.tiangolo.com/)

---
