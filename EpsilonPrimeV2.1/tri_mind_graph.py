"""
Tri-Mind Graph: Sovereign Multi-Agent Orchestration Engine
Version: 4.1 (Deep Skill Hydration)
"""
import os
import time
import json
import sys
import logging
import re
from typing import TypedDict, List, Dict, Union, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel

# --- PROJECT ROOT CONFIGURATION ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from tools.sovereign_tools import SOVEREIGN_TOOLSET, CODER_TOOLSET, RESEARCHER_TOOLSET
from tools.rag.retrieval import get_rag_context
from hive.swarm_graph import run_swarm

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("TriMind")

# --- HIVE MIND CONFIG (ABSOLUTE PATHS) ---
HIVE_AGENTS_PATH = os.path.join(PROJECT_ROOT, "hive", "agents")
AGENT_REGISTRY = {}
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".gemini", "skills")

# --- LLM CONFIGURATION ---
MODELS_TO_TRY = ['gemini-2.0-flash', 'gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-1.5-flash']
LLM_TIMEOUT_SECONDS = 60

# --- SKILL REGISTRY & HYDRATOR ---
class SkillManager:
    def __init__(self, directory):
        self.directory = directory
        self.skills = {}
        self.load_skills()

    def load_skills(self):
        if not os.path.exists(self.directory):
            return
        for f in os.listdir(self.directory):
            if f.endswith(".md"):
                path = os.path.join(self.directory, f)
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        # Extract name from frontmatter or filename
                        name_match = re.search(r"name:\s*(.*)", content)
                        name = name_match.group(1).strip() if name_match else f.replace(".md", "")
                        self.skills[name] = {
                            "path": path,
                            "content": content,
                            "summary": content[:200].replace("\n", " ") + "..."
                        }
                except Exception as e:
                    logger.error(f"Failed to load skill {f}: {e}")

    def get_relevant_skills(self, task: str, limit=3):
        """Simple keyword matching for skill selection."""
        scored_skills = []
        task_lower = task.lower()
        for name, data in self.skills.items():
            score = 0
            if name.lower() in task_lower: score += 10
            # Basic keyword matches
            keywords = re.findall(r"\w+", task_lower)
            for kw in keywords:
                if kw in data['content'].lower(): score += 1
            if score > 0:
                scored_skills.append((score, name, data))
        
        scored_skills.sort(key=lambda x: x[0], reverse=True)
        return scored_skills[:limit]

    def get_manifest(self):
        return "\n".join([f"- {name}" for name in self.skills.keys()])

skill_manager = SkillManager(SKILLS_DIR)

def load_hive_agents():
    """Scans and loads agent definitions from the hive directory."""
    global AGENT_REGISTRY
    try:
        if not os.path.exists(HIVE_AGENTS_PATH):
            return
        for file_name in os.listdir(HIVE_AGENTS_PATH):
            if file_name.endswith(".json"):
                file_path = os.path.join(HIVE_AGENTS_PATH, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    agent_def = json.load(f)
                    AGENT_REGISTRY[agent_def['id']] = agent_def
    except Exception as e:
        logger.error(f"[HIVE] CRITICAL: Could not load agents: {e}")

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "Conversation history"]
    task: str
    plan: str
    instruction: str
    code: str
    result: str
    iteration: int
    max_iterations: int
    selected_agent: str
    agent_tools: List
    risk_level: str
    autonomy_audit: str
    hydrated_skills: str # New field for injected skill content

# --- TOOL MAPPING ---
TOOL_MAP = {
    "coder-rick": CODER_TOOLSET,
    "researcher-lyra": RESEARCHER_TOOLSET,
    "default": SOVEREIGN_TOOLSET
}

