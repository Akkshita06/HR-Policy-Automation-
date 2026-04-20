# 🚀 HR Policy Bot — Agentic AI Capstone 2026

A production-ready multi-turn HR Policy Assistant built using LangGraph, ChromaDB (RAG), Groq LLM, and Streamlit.

This project demonstrates a complete agentic pipeline with memory, retrieval, tool usage, and self-evaluation—simulating a real-world HR assistant.

---

## ✨ Features

- Agentic workflow using LangGraph (multi-node pipeline)
- Retrieval-Augmented Generation (ChromaDB)
- Multi-turn conversational memory
- Self-evaluation loop for response quality
- Tool integration (datetime)
- Streamlit-based web UI
- Test suite + RAGAS evaluation

---

## 📂 Project Structure
hr_policy_bot/
├── agent/
│ ├── knowledge_base.py
│ ├── state.py
│ ├── nodes.py
│ └── graph.py
├── ui/
│ └── app.py
├── tests/
│ ├── test_agent.py
│ └── ragas_eval.py
├── main.py
├── requirements.txt
├── .env.example
└── README.md

---

## ⚙️ Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/hr_policy_bot.git
cd hr_policy_bot

## Create Virtual Environment
python -m venv venv

 Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create a .env file:

GROQ_API_KEY=your_actual_groq_api_key
▶️ Running the Project
Streamlit UI (Recommended)
streamlit run ui/app.py

Open: http://localhost:8501

Terminal Chat
python main.py
Run Tests
python tests/test_agent.py
RAGAS Evaluation
python tests/ragas_eval.py
🧠 Architecture
User Input
   ↓
memory_node     → manages conversation state
   ↓
router_node     → decides: retrieve | tool | memory
   ↓
retrieval_node  → fetches context from ChromaDB
tool_node       → executes tools (datetime)
skip_node       → bypass retrieval when needed
   ↓
answer_node     → generates response (LLM)
   ↓
eval_node       → checks faithfulness (retry if needed)
   ↓
save_node       → updates memory → END
📊 Capabilities
#	Capability	Implementation
1	LangGraph StateGraph (8 nodes)	agent/graph.py
2	ChromaDB RAG	agent/knowledge_base.py
3	Conversational Memory	MemorySaver
4	Self-Evaluation Loop	eval_node
5	Tool Usage	tool_node
6	Streamlit UI	ui/app.py
🛠️ Tech Stack
LangGraph
ChromaDB
Groq LLM
Streamlit
RAGAS
🚀 Deployment

You can deploy this app using:

Streamlit Cloud
Render
⚠️ Notes
Do not commit your .env file
Always run commands from the root directory
Ensure dependencies are installed before running
📌 Future Improvements
Add authentication
Expand HR knowledge base
Add more tools (payroll, leave balance)
Improve evaluation metrics
📄 License

MIT License

👤 Author

Akshita N

