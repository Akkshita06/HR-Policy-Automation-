# tests/ragas_eval.py
# Run with:  python tests/ragas_eval.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.graph import setup_resources, build_graph, make_ask

print("=" * 60)
print("  HR Policy Bot — RAGAS Baseline Evaluation")
print("=" * 60)

llm, embedder, collection = setup_resources()
app = build_graph(llm, embedder, collection)
ask = make_ask(app)

# ── 5 QA pairs with ground truth ─────────────────────────────────────────────
eval_questions = [
    "How many annual leave days do employees get?",
    "What is the WFH policy?",
    "When is salary credited?",
    "What is the notice period for resignation?",
    "What health insurance does the company provide?",
]

ground_truths = [
    "Employees are entitled to 18 days of paid annual leave per calendar year.",
    "Employees may work from home up to 2 days per week with manager approval, after completing probation.",
    "Salaries are credited to the registered bank account on the last working day of every calendar month.",
    "All permanent employees are required to serve a notice period of 60 calendar days upon resignation.",
    "All permanent employees and their immediate family are covered under group health insurance of Rs 3 lakhs per annum.",
]

# ── Collect answers and contexts from the agent ───────────────────────────────
answers  = []
contexts = []

print("\nRunning agent for each evaluation question...")
for i, question in enumerate(eval_questions, 1):
    print(f"  Q{i}: {question[:55]}...")
    result = ask(question, thread_id=f"ragas_{i}")
    answers.append(result.get("answer", ""))
    contexts.append([result.get("retrieved", "")])

# ── Run RAGAS ─────────────────────────────────────────────────────────────────
try:
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy, context_precision
    from datasets import Dataset

    dataset = Dataset.from_dict({
        "question":     eval_questions,
        "answer":       answers,
        "contexts":     contexts,
        "ground_truth": ground_truths,
    })

    print("\nRunning RAGAS evaluation...")
    scores = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])

    print("\n" + "=" * 60)
    print("  RAGAS BASELINE SCORES")
    print("=" * 60)
    print(f"  Faithfulness:      {scores['faithfulness']:.4f}")
    print(f"  Answer Relevancy:  {scores['answer_relevancy']:.4f}")
    print(f"  Context Precision: {scores['context_precision']:.4f}")
    print("=" * 60)
    print("\n  Record these scores in your written summary.")

except ImportError:
    print("\n[!] RAGAS not installed. Running manual faithfulness evaluation instead.")
    print("\nManual Faithfulness Scores:")
    print("-" * 60)
    for i, (q, a, ctx) in enumerate(zip(eval_questions, answers, contexts), 1):
        prompt = f"""Rate faithfulness 0.0 to 1.0.
Context: {ctx[0][:400]}
Answer: {a}
Respond with ONE decimal number only."""
        from langchain_core.messages import HumanMessage
        try:
            resp = llm.invoke([HumanMessage(content=prompt)])
            score = float(resp.content.strip().split()[0])
        except Exception:
            score = 0.5
        print(f"  Q{i}: {score:.2f}  |  {q[:50]}...")
