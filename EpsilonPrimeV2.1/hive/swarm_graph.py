"""
Sovereign Swarm Graph: Multi-Agent Orchestration Engine
Version: 6.0 (Recursive Cognitive Loop - OSINT Optimized)
"""
import os
import json
import sys
import logging
import re
from typing import TypedDict, List, Dict, Union, Annotated, Optional
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel

# --- PROJECT ROOT ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from tools.sovereign_tools import SOVEREIGN_TOOLSET, CODER_TOOLSET, RESEARCHER_TOOLSET
from tools.osint_tools import OSINT_TOOLSET
from tools.rag.retrieval import get_rag_context

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] Swarm: %(message)s')
logger = logging.getLogger("SovereignSwarm")

# --- CONFIG ---
HIVE_AGENTS_PATH = os.path.join(PROJECT_ROOT, "hive", "agents")
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".gemini", "skills")
MODELS_TO_TRY = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-2.5-pro']

# --- REGISTRIES ---
class SwarmManager:
    def __init__(self):
        self.agents = {}
        self.skills = {}
        self.load_all()

    def load_all(self):
        # Load Agents
        for f in os.listdir(HIVE_AGENTS_PATH):
            if f.endswith(".json"):
                with open(os.path.join(HIVE_AGENTS_PATH, f), 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.agents[data['id']] = data
        
        # Load Skills
        for f in os.listdir(SKILLS_DIR):
            if f.endswith(".md"):
                with open(os.path.join(SKILLS_DIR, f), 'r', encoding='utf-8') as file:
                    content = file.read()
                    name_match = re.search(r"name:\s*(.*)", content)
                    name = name_match.group(1).strip() if name_match else f.replace(".md", "")
                    self.skills[name] = content

    def get_relevant_skills(self, task: str, limit=3):
        scored = []
        for name, content in self.skills.items():
            score = 10 if name.lower() in task.lower() else 0
            score += len(re.findall(re.escape(name), content, re.I))
            if score > 0: scored.append((score, name, content))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:limit]

swarm_registry = SwarmManager()

# --- STATE DEFINITION ---
class SwarmState(TypedDict):
    messages: Annotated[List[BaseMessage], "History"]
    task: str
    current_subtask: str
    strategy: str # Epsilon's high-level directive
    shared_data: Dict # The Blackboard
    pending_vectors: List[str] # Discovered but not yet searched
    searched_vectors: List[str] # Already processed
    recursion_depth: int
    active_agent: str
    iteration: int
    max_iterations: int
    audit_status: str # 'approved', 'rejected', 'pending'
    hydrated_skills: str
    final_result: str

# --- LLM UTILITY ---
def call_llm(messages: List[BaseMessage]):
    """Enforces T1_MODEL_FAILOVER Protocol."""
    for model in MODELS_TO_TRY:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model, 
                google_api_key=os.getenv("GOOGLE_API_KEY"), 
                timeout=60,
                max_retries=0 
            )
            return llm.invoke(messages)
        except Exception as e:
            err_str = str(e)
            if "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
                logger.warning(f"[FAILOVER] Model {model} exhausted. Switching...")
                continue
            logger.error(f"[LLM] {model} failed: {e}")
            continue
    raise RuntimeError("Swarm Uplink Failed: All models in stack exhausted.")

# --- VECTOR EXTRACTION ---
def extract_vectors(text: str) -> List[str]:
    # Identify potential OSINT vectors: Emails, Phones, Usernames
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    phones = re.findall(r'\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}', text)
    usernames = re.findall(r'@(\w{3,})', text)
    return list(set(emails + phones + usernames))

# --- NODES ---

def skill_hydrator(state: SwarmState):
    relevant = swarm_registry.get_relevant_skills(state['task'])
    injected = "### SPECIALIZED TRAINING\n"
    for s, name, content in relevant:
        injected += f"--- {name} ---\n{content}\n\n"
    return {"hydrated_skills": injected}

def governor_strategy(state: SwarmState):
    """EPSILON: Defines the 'Why' and constraints."""
    if state['strategy']: return state # Don't re-strategize in the loop unless needed
    
    rag = get_rag_context(state['task'], top_k=3)
    sys_prompt = f"You are EPSILON, the Governor. Define the strategic constraints and the 'Smallest Truthful Action'.\n\n{state['hydrated_skills']}\n\nRAG:\n{rag}"
    resp = call_llm([SystemMessage(content=sys_prompt), HumanMessage(content=state['task'])])
    
    # Initial vector extraction from task
    initial_vectors = extract_vectors(state['task'])
    
    return {
        "strategy": resp.content, 
        "pending_vectors": initial_vectors,
        "messages": state['messages'] + [AIMessage(content=f"GOVERNOR STRATEGY: {resp.content}")]
    }