def invoke_llm_with_cascade(messages: List[BaseMessage], timeout: int = LLM_TIMEOUT_SECONDS):
    """Enforces T1_MODEL_FAILOVER Protocol."""
    for model_name in MODELS_TO_TRY:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model_name, 
                google_api_key=os.getenv("GOOGLE_API_KEY"), 
                timeout=timeout,
                max_retries=0
            )
            return llm.invoke(messages)
        except Exception as e:
            err_str = str(e)
            if "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
                logger.warning(f"[FAILOVER] Model {model_name} exhausted. Switching...")
                continue
            logger.error(f"[LLM] {model_name} failed: {e}")
            continue
    raise RuntimeError("Tri-Mind Uplink Failed: All models in stack exhausted.")

# --- NODES ---

def skill_hydrator(state: AgentState) -> dict:
    """Active Skill Injection Node."""
    task = state['task']
    relevant = skill_manager.get_relevant_skills(task)
    
    injected_text = "### ACTIVE SPECIALIZED TRAINING (HYDRATED)\n"
    if not relevant:
        injected_text += "No specific skill overrides triggered. Using core Sovereign protocols.\n"
    else:
        for score, name, data in relevant:
            logger.info(f"[HYDRATOR] Injecting skill: {name} (Score: {score})")
            injected_text += f"--- SKILL: {name} ---\n{data['content']}\n\n"
    
    injected_text += "\n### MASTER SKILL MANIFEST (AVAILABLE ARSENAL)\n"
    injected_text += skill_manager.get_manifest()
    
    return {"hydrated_skills": injected_text}

