# agent/nodes.py
# All 8 LangGraph node functions for the HR Policy Bot

from datetime import datetime
from langchain_core.messages import HumanMessage
from agent.state import CapstoneState

FAITHFULNESS_THRESHOLD = 0.7
MAX_EVAL_RETRIES = 2


# ── NODE 1: memory_node ───────────────────────────────────────────────────────
def memory_node(state: CapstoneState, llm, embedder, collection) -> dict:
    """
    - Appends question to message history
    - Applies sliding window (last 6 messages)
    - Extracts employee name if introduced
    - Resets eval_retries to 0 for fresh turn
    """
    messages = list(state.get("messages", []))
    question = state["question"]

    messages.append({"role": "user", "content": question})
    messages = messages[-6:]  # Sliding window

    # Extract name if employee says "my name is ..."
    user_name = state.get("user_name", "")
    q_lower = question.lower()
    if "my name is" in q_lower:
        after = q_lower.split("my name is")[-1].strip()
        candidate = after.split()[0].replace(",", "").replace(".", "")
        if candidate.isalpha():
            user_name = candidate.capitalize()

    return {
        "messages": messages,
        "user_name": user_name,
        "eval_retries": 0,
    }


# ── NODE 2: router_node ───────────────────────────────────────────────────────
def router_node(state: CapstoneState, llm, embedder, collection) -> dict:
    """
    Routes the question to one of three paths:
      retrieve    → ChromaDB RAG for HR policy questions
      tool        → datetime/calculator tool
      memory_only → casual greetings or already-answered context
    """
    question = state["question"]

    prompt = f"""You are a routing assistant for an HR Policy Bot.
Read the employee question carefully and respond with EXACTLY ONE word.

Routes:
- retrieve    : question is about HR policy, leave, payroll, WFH, benefits, performance, conduct, travel, resignation
- tool        : question requires today's current date, current time, or a date calculation
- memory_only : casual greeting (hi, hello, thanks) OR the answer is clearly in the recent conversation

Employee question: {question}

Respond with exactly one word — retrieve, tool, or memory_only. Nothing else."""

    response = llm.invoke([HumanMessage(content=prompt)])
    route = response.content.strip().lower().split()[0]
    if route not in ["retrieve", "tool", "memory_only"]:
        route = "retrieve"

    print(f"[router] route = {route}")
    return {"route": route}


# ── NODE 3: retrieval_node ────────────────────────────────────────────────────
def retrieval_node(state: CapstoneState, llm, embedder, collection) -> dict:
    """
    Embeds the question and queries ChromaDB for top-3 relevant HR policy chunks.
    Formats context with [Topic] labels.
    """
    question = state["question"]
    q_embed = embedder.encode([question]).tolist()
    results = collection.query(query_embeddings=q_embed, n_results=3)

    docs   = results["documents"][0]
    metas  = results["metadatas"][0]
    sources = [m["topic"] for m in metas]

    context = ""
    for doc, meta in zip(docs, metas):
        context += f"[{meta['topic']}]\n{doc.strip()}\n\n"

    print(f"[retrieval] sources = {sources}")
    return {"retrieved": context, "sources": sources}


# ── NODE 4: skip_retrieval_node ───────────────────────────────────────────────
def skip_retrieval_node(state: CapstoneState, llm, embedder, collection) -> dict:
    """
    Clears retrieved context for tool/memory_only routes.
    MUST explicitly set retrieved='' — empty dict causes previous context to leak.
    """
    return {"retrieved": "", "sources": []}


# ── NODE 5: tool_node ─────────────────────────────────────────────────────────
def tool_node(state: CapstoneState, llm, embedder, collection) -> dict:
    """
    Datetime tool — answers questions about current date, time, and day.
    Tools MUST NEVER raise exceptions — always return an error string instead.
    """
    question = state["question"].lower()
    try:
        now = datetime.now()
        if "date" in question:
            result = f"Today's date is {now.strftime('%A, %B %d, %Y')}."
        elif "time" in question:
            result = f"The current time is {now.strftime('%I:%M %p')}."
        elif "day" in question:
            result = f"Today is {now.strftime('%A')}."
        elif "month" in question:
            result = f"The current month is {now.strftime('%B %Y')}."
        else:
            result = f"Current date and time: {now.strftime('%A, %B %d, %Y at %I:%M %p')}."
    except Exception as e:
        result = f"Tool error: {str(e)}"  # Never raise — return error string

    print(f"[tool] result = {result}")
    return {"tool_result": result}