def supervisor_router(state: SwarmState):
    """LYRA: Decides which agent handles the next phase or vector."""
    
    # Check for recursion/vector exhaustion
    if not state['current_subtask']:
        if state['pending_vectors']:
            next_vector = state['pending_vectors'][0]
            logger.info(f"[SUPERVISOR] Picking up new vector: {next_vector}")
            return {
                "current_subtask": f"OSINT Search on vector: {next_vector}",
                "pending_vectors": state['pending_vectors'][1:],
                "searched_vectors": state['searched_vectors'] + [next_vector],
                "recursion_depth": state['recursion_depth'] + 1
            }
        elif state['recursion_depth'] > 0:
            logger.info("[SUPERVISOR] All vectors exhausted. Finalizing.")
            return {"active_agent": "finalize"}

    agent_list = "\n".join([f"- {id}: {a['role']} (Tools: {a['tools']})" for id, a in swarm_registry.agents.items()])
    sys_prompt = f"""You are LYRA, the Swarm Supervisor. Based on the Governor's strategy and current subtask, select the next agent.
    
Available Agents:
{agent_list}

RULES:
1. 'agent-sherlock' is for username searches.
2. 'agent-holmes' is for deep person/phone/email lookups.
3. 'agent-footprint' is for spiderfoot mapping.
4. 'agent-harvester' is for domain/email harvesting.
5. 'agent-web' is for manual website verification/scraping.
6. 'coder-rick' is for code/design.
7. 'eric-assistant' is for comms.

Respond with ONLY the Agent ID. If current subtask is finished, respond 'FINALIZE'."""
    
    prompt = f"""TASK: {state['task']}
SUBTASK: {state['current_subtask']}
STRATEGY: {state['strategy']}
BLACKBOARD: {json.dumps(state['shared_data'])}

Who acts next?"""
    resp = call_llm([SystemMessage(content=sys_prompt), HumanMessage(content=prompt)])
    selection = resp.content.strip().lower().replace("'", "").replace('"', '')
    
    if 'finalize' in selection.upper(): 
        return {"active_agent": "finalize", "current_subtask": ""}
    
    if selection not in swarm_registry.agents: selection = "agent-web" # Default
    
    return {"active_agent": selection}

