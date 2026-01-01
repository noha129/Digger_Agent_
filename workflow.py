# workflow.py
from typing import TypedDict, Sequence, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
from tools import TOOLS, extract_pdf_text, extract_docx_text
from tools import TOOLS
from prompt import RESEARCH_PROMPT
import json
from langchain_ollama import ChatOllama

# STATE
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    input_type: str
    source: str
    iteration_count: int

# -------------------------
model = ChatOllama(
    model="qwen3:4b",
    temperature=0.6
    
).bind_tools(TOOLS)

# -------------------------
# GRAPH NODES
# -------------------------
def detect_input_node(state: AgentState) -> AgentState:
    user_text = state["messages"][0].content.lower()
    if any(ext in user_text for ext in [".pdf", ".docx"]):
        return {**state, "input_type": "document_summary", "source": state["messages"][0].content, "iteration_count": 0}
    return {**state, "input_type": "search_query", "source": "web_search", "iteration_count": 0}

def agent_node(state: AgentState) -> AgentState:
    response = model.invoke([
        SystemMessage(content=RESEARCH_PROMPT),
        *state["messages"]
    ])
    return {
        **state,
        "messages": [response],
        "iteration_count": state["iteration_count"] + 1
    }

def tool_node(state: AgentState) -> AgentState:
    last = state["messages"][-1]
    tool_msgs = []
    for call in last.tool_calls:
        tool_fn = next(t for t in TOOLS if t.name == call["name"])
        result = tool_fn.invoke(call["args"])
        tool_msgs.append(ToolMessage(tool_call_id=call["id"], content=result))
    return {**state, "messages": tool_msgs}

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return "end"

def check_iterations(state: AgentState) -> Literal["agent", "end"]:
    return "end" if state["iteration_count"] >= 10 else "agent"

# -------------------------
# BUILD GRAPH
# -------------------------
def build_graph():
    g = StateGraph(AgentState)
    g.add_node("detect", detect_input_node)
    g.add_node("agent", agent_node)
    g.add_node("tools", tool_node)

    g.set_entry_point("detect")
    g.add_edge("detect", "agent")

    g.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
    g.add_conditional_edges("tools", check_iterations, {"agent": "agent", "end": END})

    return g.compile()

def run_and_save(user_input: str, slides_count: int = 5, filename: str = "output.json"):
    """
    Accepts:
      - PDF / DOCX path or URL
      - Search query
      - Number of slides
      - JSON output filename
    """
    # Detect document
    user_input_lower = user_input.lower()
    if user_input_lower.endswith(".pdf"):
        print("📄 Detected PDF file. Extracting text...")
        content = extract_pdf_text(user_input)
        input_type = "document_summary"
        source = user_input
    elif user_input_lower.endswith(".docx"):
        print("📄 Detected DOCX file. Extracting text...")
        content = extract_docx_text(user_input)
        input_type = "document_summary"
        source = user_input
    else:
        # Treat as search query
        content = user_input
        input_type = "search_query"
        source = "web_search"

    # Append number of slides to prompt
    full_input = f"{content} in {slides_count} slides"

    # Build graph and run
    app = build_graph()
    final_state = app.invoke({
        "messages": [HumanMessage(content=full_input)],
        "input_type": input_type,
        "source": source,
        "iteration_count": 0
    })

    raw_output = final_state["messages"][-1].content

    # Clean code blocks if present
    clean_output = raw_output.strip()
    for tag in ["```json", "```"]:
        if clean_output.startswith(tag):
            clean_output = clean_output[len(tag):]
        if clean_output.endswith(tag):
            clean_output = clean_output[:-len(tag)]
    clean_output = clean_output.strip()

    # Try parsing JSON
    try:
        parsed = json.loads(clean_output)
    except json.JSONDecodeError:
        print("\n❌ JSON parse error. Returning raw output instead.")
        parsed = {"raw_output": clean_output}

    # Save JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)

    print(f"\n✅ JSON saved as: {filename}")
    return parsed
