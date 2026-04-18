# 🏢 HR Policy Bot

An **Agentic AI** system that answers HR policy questions using Retrieval-Augmented Generation (RAG), with web search fallback, multi-turn memory, and faithfulness evaluation.

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────┐
│   Memory    │  ← Injects conversation history
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Router    │  ← Classifies: RAG / Web / Chitchat
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
[RAG]   [Web Search]   [Chitchat]
ChromaDB  DuckDuckGo    Direct LLM
   │       │               │
   └───────┴───────────────┘
                │
                ▼
        ┌─────────────┐
        │   Answer    │  ← Groq llama-3.3-70b
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │    Eval     │  ← Faithfulness scoring
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │    Save     │  ← Update message history
        └─────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Workflow | LangGraph |
| LLM | Groq `llama-3.3-70b-versatile` |
| Vector Store | ChromaDB |
| Embeddings | SentenceTransformers (`all-MiniLM-L6-v2`) |
| Web Search | DuckDuckGo Search (ddgs) |
| UI | Streamlit |
| Evaluation | Custom Faithfulness Scoring |

---

## 📁 Project Structure

```
hr-policy-bot/
│
├── agent.py                 # LangGraph agentic workflow
├── capstone_streamlit.py    # Streamlit chat UI
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── README.md                # This file
│
├── documents/
│   └── hr_policy.txt        # HR policy document (10 sections)
│
└── utils/
    └── helpers.py           # Shared utilities and helpers
```

---

## ⚙️ Setup Instructions

### 1. Clone / Download the Project

```bash
git clone <your-repo-url>
cd hr-policy-bot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

Get a free Groq API key at: **https://console.groq.com/**

---

## 🚀 How to Run

```bash
streamlit run capstone_streamlit.py
```

The app opens at **http://localhost:8501**

---

## 💡 Sample Queries to Try

### HR Policy Questions (RAG-based)
```
How many days of annual leave am I entitled to?
What is the salary disbursement date?
What is the notice period for resignation?
How do I apply for WFH?
What documents do I need for expense reimbursement?
How is the performance appraisal rating calculated?
What is the probation period for new joiners?
Can I carry forward unused leave to next year?
How do I file a grievance or complaint?
What is the maternity leave policy?
```

### General Questions (Web Search)
```
What is the current inflation rate in India?
Who is the CEO of Infosys?
What are the latest labor laws in India?
```

### Chitchat
```
Hello, who are you?
What can you help me with?
```

---

## 🔍 Features

| Feature | Details |
|---------|---------|
| **RAG** | Answers from ChromaDB vector store with cosine similarity |
| **Anti-Hallucination** | Strict grounding; returns "I don't know" if not in docs |
| **Web Search** | DuckDuckGo fallback for non-HR queries |
| **Multi-turn Memory** | Full conversation history passed to each turn |
| **Faithfulness Score** | Per-response score (0–100%) shown in UI |
| **Route Display** | Each answer shows whether it came from RAG, Web, or Chat |

---

## 📊 Faithfulness Score Interpretation

| Score | Label | Meaning |
|-------|-------|---------|
| 75%–100% | ✅ High | Answer fully grounded in policy docs |
| 45%–74% | ⚠️ Moderate | Partially grounded; verify key details |
| 0%–44% | ❌ Low | Low grounding; confirm directly with HR |

---

## 🔧 Customization

### Add Your Own Policies
Edit `documents/hr_policy.txt` and restart the app. ChromaDB will automatically re-index.

### Change the Company Name / HR Contact
Use the sidebar inputs in the Streamlit UI — no code changes needed.

### Use a Different Embedding Model
In `agent.py`, change:
```python
EMBED_MODEL = "all-MiniLM-L6-v2"
```
to any HuggingFace SentenceTransformer model.

---

## 📝 Notes

- ChromaDB uses **in-memory** storage by default. Data is re-indexed on each restart.
- The LangGraph graph is **cached** in Streamlit session for performance.
- Faithfulness scoring uses a **lexical overlap heuristic** — no external API needed.
- All conversations remain **local** — nothing is sent except to the Groq API for generation.

---

## 📄 License

MIT License — Free for personal and commercial use.