def epsilon_governance(state: AgentState) -> dict:
    task = state['task']
    hydrated = state.get('hydrated_skills', '')
    rag_context = get_rag_context(task, top_k=3)

    system_prompt = f"""You are EPSILON, the Sovereign Cortex.
Protocol: Truth-First, Internal Locus, Sovereign Action.

{hydrated}

RAG CONTEXT:
{rag_context}
"""
    prompt = f"TASK: {task}\n\nAnalyze risk and strategic alignment. Define the 'Smallest Truthful Action' (epsilon)."
    response = invoke_llm_with_cascade([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    
    risk_level = "low"
    if "high risk" in response.content.lower(): risk_level = "high"
    elif "medium risk" in response.content.lower(): risk_level = "medium"

    return {
        "plan": response.content,
        "risk_level": risk_level,
        "messages": state['messages'] + [AIMessage(content=f"EPSILON STRATEGY: {response.content}")]
    }

def lyra_instruction_architect(state: AgentState) -> dict:
    task = state['task']
    plan = state['plan']
    hydrated = state.get('hydrated_skills', '')
    
    system_prompt = f"""You are LYRA, the Instruction Architect.
Role: Translate strategy into a high-performance execution prompt.
Methodology: 4-D Framework.

{hydrated}
"""
    prompt = f"ORIGINAL TASK: {task}\nEPSILON STRATEGY: {plan}\n\nGenerate the finalized instruction set."
    response = invoke_llm_with_cascade([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    return {"instruction": response.content, "messages": state['messages'] + [AIMessage(content=f"LYRA INSTRUCTIONS: {response.content}")]}

def pickle_architect(state: AgentState) -> dict:
    instruction = state['instruction']
    task = state['task']
    hydrated = state.get('hydrated_skills', '')

    system_prompt = f"You are PICKLE RICK, the Architect. Design the technical solution.\n\n{hydrated}"
    prompt = f"TASK: {task}\nLYRA INSTRUCTIONS: {instruction}\n\nGenerate implementation code plan."
    response = invoke_llm_with_cascade([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    return {"code": response.content, "messages": state['messages'] + [AIMessage(content=f"PICKLE ARCHITECTURE: {response.content}")]}

def epsilon_audit(state: AgentState) -> dict:
    plan_code = state['code']
    if state.get('risk_level', 'low') == "low":
        return {"autonomy_audit": "approved"}

    system_prompt = "You are EPSILON (AUDIT MODE). Apply the Jack Oat Filter. Respond 'APPROVE' or 'REJECT'."
    prompt = f"PROPOSED ARCHITECTURE:\n{plan_code}"
    response = invoke_llm_with_cascade([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    return {"autonomy_audit": "approved" if "APPROVE" in response.content.upper() else "rejected", "messages": state['messages'] + [AIMessage(content=f"EPSILON AUDIT: {response.content}")]}

def agent_selector(state: AgentState) -> dict:
    instruction = state['instruction']
    agent_list = "- " + "\n- ".join([f"{k}: {v.get('role', 'N/A')}" for k, v in AGENT_REGISTRY.items()])
    system_prompt = f"Select best agent ID:\n{agent_list}"
    prompt = f"INSTRUCTION: {instruction}"
    response = invoke_llm_with_cascade([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    selected_id = response.content.strip().lower().replace("'", "").replace('"', '')
    if selected_id not in TOOL_MAP: selected_id = "default"
    return {"selected_agent": selected_id, "agent_tools": TOOL_MAP.get(selected_id, SOVEREIGN_TOOLSET)}

def jack_executor(state: AgentState) -> dict:
    if state.get('autonomy_audit') == 'rejected':
        return {"result": "Halted: Audit failure.", "messages": state['messages'] + [AIMessage(content="JACK: Standing down.")]}

    instruction = state['instruction']
    task = state['task']
    code_plan = state.get('code', '')
    tools_for_agent = state['agent_tools']

    try:
        model = LiteLLMModel(model_id="gemini/gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
        agent = CodeAgent(tools=tools_for_agent, model=model, additional_authorized_imports=['os', 'sys', 'datetime', 'json', 'shutil', 'subprocess', 'random', 'math', 'uuid', 're', 'collections'])
        execution_prompt = f"INSTRUCTIONS: {instruction}\n\nPLAN: {code_plan}\n\nTASK: {task}"
        result = agent.run(execution_prompt)
        result_str = str(result)
    except Exception as e:
        result_str = f"Jack Error: {e}"

    return {"result": result_str, "iteration": state['iteration'] + 1, "messages": state['messages'] + [AIMessage(content=f"JACK EXECUTION RESULT: {result_str}")]}

def final_review(state: AgentState) -> str:
    if state.get('autonomy_audit') == 'rejected' or "Jack Error" not in state.get('result', '') or state['iteration'] >= state['max_iterations']:
        return END
    return "agent_selector"

workflow = StateGraph(AgentState)
workflow.add_node("skill_hydrator", skill_hydrator)
workflow.add_node("epsilon_governance", epsilon_governance)
workflow.add_node("lyra_instruction_architect", lyra_instruction_architect)
workflow.add_node("pickle_architect", pickle_architect)
workflow.add_node("epsilon_audit", epsilon_audit)
workflow.add_node("agent_selector", agent_selector)
workflow.add_node("jack_executor", jack_executor)

workflow.add_edge(START, "skill_hydrator")
workflow.add_edge("skill_hydrator", "epsilon_governance")
workflow.add_edge("epsilon_governance", "lyra_instruction_architect")
workflow.add_edge("lyra_instruction_architect", "pickle_architect")
workflow.add_edge("pickle_architect", "epsilon_audit")
workflow.add_edge("epsilon_audit", "agent_selector")
workflow.add_edge("agent_selector", "jack_executor")
workflow.add_conditional_edges("jack_executor", final_review, {END: END, "agent_selector": "agent_selector"})

app = workflow.compile()

def run_tri_mind(task: str) -> str:
    if task.lower().startswith("swarm "):
        swarm_task = task[6:].strip()
        logger.info(f"[ROUTING] Diverting to Sovereign Swarm V5.0: {swarm_task}")
        return run_swarm(swarm_task)

    if not AGENT_REGISTRY: load_hive_agents()
    initial_state = {"messages": [], "task": task, "plan": "", "instruction": "", "code": "", "result": "", "iteration": 0, "max_iterations": 3, "selected_agent": "default", "agent_tools": SOVEREIGN_TOOLSET, "risk_level": "low", "autonomy_audit": "pending", "hydrated_skills": ""}
    try:
        final_state = app.invoke(initial_state)
        return final_state['messages'][-1].content
    except Exception as e:
        return f"Tri-Mind Error: {e}"

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Status check."
    print(run_tri_mind(task))
