# agent/state.py
# CapstoneState — single source of truth passed between all LangGraph nodes

from typing import TypedDict, List


class CapstoneState(TypedDict):
    question:     str         # Current employee question
    messages:     List[dict]  # Full conversation history (sliding window of 6)
    route:        str         # Router decision: 'retrieve' | 'tool' | 'memory_only'
    retrieved:    str         # Retrieved HR policy context string
    sources:      List[str]   # List of source topic names from ChromaDB
    tool_result:  str         # Result returned by the tool node
    answer:       str         # Final LLM-generated answer
    faithfulness: float       # Faithfulness score from eval node (0.0 – 1.0)
    eval_retries: int         # Number of eval retries attempted so far
    user_name:    str         # Employee name extracted from conversation
