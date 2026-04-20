# main.py — Run HR Policy Bot in the terminal (interactive chat)
# Usage: python main.py

from agent.graph import setup_resources, build_graph, make_ask

print("=" * 60)
print("  HR Policy Bot — Terminal Chat")
print("  Type 'quit' to exit | Type 'new' to reset conversation")
print("=" * 60)

llm, embedder, collection = setup_resources()
app = build_graph(llm, embedder, collection)
ask = make_ask(app)

thread_id = "terminal_session_001"

while True:
    try:
        question = input("\nYou: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        break

    if not question:
        continue

    if question.lower() == "quit":
        print("Goodbye!")
        break

    if question.lower() == "new":
        from datetime import datetime
        thread_id = f"terminal_{datetime.now().strftime('%H%M%S')}"
        print("[Conversation reset]")
        continue

    result = ask(question, thread_id=thread_id)
    answer  = result.get("answer", "")
    sources = result.get("sources", [])
    route   = result.get("route", "?")
    score   = result.get("faithfulness", None)

    print(f"\nBot: {answer}")
    if sources:
        print(f"     Sources: {', '.join(sources)}")
    print(f"     [Route: {route} | Faithfulness: {score:.2f}]")
