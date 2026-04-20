# HR Policy Bot — Agentic AI Capstone 2026

A fully working multi-turn HR Policy assistant built with **LangGraph**, **ChromaDB RAG**, **Groq LLM**, and **Streamlit**.

---

## Project Structure

```
hr_policy_bot/
├── agent/
│   ├── __init__.py
│   ├── knowledge_base.py   # 10 HR policy documents
│   ├── state.py            # CapstoneState TypedDict
│   ├── nodes.py            # All 8 LangGraph node functions
│   └── graph.py            # Graph assembly, LLM/ChromaDB setup
├── ui/
│   ├── __init__.py
│   └── app.py              # Streamlit web UI
├── tests/
│   ├── __init__.py
│   ├── test_agent.py       # 13 test questions + summary table
│   └── ragas_eval.py       # RAGAS baseline evaluation
├── main.py                 # Terminal chat interface
├── requirements.txt
├── .env                    # Your API key goes here
└── README.md
```

---

## Setup — Step by Step

### 1. Clone / open in VS Code
Open the `hr_policy_bot/` folder in VS Code.

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key
Open the `.env` file and replace the placeholder:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```
Get your free key at: https://console.groq.com

---

## How to Run

### Option A — Streamlit Web UI (recommended)
```bash
streamlit run ui/app.py
```
Opens in browser at http://localhost:8501

### Option B — Terminal Chat
```bash
python main.py
```

### Option C — Run All Tests
```bash
python tests/test_agent.py
```

### Option D — RAGAS Evaluation
```bash
python tests/ragas_eval.py
```

---

## Architecture

```
User question
     ↓
[memory_node]    → slide window, extract name, reset retries
     ↓
[router_node]    → LLM decides: retrieve / tool / memory_only
     ↓
[retrieval_node] → embed question → ChromaDB top-3 chunks
[skip_node]      → clear context (tool/memory route)
[tool_node]      → datetime tool (current date/time)
     ↓
[answer_node]    → system prompt + context + history → LLM answer
     ↓
[eval_node]      → faithfulness score (0.0–1.0) → retry if < 0.7
     ↓
[save_node]      → append answer to messages → END
```

---

## Six Mandatory Capabilities

| # | Capability | Where |
|---|-----------|-------|
| 1 | LangGraph StateGraph (8 nodes) | agent/graph.py |
| 2 | ChromaDB RAG (10 documents) | agent/knowledge_base.py, agent/nodes.py |
| 3 | MemorySaver + thread_id | agent/graph.py |
| 4 | Self-reflection eval node | agent/nodes.py → eval_node |
| 5 | Tool use (datetime) | agent/nodes.py → tool_node |
| 6 | Streamlit deployment | ui/app.py |

---

## Submission Checklist

- [ ] All cells run without error (Kernel > Restart & Run All)
- [ ] ZIP file with all project files
- [ ] GitHub repository (public)
- [ ] PDF Documentation (4–5 pages, Arial, A4)
- [ ] Name, Roll Number, Batch on title page
- [ ] RAGAS scores recorded in written summary
- [ ] Test results table filled in
- [ ] Deadline: April 21, 2026 | 11:59 PM

---

*Dr. Kanthi Kiran Sirra | Sr. AI Engineer | Agentic AI Course 2026*
