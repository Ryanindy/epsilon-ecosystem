"""
main.py: Flask application entry point for the Provider Assistant.
Supports both API Server mode and CLI mode.
"""
import os
import time
import uuid
import sys
import glob
import socket
import logging

from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# --- PROJECT ROOT CONFIGURATION ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from sms_handler import handle_incoming_sms, generate_ai_response, fetch_client_context
from tri_mind_graph import run_tri_mind

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("EpsilonServer")

app = Flask(__name__, template_folder=os.path.join(PROJECT_ROOT, "templates"))

# Security: Bearer Token for API - NO DEFAULT KEY
API_KEY = os.getenv("EPSILON_API_KEY")
if not API_KEY:
    logger.warning("EPSILON_API_KEY not set! API authentication will fail.")

def check_auth():
    """Validates Bearer token authentication."""
    if not API_KEY:
        logger.error("AUTH FAILED: No API_KEY configured on server")
        return False
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False
    token = auth_header.split(" ")[1]
    return token == API_KEY

def check_port(port):
    try:
        print(f"CHECK_PORT: Attempting to check port {port}", file=sys.stderr)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex(('localhost', port))
            status = "LIVE" if result == 0 else "DOWN"
            print(f"CHECK_PORT: Port {port} status: {status} (Result: {result})", file=sys.stderr)
            return status
    except Exception as e:
        print(f"CHECK_PORT: ERROR checking port {port}: {e}", file=sys.stderr)
        return f"ERROR: {e}"

def get_latest_pickle_session():
    """Finds the most recent session directory for Pickle Rick."""
    try:
        sessions_dir = os.path.join(PROJECT_ROOT, ".gemini", "extensions", "pickle-rick", "sessions", "*")
        list_of_dirs = glob.glob(sessions_dir)
        if not list_of_dirs:
            return None
        latest_dir = max(list_of_dirs, key=os.path.getctime)
        return latest_dir
    except Exception as e:
        logger.error(f"Failed to get pickle session: {e}")
        return None

