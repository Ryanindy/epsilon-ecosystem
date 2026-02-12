"""
main.py: Flask application entry point for the Provider Assistant.
Supports both API Server mode and CLI mode.
"""
import os
import time
import uuid
import sys

from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# ... (keep existing imports) ...

@app.route("/", methods=["GET"])
def index():
    """Serves the Sovereign Portal UI."""
    return render_template("index.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Alias for index."""
    return render_template("index.html")

@app.route("/sms", methods=["POST"])
def sms_endpoint():
    """
    Twilio webhook endpoint for incoming SMS messages.
    NOTE: In production, use Twilio signature validation.
    For internal/YOLO use, we check for a simple bypass or key.
    """
    # Simple check for demo/dev safety
    if not request.values.get("AccountSid") and not check_auth():
         return jsonify({"error": "Unauthorized"}), 401
         
    sender_number = request.values.get("From", "")
    message_body = request.values.get("Body", "")
    return handle_incoming_sms(sender_number, message_body)

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    """
    OpenAI-compatible endpoint for Local LLM tools.
    """
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    messages = data.get("messages", [])
    
    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    # Extract the latest user message
    last_user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    
    # Use a dummy number for API chats or extract from context if available
    sender_number = "API_USER"
    
    # Mode Selection: Default vs Sovereign (LangGraph)
    mode = data.get("mode", "default")
    
    try:
        if mode == "sovereign":
            response_text = run_tri_mind(last_user_message)
        else:
            context = fetch_client_context(sender_number)
            response_text = generate_ai_response(sender_number, last_user_message, context)
    except Exception as e:
        response_text = f"Error generating response: {str(e)}"

    # Construct OpenAI-style response
    return jsonify({
        "id": f"chatcmpl-{str(uuid.uuid4())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": data.get("model", "provider-assistant"),
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response_text
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(last_user_message),
            "completion_tokens": len(response_text),
            "total_tokens": len(last_user_message) + len(response_text)
        }
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return "OK", 200

if __name__ == "__main__":
    # Dual Mode: CLI or Server
    if len(sys.argv) > 1:
        # CLI Mode: Process arguments as a prompt
        prompt = " ".join(sys.argv[1:])
        sender_number = "CLI_USER"
        try:
            response = handle_incoming_sms(sender_number, prompt)
            print(response)
        except Exception as e:
            print(f"Error: {e}")
    else:
        # Server Mode: Start Flask
        port = int(os.getenv("PORT", 5000))
        debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
        # BIND TO LOCALHOST BY DEFAULT FOR SECURITY
        app.run(host="127.0.0.1", port=port, debug=debug_mode)