# ── NODE 6: answer_node ───────────────────────────────────────────────────────
def answer_node(state: CapstoneState, llm, embedder, collection) -> dict:
    """
    Generates the final answer using:
      - Retrieved HR policy context (if retrieve route)
      - Tool result (if tool route)
      - Conversation history
    Grounding rule: answer ONLY from context — no hallucination.
    """
    question    = state["question"]
    retrieved   = state.get("retrieved", "")
    tool_result = state.get("tool_result", "")
    messages    = state.get("messages", [])
    retries     = state.get("eval_retries", 0)
    user_name   = state.get("user_name", "")

    greeting = f"Hi {user_name}! " if user_name else ""

    retry_instruction = ""
    if retries > 0:
        retry_instruction = (
            "\n⚠ IMPORTANT: Your previous answer scored low on faithfulness. "
            "Be more precise and ensure every statement comes directly from the context below."
        )

    history_text = "\n".join(
        [f"{m['role'].upper()}: {m['content']}" for m in messages[-4:]]
    ) if messages else "No prior conversation."

    system_prompt = f"""You are a friendly, professional HR Policy Assistant for a company.
{retry_instruction}

STRICT RULE: Answer ONLY using the HR POLICY CONTEXT or TOOL RESULT provided below.
- If the answer is not in the context, respond: "I don't have this information in our HR policy documents. Please contact HR at hr@company.com or call the HR helpline."
- Never invent policies, numbers, dates, or benefits not mentioned in the context.
- Be concise, clear, and empathetic.
- If sources are available, mention the policy name at the end (e.g., "Per the Annual Leave Policy...").

━━━ HR POLICY CONTEXT ━━━
{retrieved if retrieved else "No policy context retrieved for this question."}

━━━ TOOL RESULT ━━━
{tool_result if tool_result else "No tool result."}

━━━ RECENT CONVERSATION ━━━
{history_text}
"""

    response = llm.invoke([
        HumanMessage(content=system_prompt),
        HumanMessage(content=question),
    ])

    answer = greeting + response.content.strip()
    print(f"[answer] length = {len(answer)} chars")
    return {"answer": answer}


# ── NODE 7: eval_node ─────────────────────────────────────────────────────────
def eval_node(state: CapstoneState, llm, embedder, collection) -> dict:
    """
    Rates the answer's faithfulness to the retrieved context (0.0 – 1.0).
    Skips evaluation for tool/memory_only routes (no retrieved context).
    Increments eval_retries counter.
    """
    answer    = state.get("answer", "")
    retrieved = state.get("retrieved", "")
    retries   = state.get("eval_retries", 0)

    if not retrieved.strip():
        # No context to evaluate against — skip
        print("[eval] skipped (no retrieved context)")
        return {"faithfulness": 1.0, "eval_retries": retries}

    prompt = f"""You are a faithfulness evaluator.
Rate how faithfully the answer sticks to the provided context.
Score must be between 0.0 and 1.0.
1.0 = answer uses ONLY information from the context.
0.0 = answer contradicts or ignores the context entirely.

Context:
{retrieved[:600]}

Answer:
{answer}

Respond with a single decimal number only (e.g. 0.85). Nothing else."""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        score = float(response.content.strip().split()[0])
        score = max(0.0, min(1.0, score))
    except Exception:
        score = 0.5

    print(f"[eval] faithfulness = {score:.2f} | retries so far = {retries}")
    return {"faithfulness": score, "eval_retries": retries + 1}


# ── NODE 8: save_node ─────────────────────────────────────────────────────────
def save_node(state: CapstoneState, llm, embedder, collection) -> dict:
    """
    Appends the final answer to the conversation history and ends the graph turn.
    """
    messages = list(state.get("messages", []))
    answer   = state.get("answer", "")
    messages.append({"role": "assistant", "content": answer})
    print("[save] turn complete")
    return {"messages": messages}
