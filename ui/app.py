# ui/app.py  —  HR Policy Bot  |  Redesigned UI
# Run with:  streamlit run ui/app.py --server.fileWatcherType none

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime
from agent.graph import setup_resources, build_graph, make_ask

st.set_page_config(page_title="HR Policy Bot", page_icon="📋", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --bg:      #0a0f1e; --bg2: #111827; --card: #1a2235; --hover: #1e2d47;
    --blue:    #3b82f6; --cyan: #06b6d4; --green: #10b981; --amber: #f59e0b;
    --txt:     #f1f5f9; --muted: #94a3b8; --dim: #475569;
    --border:  #1e3a5f; --border2: #2d4a6e;
    --glow:    0 0 20px rgba(59,130,246,0.15);
}
html,body,[class*="css"]{font-family:'Sora',sans-serif!important;background:var(--bg)!important;color:var(--txt)!important;}
#MainMenu,footer,header{visibility:hidden;}
.stApp{background:linear-gradient(135deg,#0a0f1e 0%,#0d1529 50%,#0a1628 100%)!important;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d1829,#0a1220)!important;border-right:1px solid var(--border)!important;}
.block-container{padding:1.5rem 2rem!important;max-width:900px!important;}

.brand{padding:2rem 1.5rem 1rem;border-bottom:1px solid var(--border);}
.brand-icon{width:42px;height:42px;background:linear-gradient(135deg,var(--blue),var(--cyan));border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:.75rem;box-shadow:var(--glow);}
.brand h2{font-size:1.1rem!important;font-weight:700!important;color:var(--txt)!important;margin:0 0 2px!important;}
.brand p{font-size:.7rem!important;color:var(--muted)!important;margin:0!important;text-transform:uppercase;letter-spacing:.5px;}

.stats{display:flex;gap:.5rem;padding:1rem 1.5rem;border-bottom:1px solid var(--border);}
.stat{flex:1;background:var(--card);border:1px solid var(--border);border-radius:8px;padding:.5rem .4rem;text-align:center;}
.stat b{font-size:1.1rem;font-weight:700;color:var(--cyan);display:block;line-height:1;}
.stat s2{font-size:.6rem;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;display:block;margin-top:2px;}

.th{padding:1rem 1.5rem .4rem;font-size:.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:var(--dim);}
.tc{display:flex;align-items:center;gap:.6rem;padding:.5rem 1.5rem;border-left:2px solid transparent;transition:all .15s;}
.tc:hover{background:var(--hover);border-left-color:var(--blue);}
.ti{width:26px;height:26px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;}
.tn{font-size:.78rem;color:var(--txt);}

.chat-hdr{display:flex;align-items:center;gap:1rem;padding:1.5rem 0 1.2rem;border-bottom:1px solid var(--border);margin-bottom:1.5rem;}
.hdr-icon{width:46px;height:46px;background:linear-gradient(135deg,var(--blue),var(--cyan));border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:var(--glow);flex-shrink:0;}
.hdr-text h2{font-size:1.25rem!important;font-weight:700!important;color:var(--txt)!important;margin:0 0 2px!important;}
.hdr-text p{font-size:.78rem!important;color:var(--muted)!important;margin:0!important;}
.online{margin-left:auto;display:flex;align-items:center;gap:.4rem;background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);border-radius:20px;padding:.3rem .75rem;font-size:.7rem;color:var(--green);font-weight:500;}
.dot{width:6px;height:6px;border-radius:50%;background:var(--green);animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}

.welcome{background:linear-gradient(135deg,rgba(59,130,246,.08),rgba(6,182,212,.05));border:1px solid rgba(59,130,246,.2);border-radius:14px;padding:1.5rem;margin-bottom:1.5rem;}
.welcome h3{font-size:1rem!important;font-weight:600!important;color:var(--txt)!important;margin:0 0 .5rem!important;}
.welcome p{font-size:.82rem!important;color:var(--muted)!important;margin:0 0 1rem!important;line-height:1.6;}
.pills{display:flex;flex-wrap:wrap;gap:.5rem;}
.pill{background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.25);border-radius:20px;padding:.3rem .75rem;font-size:.74rem;color:#93c5fd;}

.row{display:flex;gap:.75rem;margin-bottom:1.2rem;animation:fu .3s ease;}
@keyframes fu{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.row.u{flex-direction:row-reverse;}
.av{width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;margin-top:2px;}
.av.b{background:linear-gradient(135deg,var(--blue),var(--cyan));box-shadow:0 0 12px rgba(59,130,246,.3);}
.av.u2{background:linear-gradient(135deg,#6366f1,#8b5cf6);}
.bub{max-width:75%;border-radius:14px;padding:.85rem 1.1rem;line-height:1.65;font-size:.87rem;}
.bub.b2{background:var(--card);border:1px solid var(--border);color:var(--txt);border-top-left-radius:4px;}
.bub.u3{background:linear-gradient(135deg,#1d4ed8,#2563eb);color:#fff;border-top-right-radius:4px;border:1px solid rgba(59,130,246,.3);}
.srcs{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.65rem;}
.src{background:rgba(6,182,212,.1);border:1px solid rgba(6,182,212,.2);border-radius:6px;padding:.2rem .55rem;font-size:.67rem;color:var(--cyan);font-family:'JetBrains Mono',monospace;}
.fb{margin-top:.6rem;display:flex;align-items:center;gap:.5rem;}
.fl{font-size:.63rem;color:var(--dim);white-space:nowrap;font-family:'JetBrains Mono',monospace;}
.fbg{flex:1;height:4px;background:rgba(255,255,255,.06);border-radius:2px;overflow:hidden;}
.ff{height:100%;border-radius:2px;}
.rb{display:inline-block;font-size:.62rem;font-family:'JetBrains Mono',monospace;padding:.15rem .5rem;border-radius:4px;margin-top:.5rem;}
.rr{background:rgba(59,130,246,.15);color:#60a5fa;border:1px solid rgba(59,130,246,.2);}
.rt{background:rgba(245,158,11,.15);color:#fbbf24;border:1px solid rgba(245,158,11,.2);}
.rm{background:rgba(16,185,129,.15);color:#34d399;border:1px solid rgba(16,185,129,.2);}
.ts{font-size:.6rem;color:var(--dim);margin-top:.3rem;padding:0 .2rem;}
.row.u .ts{text-align:right;}

.typing{display:flex;align-items:center;gap:.75rem;margin-bottom:1.2rem;}
.tdots{display:flex;gap:4px;background:var(--card);border:1px solid var(--border);border-radius:14px;border-top-left-radius:4px;padding:.85rem 1rem;}
.tdots span{width:7px;height:7px;border-radius:50%;background:var(--blue);animation:b 1.2s infinite;}
.tdots span:nth-child(2){animation-delay:.2s}.tdots span:nth-child(3){animation-delay:.4s}
@keyframes b{0%,80%,100%{transform:translateY(0);opacity:.4}40%{transform:translateY(-6px);opacity:1}}

.stButton button{background:rgba(59,130,246,.1)!important;border:1px solid rgba(59,130,246,.3)!important;color:#93c5fd!important;border-radius:10px!important;font-family:'Sora',sans-serif!important;font-size:.8rem!important;font-weight:500!important;width:100%!important;}
.stButton button:hover{background:rgba(59,130,246,.2)!important;}
hr{border-color:var(--border)!important;}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_agent():
    llm, embedder, collection = setup_resources()
    app = build_graph(llm, embedder, collection)
    return make_ask(app)

ask = load_agent()

if "messages"  not in st.session_state: st.session_state.messages  = []
if "thread_id" not in st.session_state: st.session_state.thread_id = "emp_001"

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">📋</div>
        <h2>HR Policy Bot</h2>
        <p>Agentic AI Capstone 2026</p>
    </div>""", unsafe_allow_html=True)

    asked = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    st.markdown(f"""
    <div class="stats">
        <div class="stat"><b>10</b><s2>Policies</s2></div>
        <div class="stat"><b>{asked}</b><s2>Asked</s2></div>
        <div class="stat"><b>8</b><s2>Nodes</s2></div>
    </div>""", unsafe_allow_html=True)

    topics = [
        ("🏖️","#3b82f6","Annual Leave"),("🤒","#ef4444","Sick Leave"),
        ("🏠","#10b981","Work From Home"),("💰","#f59e0b","Payroll & Salary"),
        ("👶","#8b5cf6","Maternity / Paternity"),("📊","#06b6d4","Performance Review"),
        ("⚖️","#ec4899","Code of Conduct"),("✈️","#f97316","Travel & Expenses"),
        ("🚪","#64748b","Resignation & Exit"),("🎁","#14b8a6","Benefits & Perks"),
    ]
    st.markdown('<div class="th">📚 &nbsp;Topics Covered</div>', unsafe_allow_html=True)
    for icon, color, name in topics:
        st.markdown(f"""
        <div class="tc">
            <div class="ti" style="background:color-mix(in srgb,{color} 20%,transparent 80%)">{icon}</div>
            <span class="tn">{name}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col = st.columns(1)[0]
    if col.button("↺  New Conversation"):
        st.session_state.messages  = []
        st.session_state.thread_id = f"emp_{datetime.now().strftime('%H%M%S')}"
        st.rerun()

    st.markdown("""
    <div style="padding:1rem 1.5rem 0;font-size:.68rem;color:#475569;line-height:1.8">
        <strong style="color:#64748b">Architecture</strong><br>
        LangGraph &nbsp;·&nbsp; ChromaDB RAG<br>
        MemorySaver &nbsp;·&nbsp; Eval Node<br>
        Groq LLaMA 3.3 &nbsp;·&nbsp; Streamlit<br><br>
        <strong style="color:#64748b">HR Support</strong><br>hr@company.com
    </div>""", unsafe_allow_html=True)


# ── MAIN ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-hdr">
    <div class="hdr-icon">🤖</div>
    <div class="hdr-text">
        <h2>HR Policy Assistant</h2>
        <p>LangGraph · ChromaDB RAG · MemorySaver · Self-Eval · Groq LLaMA 3.3</p>
    </div>
    <div class="online"><div class="dot"></div>Online</div>
</div>""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <h3>👋 Welcome! Ask me anything about company HR policies.</h3>
        <p>I have 10 HR policy documents, remember our full conversation,
        score every answer for accuracy, and honestly tell you when I don't know something.</p>
        <div class="pills">
            <span class="pill">How many leave days do I get?</span>
            <span class="pill">What is the WFH policy?</span>
            <span class="pill">When is salary credited?</span>
            <span class="pill">What is the notice period?</span>
            <span class="pill">What benefits does the company offer?</span>
            <span class="pill">What is today's date?</span>
        </div>
    </div>""", unsafe_allow_html=True)

def fc(s):
    if s>=.8: return "#10b981"
    if s>=.6: return "#f59e0b"
    return "#ef4444"

for msg in st.session_state.messages:
    role    = msg["role"]
    content = msg["content"]
    sources = msg.get("sources",[])
    route   = msg.get("route","")
    faith   = msg.get("faithfulness", None)
    ts      = msg.get("time","")

    if role == "user":
        st.markdown(f"""
        <div class="row u">
            <div class="av u2">👤</div>
            <div><div class="bub u3">{content}</div><div class="ts">{ts}</div></div>
        </div>""", unsafe_allow_html=True)
    else:
        src_html = ""
        if sources:
            tags = "".join(f'<span class="src">{s}</span>' for s in sources)
            src_html = f'<div class="srcs">{tags}</div>'

        faith_html = ""
        if faith is not None and sources:
            pct   = int(faith*100)
            color = fc(faith)
            faith_html = f"""<div class="fb">
                <span class="fl">Faithfulness</span>
                <div class="fbg"><div class="ff" style="width:{pct}%;background:{color}"></div></div>
                <span class="fl" style="color:{color}">{pct}%</span></div>"""

        rc = {"retrieve":"rr","tool":"rt"}.get(route,"rm")
        rl = {"retrieve":"⬡ retrieve","tool":"⚡ tool"}.get(route,"◈ memory")
        rbadge = f'<span class="rb {rc}">{rl}</span>' if route else ""

        st.markdown(f"""
        <div class="row">
            <div class="av b">🤖</div>
            <div>
                <div class="bub b2">{content}{src_html}{faith_html}{rbadge}</div>
                <div class="ts">{ts}</div>
            </div>
        </div>""", unsafe_allow_html=True)


if prompt := st.chat_input("Ask about leave, payroll, WFH, benefits, resignation..."):
    ts = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role":"user","content":prompt,"time":ts})

    ph = st.empty()
    ph.markdown("""
    <div class="typing">
        <div class="av b" style="width:34px;height:34px;border-radius:10px;
             background:linear-gradient(135deg,#3b82f6,#06b6d4);
             display:flex;align-items:center;justify-content:center;font-size:15px;">🤖</div>
        <div class="tdots"><span></span><span></span><span></span></div>
    </div>""", unsafe_allow_html=True)

    result      = ask(prompt, thread_id=st.session_state.thread_id)
    answer      = result.get("answer","Sorry, I could not process that.")
    sources     = result.get("sources",[])
    route       = result.get("route","")
    faithfulness = result.get("faithfulness", None)

    ph.empty()
    st.session_state.messages.append({
        "role":"assistant","content":answer,"sources":sources,
        "route":route,"faithfulness":faithfulness,
        "time":datetime.now().strftime("%I:%M %p"),
    })
    st.rerun()
