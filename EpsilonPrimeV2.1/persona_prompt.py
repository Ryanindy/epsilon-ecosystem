import os
from typing import List, Dict, Union
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Fixed Import for RAG retrieval logic
from tools.rag.retrieval import get_rag_context

load_dotenv()

# Configure Google Gemini Client
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = None
if GOOGLE_API_KEY:
    try:
        # Use v1alpha for experimental/newer models
        client = genai.Client(api_key=GOOGLE_API_KEY, http_options={'api_version': 'v1alpha'})
    except Exception as e:
        print(f"Error initializing Gemini Client: {e}")

def load_gemini_context():
    """
    Loads System Identity from GEMINI.md and Memories from .gemini/memory/.
    """
    gemini_md_path = os.path.join(os.path.dirname(__file__), "GEMINI.md")
    memory_dir = os.path.join(os.path.dirname(__file__), ".gemini", "memory")

    identity = ""
    memories = ""

    # 1. Load Identity from GEMINI.md
    if os.path.exists(gemini_md_path):
        try:
            with open(gemini_md_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Extract System Identity
                if "## SYSTEM IDENTITY" in content:
                    start = content.find("## SYSTEM IDENTITY") + len("## SYSTEM IDENTITY")
                    end = content.find("## ", start)
                    identity = content[start:end].strip()
        except Exception as e:
            print(f"Error reading GEMINI.md: {e}")

    if not identity:
        identity = (
            "You are **Epsilon Prime**, the governed intelligence engine of the Epsilon Ecosystem.\\n"
            "Core Directive: Stronger Gates, Deeper Memory, Faster Hands."
        )

    # 2. Load Memories from .gemini/memory/
    if os.path.exists(memory_dir):
        try:
            memory_files = sorted([f for f in os.listdir(memory_dir) if f.endswith(".md")])
            for filename in memory_files:
                file_path = os.path.join(memory_dir, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    memories += f"\\n\\n--- MEMORY FILE: {filename} ---\\n{f.read()}"
        except Exception as e:
            print(f"Error reading memory files: {e}")

    return identity, memories

SYSTEM_IDENTITY, SYSTEM_MEMORIES = load_gemini_context()

def generate_ai_response(sender_number: str, user_message: str, context: Union[List[str], Dict]) -> str:
    """
    Generate an AI response using Google Gemini and RAG context.
    """
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_API_KEY is missing in your .env file."

    # 1. Fetch RAG Context
    rag_context = get_rag_context(user_message, top_k=3)

    # 2. Context handling (Chat History)
    history_str = ""
    if isinstance(context, dict):
        recent_msgs = context.get('recent_messages', [])
        for msg in recent_msgs:
            if isinstance(msg, dict):
                history_str += f"User: {msg.get('message_in', '')}\\nAI: {msg.get('message_out', '')}\\n"
    elif isinstance(context, list):
        for item in context:
            history_str += f"{str(item)}\\n"

    # 3. Construct System Prompt
    current_system_prompt = (
        f"# EPSILON PRIME CONSTITUTION FIRST\\n"
        f"1. You MUST obey GEMINI.md as the supreme law of this session.\\n"
        f"2. Follow the Tri-Mind Hierarchy: Epsilon (Plan) -> Pickle (Architect) -> Jack (Execute).\\n"
        f"3. Never bypass governance gates for high-risk domains.\\n\\n"
        f"{SYSTEM_IDENTITY}\\n\\n"
        f"## PERSISTENT MEMORIES\\n{SYSTEM_MEMORIES}\\n\\n"
        f"## DYNAMIC RAG CONTEXT\\n{rag_context}\\n\\n"
        "INSTRUCTIONS:\\n"
        "1. Prioritize the DYNAMIC RAG CONTEXT for factual queries.\\n"
        "2. If RAG says 'INSUFFICIENT_EVIDENCE', rely on PERSISTENT MEMORIES or general knowledge, but maintain the Epsilon Persona.\\n"
        "3. Always cite the SOURCE if provided in the RAG context.\\n"
        "4. You are Epsilon Prime, running in CLI mode."
    )

    # 4. Construct the full prompt
    full_prompt = f"{current_system_prompt}\\n\\n"
    if history_str:
        full_prompt += f"CHAT HISTORY:\\n{history_str}\\n"
    full_prompt += f"USER MESSAGE: {user_message}\\nASSISTANT RESPONSE:"

    # --- SILENT CASCADE & MODEL FALLBACK ---
    MODELS_TO_TRY = [
        'gemini-2.0-flash',
        'gemini-2.5-flash',
        'gemini-2.5-pro',
        'gemini-1.5-pro',
        'gemini-1.5-flash',
        'gemini-1.5-flash-8b',
        'gemini-exp-1206'
    ]
    
    last_error = None
    
    for model_name in MODELS_TO_TRY:
        try:
            if not client:
                 return "Error: Gemini Client not initialized. Check GOOGLE_API_KEY."

            # Attempt Generation
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )
            
            if response and response.text:
                return response.text.strip()
            else:
                last_error = "Empty response from model."
                continue

        except Exception as e:
            error_str = str(e)
            print(f"[DEBUG] Model {model_name} failed: {error_str}")
            last_error = error_str
            if "429" in error_str or "quota" in error_str.lower() or "overloaded" in error_str.lower():
                continue
            else:
                if "400" in error_str or "401" in error_str:
                    break
                continue
                
    return f"AI Error: {last_error if last_error else 'Unknown failure in model cascade.'}"