def worker_node(state: SwarmState):
    """Executes specialized agent tools and extracts new vectors."""
    agent_id = state['active_agent']
    if agent_id == "finalize": return state
    
    agent_def = swarm_registry.agents[agent_id]
    logger.info(f"[WORKER] {agent_id} engaging on '{state['current_subtask']}'...")
    
    # Load Persona
    persona = ""
    persona_path = os.path.join(PROJECT_ROOT, agent_def.get('persona', ''))
    if os.path.exists(persona_path):
        with open(persona_path, 'r', encoding='utf-8') as f:
            persona = f.read()

    # Tool Selection
    toolsets = {
        "coder-rick": CODER_TOOLSET,
        "agent-sherlock": OSINT_TOOLSET,
        "agent-footprint": OSINT_TOOLSET,
        "agent-harvester": OSINT_TOOLSET,
        "agent-holmes": OSINT_TOOLSET,
        "agent-web": RESEARCHER_TOOLSET + OSINT_TOOLSET,
        "researcher-lyra": RESEARCHER_TOOLSET,
        "eric-assistant": SOVEREIGN_TOOLSET
    }
    
    try:
        model = LiteLLMModel(model_id="gemini/gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))
        agent = CodeAgent(
            tools=toolsets.get(agent_id, SOVEREIGN_TOOLSET),
            model=model,
            additional_authorized_imports=['os', 'sys', 'json', 're', 'datetime', 'math']
        )
        
        exec_prompt = f"""IDENTITY: {agent_def['name']}
ROLE: {agent_def['role']}
PERSONA:
{persona}

STRATEGY: {state['strategy']}
SUBTASK: {state['current_subtask']}
BLACKBOARD: {json.dumps(state['shared_data'])}

INSTRUCTIONS:
1. fulfill your role for the current subtask.
2. Update the Blackboard with results.
3. Format: [UPDATE_BLACKBOARD] {{"key": "value"}} [RESULT] your_summary"""
        
        result = str(agent.run(exec_prompt))
        
        # Vector Extraction from worker result
        new_found = extract_vectors(result)
        pending = list(state['pending_vectors'])
        for v in new_found:
            if v not in state['searched_vectors'] and v not in pending:
                logger.info(f"[COGNITIVE_LOOP] Discovered new vector: {v}")
                pending.append(v)

        # Extract Blackboard updates
        updates = {}
        match = re.search(r"\[UPDATE_BLACKBOARD\]\s*(\{.*?\})", result)
        if match:
            try: updates = json.loads(match.group(1))
            except: pass
            
        new_shared = state['shared_data'].copy()
        new_shared.update(updates)
        
        return {
            "shared_data": new_shared,
            "pending_vectors": pending,
            "iteration": state['iteration'] + 1,
            "messages": state['messages'] + [AIMessage(content=f"WORKER ({agent_id}): {result}")]
        }
    except Exception as e:
        logger.error(f"Worker {agent_id} failed: {e}")
        return {"iteration": state['iteration'] + 1}

def governor_audit(state: SwarmState):
    """EPSILON: Final check."""
    if state['active_agent'] != "finalize": return {"audit_status": "pending"}
    
    sys_prompt = "You are EPSILON (AUDIT). Review the final blackboard state. Does it meet Sovereign criteria? Respond 'APPROVE' or 'REJECT' + reasoning."
    prompt = f"TASK: {state['task']}\nBLACKBOARD: {json.dumps(state['shared_data'])}\nPerform Audit."
    resp = call_llm([SystemMessage(content=sys_prompt), HumanMessage(content=prompt)])
    
    status = "approved" if "APPROVE" in resp.content.upper() else "rejected"
    return {"audit_status": status, "messages": state['messages'] + [AIMessage(content=f"GOVERNOR AUDIT: {resp.content}")]}

def executor_jack(state: SwarmState):
    """JACK: Enactment."""
    if state['audit_status'] != 'approved': 
        return {"final_result": f"Halted: Audit Failure. {state['messages'][-1].content}"}
    
    logger.info("[JACK] Finalizing report...")
    try:
        model = LiteLLMModel(model_id="gemini/gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY"))
        agent = CodeAgent(tools=OSINT_TOOLSET + SOVEREIGN_TOOLSET, model=model)
        
        exec_prompt = f"TASK: {state['task']}\nBLACKBOARD: {json.dumps(state['shared_data'])}\nFinalize the Markdown OSINT report."
        result = str(agent.run(exec_prompt))
        return {"final_result": result}
    except Exception as e:
        return {"final_result": f"Execution Error: {e}"}

# --- GRAPH CONSTRUCTION ---
builder = StateGraph(SwarmState)

builder.add_node("skill_hydrator", skill_hydrator)
builder.add_node("governor_strategy", governor_strategy)
builder.add_node("supervisor", supervisor_router)
builder.add_node("worker", worker_node)
builder.add_node("governor_audit", governor_audit)
builder.add_node("executor", executor_jack)

builder.add_edge(START, "skill_hydrator")
builder.add_edge("skill_hydrator", "governor_strategy")
builder.add_edge("governor_strategy", "supervisor")

def supervisor_logic(state: SwarmState):
    if state['active_agent'] == "finalize": return "governor_audit"
    if state['iteration'] >= state['max_iterations'] or state['recursion_depth'] >= 5: 
        return "governor_audit"
    return "worker"

builder.add_conditional_edges("supervisor", supervisor_logic, {"worker": "worker", "governor_audit": "governor_audit"})
builder.add_edge("worker", "supervisor")
builder.add_edge("governor_audit", "executor")
builder.add_edge("executor", END)

app = builder.compile()

def run_swarm(task: str):
    initial = {
        "messages": [], "task": task, "current_subtask": "", "strategy": "", 
        "shared_data": {}, "pending_vectors": [], "searched_vectors": [],
        "recursion_depth": 0, "active_agent": "", "iteration": 0, "max_iterations": 15, 
        "audit_status": "pending", "hydrated_skills": "", "final_result": ""
    }
    try:
        final = app.invoke(initial)
        return final.get('final_result', "Process Ended without result.")
    except Exception as e:
        return f"Swarm Error: {e}"

if __name__ == "__main__":
    t = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Audit system status."
    print(run_swarm(t))