@app.route("/", methods=["GET"])
def index():
    """Serves the Sovereign Portal UI."""
    return render_template("index.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Alias for index."""
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def api_status():
    """Returns system status for the dashboard."""
    try:
        print("API_STATUS: Entered endpoint.", file=sys.stderr)
        
        services = {
            "n8n": check_port(5678),
            "openclaw": check_port(18789),
            "api_bridge": "LIVE"
        }
        print(f"API_STATUS: Service checks complete: {services}", file=sys.stderr)
        
        rag_path = os.path.join(PROJECT_ROOT, "rag", ".chromadb")
        rag_status = "ONLINE" if os.path.exists(rag_path) else "OFFLINE"
        logger.debug(f"RAG check complete: {rag_status}")

        god_mode_path = os.path.join(PROJECT_ROOT, ".gemini", "GOD_MODE_ACTIVE")
        god_mode_status = os.path.exists(god_mode_path)
        print(f"API_STATUS: God Mode check complete: {god_mode_status}", file=sys.stderr)

        response = {
            "services": services,
            "rag": rag_status,
            "god_mode": god_mode_status,
            "timestamp": time.time()
        }
        print("API_STATUS: Response prepared. Returning JSON.", file=sys.stderr)
        return jsonify(response)
    except Exception as e:
        print(f"API_STATUS: CRITICAL ERROR IN ENDPOINT: {e}", file=sys.stderr)
        return jsonify({"error": "Internal Server Error in api_status"}), 500

@app.route("/api/skills", methods=["GET"])
def api_skills():
    """Returns a list of all skills with their activation status."""
    skill_categories = {
        "tools": os.path.join(PROJECT_ROOT, "skills", "tools"),
        "governance": os.path.join(PROJECT_ROOT, "skills", "governance"),
        "personas": os.path.join(PROJECT_ROOT, "skills", "personas")
    }
    
    all_skills = []
    for category, path in skill_categories.items():
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.endswith(".md"):
                    name = f.replace(".skill.md", "").replace(".persona.md", "").replace(".md", "")
                    status = "ACTIVE" if category in ["tools", "governance"] else "LOAD ON DEMAND"
                    if category == "governance":
                        status = "ACTIVE (CORE)"
                    
                    all_skills.append({
                        "name": name,
                        "category": category,
                        "status": status
                    })
    
    return jsonify({"skills": sorted(all_skills, key=lambda x: x['name'])})

@app.route("/api/commands", methods=["GET"])
def api_commands():
    """Returns the primary operational command triggers."""
    triggers = [
        {"cmd": "STASIS", "desc": "Omega Protocol (Shutdown & Sync)"},
        {"cmd": "OMEGA", "desc": "Emergency Stop"},
        {"cmd": "WAKE UP", "desc": "Total Recall (Boot)"},
        {"cmd": "/sudo <action>", "desc": "Elevated Jack Mode"},
        {"cmd": "/rag <query>", "desc": "Vector Deep Search"},
        {"cmd": "/memory list", "desc": "View Episodic Memory"},
        {"cmd": "swarm <task>", "desc": "Launch Sovereign Swarm V5.0 Agents"},
        {"cmd": "epsilon --server", "desc": "Launch API Bridge"},
        {"cmd": "epsilon --sync", "desc": "Global Git/RAG Sync"},
        {"cmd": "epsilon --backup", "desc": "System Backup"}
    ]
    return jsonify({"commands": triggers})

@app.route("/api/tickets", methods=["GET"])
def api_tickets():
    """Returns a list of tickets from the latest session."""
    session_path = get_latest_pickle_session()
    if not session_path:
        return jsonify({"error": "No active session found"}), 404
    
    tickets_dir = os.path.join(session_path, "tickets")
    tickets = []
    if os.path.exists(tickets_dir):
        tickets = [t for t in os.listdir(tickets_dir) if t.endswith(".md")]
    return jsonify({"tickets": sorted(tickets), "session": session_path})

@app.route("/api/ticket", methods=["POST"])
def api_create_ticket():
    """Creates a new ticket in the latest session."""
    session_path = get_latest_pickle_session()
    if not session_path:
        return jsonify({"error": "No active session found"}), 404

    data = request.json
    title = data.get("title", "Untitled Ticket")
    content = data.get("content", "No details provided.")
    
    tickets_dir = os.path.join(session_path, "tickets")
    os.makedirs(tickets_dir, exist_ok=True)
    
    filename = "".join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join(tickets_dir, f"{filename.replace(' ', '_')}.md")
    
    ticket_content = f"# {title}\n\n{content}"
    
    with open(filepath, "w") as f:
        f.write(ticket_content)
        
    return jsonify({"success": True, "path": filepath})

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Handles chat messages from the Sovereign Portal."""
    data = request.json
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "Empty message"}), 400
    try:
        response = run_tri_mind(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sms", methods=["POST"])
def sms_endpoint():
    """
    Twilio webhook endpoint for incoming SMS messages.
    Requires either valid Twilio signature OR Bearer token auth.
    """
    # Check for Bearer token auth first (for internal/API use)
    if check_auth():
        pass  # Authorized via API key
    elif request.values.get("AccountSid"):
        # TODO: Add proper Twilio signature validation in production
        # For now, validate AccountSid matches expected value
        expected_sid = os.getenv("TWILIO_ACCOUNT_SID")
        if expected_sid and request.values.get("AccountSid") != expected_sid:
            logger.warning(f"SMS auth failed: Invalid AccountSid")
            return jsonify({"error": "Unauthorized"}), 401
    else:
        return jsonify({"error": "Unauthorized"}), 401

    sender_number = request.values.get("From", "")
    message_body = request.values.get("Body", "")
    return handle_incoming_sms(sender_number, message_body)

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    messages = data.get("messages", [])
    if not messages:
        return jsonify({"error": "No messages provided"}), 400
    last_user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    sender_number = "API_USER"
    mode = data.get("mode", "default")
    try:
        if mode == "sovereign":
            response_text = run_tri_mind(last_user_message)
        else:
            context = fetch_client_context(sender_number)
            response_text = generate_ai_response(sender_number, last_user_message, context)
    except Exception as e:
        response_text = f"Error generating response: {str(e)}"
    return jsonify({
        "id": f"chatcmpl-{str(uuid.uuid4())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": data.get("model", "provider-assistant"),
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": response_text},
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(last_user_message),
            "completion_tokens": len(response_text),
            "total_tokens": len(last_user_message) + len(response_text)
        }
    })

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        try:
            response = handle_incoming_sms("CLI_USER", prompt)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
    else:
        port = int(os.getenv("PORT", 5000))
        debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
        app.run(host="0.0.0.0", port=port, debug=debug_mode)
