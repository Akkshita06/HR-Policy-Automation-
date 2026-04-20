# HR Policy Bot — GitHub Project Documentation

> **Agentic AI Capstone 2026**  
> LangGraph · ChromaDB · Groq LLaMA-3.3-70B · Streamlit  

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Solution Design](#3-solution-design)
4. [Codebase Walkthrough](#4-codebase-walkthrough)
5. [LangGraph State Machine](#5-langgraph-state-machine)
6. [RAG Pipeline Deep Dive](#6-rag-pipeline-deep-dive)
7. [Self-Reflection & Eval Loop](#7-self-reflection--eval-loop)
8. [Streamlit UI](#8-streamlit-ui)
9. [Testing & Evaluation](#9-testing--evaluation)
10. [Setup & Deployment](#10-setup--deployment)
11. [Design Decisions & Trade-offs](#11-design-decisions--trade-offs)
12. [Future Improvements](#12-future-improvements)

---

## 1. Project Overview

**HR Policy Bot** is a production-grade, multi-turn conversational AI assistant that helps employees query company HR policies accurately and instantly. It combines a **LangGraph agentic workflow** with **ChromaDB vector retrieval**, a **Groq-hosted LLaMA-3.3-70B** language model, and a built-in **faithfulness evaluation loop** — ensuring every answer is grounded in the policy knowledge base and never hallucinated.

The system is deployed via a **Streamlit** web interface with a custom dark-themed chat UI, and is also runnable as a terminal application.

### Key Numbers at a Glance

| Metric | Value |
|---|---|
| LangGraph Nodes | 8 |
| HR Policy Documents | 10 |
| ChromaDB Retrieval | Top-3 chunks per query |
| Faithfulness Threshold | 0.70 |
| Max Auto-Retries | 2 |
| Conversation Memory Window | Last 6 messages |
| Test Questions | 13 |

---

## 2. Problem Statement

Most companies maintain HR policies in static documents — PDFs, intranet pages, or email threads — that employees rarely read or can't easily search. This leads to:

- **Repeated queries to HR teams** for basic policy questions (leave balances, WFH eligibility, payroll dates)
- **Misinformation** when employees rely on colleagues rather than official policy
- **No audit trail** or consistency in the answers given
- **Delayed responses** outside business hours

Existing chatbot solutions either hallucinate policy details or fail to maintain conversational context across a multi-turn dialogue.

### Requirements This Project Addresses

| Requirement | Description |
|---|---|
| Accuracy | Answers must be grounded strictly in policy documents |
| Context | Must remember employee's name and previous questions |
| Tool Use | Must handle real-time queries (current date, leave calculation) |
| Transparency | Must cite the policy source for every answer |
| Reliability | Must self-evaluate and retry if answer quality is low |

---

## 3. Solution Design

### High-Level Architecture

```
Employee Question
       │
       ▼
  ┌──────────┐     Sliding window     ┌──────────────┐
  │  Memory  │────(last 6 messages)──▶│    Router    │
  │   Node   │     + name extract     │     Node     │
  └──────────┘                        └──────┬───────┘
                                             │
                          ┌──────────────────┼──────────────────┐
                          ▼                  ▼                  ▼
                    [retrieve]           [tool]            [memory_only]
                          │                  │                  │
                    ChromaDB             datetime            skip ctx
                    top-3 chunks         tool_result         cleared
                          │                  │                  │
                          └──────────────────┼──────────────────┘
                                             ▼
                                      ┌────────────┐
                                      │   Answer   │
                                      │    Node    │
                                      └─────┬──────┘
                                            │
                                      ┌─────▼──────┐
                                      │  Eval Node │
                                      │ (0.0–1.0)  │
                                      └─────┬──────┘
                                            │
                               score < 0.7 AND retries < 2?
                                    Yes ◀───┘───▶ No
                                     │              │
                               retry answer    ┌────▼─────┐
                                               │   Save   │
                                               │   Node   │
                                               └──────────┘
```

### Routing Logic

The router node classifies every question into one of three paths:

| Route | Trigger | Action |
|---|---|---|
| `retrieve` | HR policy question | Embed query → ChromaDB → LLM answer with context |
| `tool` | Date/time query | Run datetime tool → LLM answer with tool result |
| `memory_only` | Greeting / already answered | Skip retrieval, answer from history |

---

## 4. Codebase Walkthrough

### `agent/state.py` — Shared State

The `CapstoneState` TypedDict is the single source of truth passed between all graph nodes:

```python
class CapstoneState(TypedDict):
    question:     str         # Current question
    messages:     List[dict]  # Conversation history (sliding window of 6)
    route:        str         # Router decision
    retrieved:    str         # ChromaDB context string
    sources:      List[str]   # Policy topic names from retrieval
    tool_result:  str         # Datetime tool output
    answer:       str         # Final LLM answer
    faithfulness: float       # Eval score (0.0–1.0)
    eval_retries: int         # Retry counter
    user_name:    str         # Extracted employee name
```

Every node receives this state and returns a partial dict of updates — LangGraph merges them automatically.

### `agent/knowledge_base.py` — Policy Documents

10 HR policy documents, each 100–500 words, covering:
Annual Leave, Sick Leave, WFH, Payroll, Maternity/Paternity, Performance Review, Code of Conduct, Travel & Expense, Employee Benefits, and Resignation & Exit Policy.

Each document follows the format:
```python
{
    "id": "doc_001",
    "topic": "Annual Leave Policy",
    "text": "..."  # ~200 words of policy detail
}
```

### `agent/graph.py` — Graph Assembly

`setup_resources()` initialises:
1. `ChatGroq` with `llama-3.3-70b-versatile` (temperature=0 for determinism)
2. `SentenceTransformer("all-MiniLM-L6-v2")` for embeddings
3. `chromadb.Client()` with all 10 documents pre-embedded and loaded

`build_graph()` assembles the StateGraph, wires all 8 nodes, adds conditional edges for routing and eval decisions, and compiles with `MemorySaver` for persistent memory across turns.

---

## 5. LangGraph State Machine

### Node Details

#### Node 1: `memory_node`
- Appends current question to message history
- Applies sliding window: keeps only the last 6 messages
- Extracts employee name from phrases like "my name is ..."
- Resets `eval_retries` to 0 for each fresh turn

#### Node 2: `router_node`
- Sends the question to the LLM with a strict one-word routing prompt
- Validates response is one of: `retrieve`, `tool`, `memory_only`
- Falls back to `retrieve` for any unexpected output

#### Node 3: `retrieval_node`
- Encodes the question using `SentenceTransformer`
- Queries ChromaDB with `n_results=3`
- Formats retrieved chunks with `[Topic]` labels

#### Node 4: `skip_retrieval_node`
- Explicitly clears `retrieved` and `sources` to prevent context leakage from prior turns

#### Node 5: `tool_node`
- Detects query type (date / time / day / month) and returns formatted datetime string
- Wrapped in try/except — never raises, always returns a string (error-safe tool pattern)

#### Node 6: `answer_node`
- Constructs a system prompt with retrieved context, tool result, and recent conversation
- Injects retry instruction if `eval_retries > 0`
- Prepends employee name greeting when name is known
- Strict grounding rule: "Answer ONLY from context — if not found, direct to hr@company.com"

#### Node 7: `eval_node`
- Skips evaluation if no context was retrieved (tool/memory routes get faithfulness = 1.0)
- Sends context + answer to LLM and asks for a single decimal score
- Increments `eval_retries` counter

#### Node 8: `save_node`
- Appends final answer to conversation history as `{"role": "assistant", "content": answer}`

### Conditional Edges

```python
# After router_node:
route_decision → {"retrieve": "retrieve", "skip": "skip", "tool": "tool"}

# After eval_node:
eval_decision → {"answer": "answer", "save": "save"}
# Retry condition: faithfulness < 0.7 AND eval_retries < 2
```

---

## 6. RAG Pipeline Deep Dive

### Embedding Model

**`all-MiniLM-L6-v2`** (Sentence Transformers) was chosen for:
- Fast inference (no API call required)
- Strong semantic similarity for short policy Q&A
- 384-dimensional embeddings — small and efficient for in-memory ChromaDB

### ChromaDB Setup

```python
client = chromadb.Client()  # In-memory (no persistence required for demo)
collection = client.create_collection("hr_policy_kb")
collection.add(
    documents=texts,      # Raw policy text
    embeddings=embeddings, # Pre-computed with SentenceTransformer
    ids=ids,
    metadatas=metadatas,  # {"topic": "Annual Leave Policy"}
)
```

### Retrieval

For each question, top-3 semantically closest chunks are retrieved and formatted:
```
[Annual Leave Policy]
All permanent employees are entitled to 18 days of paid annual leave...

[Sick Leave Policy]
For absences exceeding 2 consecutive days, a medical certificate...
```

This multi-document context improves answer completeness for questions that span policy boundaries.

---

## 7. Self-Reflection & Eval Loop

One of the most unique features of this system is the **built-in faithfulness evaluation** powered by the same LLM used for generation.

### Evaluation Prompt

The eval node sends a targeted prompt asking the LLM to rate (0.0–1.0) how faithfully the answer sticks to the retrieved context, where:
- `1.0` = answer uses ONLY information from the context
- `0.0` = answer contradicts or ignores the context

### Retry Mechanism

```
eval_node scores answer
    │
    ├── score ≥ 0.7 OR retries ≥ 2 → save_node (END)
    │
    └── score < 0.7 AND retries < 2 → answer_node (RETRY)
                                            │
                                     retry_instruction injected:
                                     "Be more precise. Every statement
                                      must come from context below."
```

This creates a feedback loop that catches hallucinations before they reach the user — without any external evaluation tool.

---

## 8. Streamlit UI

The UI (`ui/app.py`) features:

- **Dark theme** with CSS custom properties (`--bg`, `--card`, `--blue`, `--cyan`)
- **Sora + JetBrains Mono** font stack for a modern AI product feel
- **Sidebar** with brand header, session stats (messages, topics retrieved, avg faithfulness), and quick-topic navigation chips
- **Chat interface** with animated message bubbles (user = indigo gradient, bot = dark card)
- **Source tags** displayed below each bot reply (e.g., `Annual Leave Policy`, `WFH Policy`)
- **Faithfulness bar** rendered under each answer showing the eval score visually
- **Route badge** showing `retrieve`, `tool`, or `memory_only` for transparency
- **New Conversation** button to reset the thread ID and clear history

---

## 9. Testing & Evaluation

### Functional Test Suite (`tests/test_agent.py`)

13 test questions covering all major routing paths:

| Category | Example Questions |
|---|---|
| RAG — Leave | "How many days of annual leave do I get?" |
| RAG — WFH | "Can I work from home during probation?" |
| RAG — Payroll | "When will my salary be credited?" |
| RAG — Benefits | "What is the maternity leave entitlement?" |
| Tool | "What is today's date?" |
| Memory | "Hi!", "Thanks!" |
| Out-of-scope | "What is the company's revenue?" |

Output is a formatted table with route taken, faithfulness score, and a preview of the answer.

### RAGAS Evaluation (`tests/ragas_eval.py`)

Runs the pipeline against RAGAS metrics:
- **Faithfulness** — are claims supported by context?
- **Answer Relevancy** — does the answer address the question?
- **Context Recall** — is the relevant context retrieved?

---

## 10. Setup & Deployment

### Prerequisites

- Python 3.10+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Quick Start

```bash
# 1. Clone
git clone https://github.com/your-username/hr-policy-bot.git
cd hr-policy-bot

# 2. Virtual environment
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install
pip install -r requirements.txt

# 4. Configure
echo "GROQ_API_KEY=your_key_here" > .env

# 5. Run Streamlit
streamlit run ui/app.py

# OR terminal mode
python main.py
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Groq API key for LLaMA-3.3-70B access |

---

## 11. Design Decisions & Trade-offs

| Decision | Choice | Rationale |
|---|---|---|
| LLM Provider | Groq (not OpenAI) | Ultra-low latency inference; free tier available |
| Embedding Model | Local SentenceTransformer | No API cost; deterministic; fast |
| Vector DB | ChromaDB in-memory | No server setup; sufficient for 10-doc KB |
| Graph Framework | LangGraph | Native StateGraph + MemorySaver; retry loops are first-class |
| Eval Strategy | LLM-as-judge | No external eval API needed; same model scores faithfulness |
| Temperature | 0 | Maximum determinism for policy answers |
| Routing | LLM-based | Flexible; handles edge cases better than keyword matching |

---
## 12. Screenshots
<img width="1919" height="1001" alt="image" src="https://github.com/user-attachments/assets/4d5f472d-d866-41b0-bc30-ccdaa114d504" />

## 13. Future Improvements

| Priority | Improvement | Description |
|---|---|---|
| High | Persistent ChromaDB | Replace in-memory with persisted collection to survive restarts |
| High | PDF Ingestion Pipeline | Auto-ingest company HR PDF updates into the knowledge base |
| High | Authentication | Employee login → personalised leave balance lookups |
| Medium | HR System Integration | Connect to HRMS (e.g., Workday, Zoho People) for real-time data |
| Medium | Multi-language Support | Hindi and regional language query support |
| Medium | Voice Interface | Speech-to-text input for mobile / frontline workers |
| Low | Analytics Dashboard | Query volume, top topics, faithfulness trend over time |
| Low | Escalation Workflow | Low-confidence answers auto-route to HR email ticket |

---


