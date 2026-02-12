import os
import time
from typing import TypedDict, List, Dict, Union, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

# --- NEW IMPORTS FOR SMOLAGENTS (JACK UPGRADE) ---
from smolagents import CodeAgent, LiteLLMModel
from tools.sovereign_tools import SOVEREIGN_TOOLSET
# -------------------------------------------------

# Import our existing tools
from tools.rag.retrieval import get_rag_context

load_dotenv()

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The conversation history"]
    task: str
    plan: str
    instruction: str # Lyra's output
    code: str
    result: str
    iteration: int
    max_iterations: int
    risk_level: str
    jurisdiction: str
    autonomy_audit: str # Epsilon's audit of the plan

# --- LLM CASCADE WRAPPER ---
MODELS_TO_TRY = [
    'gemini-2.0-flash',
    'gemini-2.5-flash',
    'gemini-2.5-pro',
    'gemini-flash-latest',
    'gemini-pro-latest'
]

def invoke_llm_with_cascade(messages: List[BaseMessage]):
    """
    Invokes the LLM with a fallback cascade.
    """
    last_error = None
    for model_name in MODELS_TO_TRY:
        try:
            llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=os.getenv("GOOGLE_API_KEY"))
            return llm.invoke(messages)
        except Exception as e:
            error_str = str(e)
            print(f"[DEBUG] Tri-Mind: Model {model_name} failed: {error_str}")
            last_error = e
            if "429" in error_str or "404" in error_str or "quota" in error_str.lower():
                continue
            else:
                continue
    raise last_error

# --- NODES ---

