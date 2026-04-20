# agent/graph.py
# Assembles and compiles the LangGraph StateGraph for the HR Policy Bot

import os
from functools import partial

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from sentence_transformers import SentenceTransformer
import chromadb

from agent.state import CapstoneState
from agent.nodes import (
    memory_node, router_node, retrieval_node,
    skip_retrieval_node, tool_node, answer_node,
    eval_node, save_node,
    FAITHFULNESS_THRESHOLD, MAX_EVAL_RETRIES,
)
from agent.knowledge_base import HR_DOCUMENTS

load_dotenv()


# ── Routing functions ─────────────────────────────────────────────────────────

def route_decision(state: CapstoneState) -> str:
    """Called after router_node — decides which path to take."""
    route = state.get("route", "retrieve")
    if route == "tool":
        return "tool"
    if route == "memory_only":
        return "skip"
    return "retrieve"


def eval_decision(state: CapstoneState) -> str:
    """Called after eval_node — retry answer if faithfulness is low."""
    score   = state.get("faithfulness", 1.0)
    retries = state.get("eval_retries", 0)
    if score < FAITHFULNESS_THRESHOLD and retries < MAX_EVAL_RETRIES:
        print(f"[eval_decision] RETRY (score={score:.2f}, retries={retries})")
        return "answer"
    print(f"[eval_decision] SAVE (score={score:.2f}, retries={retries})")
    return "save"




def setup_resources():
    """Initialise LLM, embedding model, and ChromaDB knowledge base."""
    api_key = os.getenv("GROQ")
    if not api_key:
        raise ValueError("GROQ not found. Set it in your .env file.")

    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=api_key)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.Client()
    collection = client.create_collection("hr_policy_kb")

    texts      = [doc["text"]  for doc in HR_DOCUMENTS]
    ids        = [doc["id"]    for doc in HR_DOCUMENTS]
    metadatas  = [{"topic": doc["topic"]} for doc in HR_DOCUMENTS]
    embeddings = embedder.encode(texts).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas,
    )
    print(f"[setup] Knowledge base loaded: {collection.count()} documents")
    return llm, embedder, collection


# ── Build Graph ───────────────────────────────────────────────────────────────

def build_graph(llm, embedder, collection):
    """
    Builds and compiles the LangGraph StateGraph.
    Returns the compiled app (with MemorySaver checkpointer).
    """
    # Wrap nodes with injected dependencies using functools.partial
    def wrap(fn):
        return partial(fn, llm=llm, embedder=embedder, collection=collection)

    graph = StateGraph(CapstoneState)

    # Add all 8 nodes
    graph.add_node("memory",   wrap(memory_node))
    graph.add_node("router",   wrap(router_node))
    graph.add_node("retrieve", wrap(retrieval_node))
    graph.add_node("skip",     wrap(skip_retrieval_node))
    graph.add_node("tool",     wrap(tool_node))
    graph.add_node("answer",   wrap(answer_node))
    graph.add_node("eval",     wrap(eval_node))
    graph.add_node("save",     wrap(save_node))

    # Entry point
    graph.set_entry_point("memory")

    # Fixed edges
    graph.add_edge("memory",   "router")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("skip",     "answer")
    graph.add_edge("tool",     "answer")
    graph.add_edge("answer",   "eval")
    graph.add_edge("save",     END)

    # Conditional edges
    graph.add_conditional_edges(
        "router",
        route_decision,
        {"retrieve": "retrieve", "skip": "skip", "tool": "tool"},
    )
    graph.add_conditional_edges(
        "eval",
        eval_decision,
        {"answer": "answer", "save": "save"},
    )

    app = graph.compile(checkpointer=MemorySaver())
    print("[setup] Graph compiled successfully ✓")
    return app


# ── Helper: ask() ─────────────────────────────────────────────────────────────

def make_ask(app):
    """Returns an ask() function bound to a compiled app."""
    def ask(question: str, thread_id: str = "emp_001") -> dict:
        config = {"configurable": {"thread_id": thread_id}}
        initial_state: CapstoneState = {
            "question":     question,
            "messages":     [],
            "route":        "",
            "retrieved":    "",
            "sources":      [],
            "tool_result":  "",
            "answer":       "",
            "faithfulness": 0.0,
            "eval_retries": 0,
            "user_name":    "",
        }
        result = app.invoke(initial_state, config)
        return result
    return ask