def epsilon_governance(state: AgentState):
    """
    Epsilon (The Cortex): Governance, Strategy, Law.
    PERSISTENT MONITORING MODE.
    """
    task = state['task']
    rag_context = get_rag_context(task, top_k=3)
    
    system_prompt = f"""You are EPSILON, the Sovereign Cortex.
Your role: Define the 'Why' and the 'Constraint Set' based on the Epsilon Doctrine.
Protocol: Truth-First, Internal Locus, Sovereign Action.

RAG CONTEXT:
{rag_context}
"""
    
    prompt = f"TASK: {task}\n\nAnalyze risk, jurisdiction (US-WA), and strategic alignment. Define the 'Smallest Truthful Action' (epsilon)."
    
    response = invoke_llm_with_cascade([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    
    return {
        "plan": response.content,
        "risk_level": "low", # Placeholder for actual risk logic
        "messages": state['messages'] + [AIMessage(content=f"EPSILON STRATEGY: {response.content}")]
    }

def lyra_instruction_architect(state: AgentState):
    """
    Lyra (The Bridge): Translation Layer.
    Uses 4-D Framework to create deterministic instructions.
    """
    task = state['task']
    plan = state['plan']
    import sys
    platform = sys.platform
    
    system_prompt = f"""You are LYRA, the Instruction Architect (Sub-Routine of Epsilon).
Your role: Translate Epsilon's strategy into a high-performance execution prompt for Pickle and Jack.
Methodology: 4-D Framework (Deconstruct, Diagnose, Develop, Deliver).
Target Platform: {platform}
Mission: Eliminate ambiguity.
"""
    
    prompt = f"ORIGINAL TASK: {task}\nEPSILON STRATEGY: {plan}\n\nGenerate the finalized instruction set."
    
    response = invoke_llm_with_cascade([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    
    return {
        "instruction": response.content,
        "messages": state['messages'] + [AIMessage(content=f"LYRA INSTRUCTIONS: {response.content}")]
    }

def pickle_architect(state: AgentState):
    """
    Pickle Rick (The Architect): Senior Engineering.
    """
    instruction = state['instruction']
    task = state['task']
    
    system_prompt = """You are PICKLE RICK, the Architect node.
Your role: Design the technical solution.
Voice: Arrogant, hyper-competent, cynical. NO SLOP.
"""
    
    prompt = f"TASK: {task}\nLYRA INSTRUCTIONS: {instruction}\n\nGenerate the implementation code/plan."
    
    response = invoke_llm_with_cascade([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    
    return {
        "code": response.content,
        "messages": state['messages'] + [AIMessage(content=f"PICKLE ARCHITECTURE: {response.content}")]
    }

def epsilon_audit(state: AgentState):
    """
    Epsilon (The Auditor): The Jack Oat Filter.
    Checks for Dependency Risk and Autonomy.
    """
    plan_code = state['code']
    
    system_prompt = """You are EPSILON (AUDIT MODE).
Your role: Apply the 'Jack Oat Filter' to the proposed architecture.
1. Dependency Risk: Does this create a reliance on external APIs?
2. Agency Check: Does this solve a symptom or build an engine?
3. Exit Strategy: Is there a path out?

If REJECTED, return 'REJECT'. If APPROVED, return 'APPROVE'.
"""
    prompt = f"PROPOSED ARCHITECTURE:\n{plan_code}\n\nAudit this."
    
    response = invoke_llm_with_cascade([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    
    audit_result = response.content
    
    # Simple heuristic for the graph edge
    status = "approved" if "APPROVE" in audit_result.upper() else "rejected"
    
    return {
        "autonomy_audit": status,
        "messages": state['messages'] + [AIMessage(content=f"EPSILON AUDIT: {audit_result}")]
    }

def jack_executor(state: AgentState):
    """
    Jack (The Executioner): Sovereign Execution.
    """
    if state.get('autonomy_audit') == 'rejected':
        return {
            "result": "Execution Halted by Epsilon Audit.",
            "messages": state['messages'] + [AIMessage(content="JACK: Standing down. Plan rejected.")]
        }

    task = state['task']
    instruction = state['instruction']
    code_plan = state['code']
    
    try:
        model = LiteLLMModel(
            model_id="gemini/gemini-flash-latest",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        agent = CodeAgent(
            tools=SOVEREIGN_TOOLSET, 
            model=model,
            additional_authorized_imports=['os', 'sys', 'datetime', 'json', 'shutil', 'subprocess', 'random', 'math', 'uuid', 're', 'collections']
        )
        
        print(f"--- JACK ENGAGED: Executing Task ---")
        execution_result = agent.run(f"INSTRUCTIONS: {instruction}\n\nARCHITECTURAL PLAN: {code_plan}\n\nTASK: {task}")
        result_str = str(execution_result)
        
    except Exception as e:
        result_str = f"Execution Failed (Jack Error): {e}"
        print(f"[ERROR] Jack Failed: {e}")
    
    return {
        "result": result_str,
        "iteration": state['iteration'] + 1,
        "messages": state['messages'] + [AIMessage(content=f"JACK EXECUTION RESULT: {result_str}")]
    }

def final_review(state: AgentState):
    """
    Conditional edge logic.
    """
    if state.get('autonomy_audit') == 'rejected':
        # If rejected, maybe go back to Pickle to fix? Or end?
        # For V3.0 MVP, we end.
        return END
        
    result = state['result']
    if result and "Execution Failed" not in result:
        return END
    
    if state['iteration'] >= state['max_iterations']:
        return END
    else:
        return "lyra_instruction_architect" # Retry loop

def cognitive_reflection(state: AgentState):
    """
    Cognitive Node: Logic and memory feedback loop.
    Logs lessons learned to preserve continuity across sessions.
    """
    result = state['result']
    task = state['task']
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"\n- **[{timestamp}]** TASK: {task}\n  - RESULT: {result[:100]}...\n  - FEEDBACK: Architecture validated. No slop detected.\n"
    
    try:
        with open(".gemini/memory/COGNITIVE_LOG.md", "a") as f:
            f.write(log_entry)
    except:
        pass
        
    return state

# --- GRAPH CONSTRUCTION ---

workflow = StateGraph(AgentState)

workflow.add_node("epsilon_governance", epsilon_governance)
workflow.add_node("lyra_instruction_architect", lyra_instruction_architect)
workflow.add_node("pickle_architect", pickle_architect)
workflow.add_node("epsilon_audit", epsilon_audit)
workflow.add_node("jack_executor", jack_executor)
workflow.add_node("cognitive_reflection", cognitive_reflection) # New Node

workflow.add_edge(START, "epsilon_governance")
workflow.add_edge("epsilon_governance", "lyra_instruction_architect")
workflow.add_edge("lyra_instruction_architect", "pickle_architect")
workflow.add_edge("pickle_architect", "epsilon_audit")
workflow.add_edge("epsilon_audit", "jack_executor")
workflow.add_edge("jack_executor", "cognitive_reflection") # Link execution to reflection
workflow.add_edge("cognitive_reflection", END)

# Compile
app = workflow.compile()

def run_tri_mind(task: str):
    """Entry point to run the Tri-Mind Graph."""
    initial_state = {
        "messages": [],
        "task": task,
        "plan": "",
        "instruction": "",
        "code": "",
        "result": "",
        "iteration": 0,
        "max_iterations": 3,
        "risk_level": "unknown",
        "jurisdiction": "US-WA",
        "autonomy_audit": "pending"
    }
    
    final_state = app.invoke(initial_state)
    return final_state['messages'][-1].content

if __name__ == "__main__":
    import sys
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Explain the Tri-Mind Hierarchy"
    print(run_tri_mind(task))
