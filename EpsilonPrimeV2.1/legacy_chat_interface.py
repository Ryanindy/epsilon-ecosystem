import os
import sys
import threading
import time

# Ensure we can import from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from sms_handler import generate_ai_response, fetch_client_context

load_dotenv()

# Configuration
INACTIVITY_LIMIT = 900  # 15 minutes in seconds
sender_id = "CLI_USER"

# Global State
last_activity = time.time()
is_running = True

def consolidation_monitor():
    """Background thread to monitor inactivity."""
    global last_activity, is_running
    
    while is_running:
        time.sleep(10) # Check every 10 seconds
        
        if time.time() - last_activity > INACTIVITY_LIMIT:
            print("\n\n[SYSTEM]: âš ï¸ Inactivity Detected (15m). Auto-Consolidating Session...")
            
            try:
                # Trigger the consolidation
                context = fetch_client_context(sender_id)
                prompt = "SYSTEM_TRIGGER: The user has been inactive for 15 minutes. Please run the 'session_consolidator' skill immediately to summarize and save this session's key learnings to the RAG. Output the filename saved."
                
                response = generate_ai_response(sender_id, prompt, context)
                print(f"\n[AUTO-CONSOLIDATOR]: {response}\n")
                print("You: ", end="", flush=True) # Restore prompt
                
                # Reset activity to prevent loop
                last_activity = time.time()
                
            except Exception as e:
                print(f"\n[SYSTEM]: Auto-consolidation failed: {e}")

def chat():
    global last_activity, is_running
    
    print("\n" + "="*50)
    print("⚡ EPSILON PRIME - SOVEREIGN TERMINAL v2.1 ⚡")
    print("==========================================")
    print(f"STATUS: OPERATIONAL | MODE: YOLO | GOD MODE: ACTIVE")
    print(f"AUTO-CONSOLIDATION: {INACTIVITY_LIMIT}s")
    print("Type 'exit' or 'q' to quit.")
    print("="*50 + "\n")
    
    # Start Monitor Thread
    monitor_thread = threading.Thread(target=consolidation_monitor, daemon=True)
    monitor_thread.start()
    
    while True:
        try:
            # Blocking input (but thread runs in background)
            user_input = input("ε′ 〉").strip()
            
            # Reset Activity Timer
            last_activity = time.time()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye.")
                is_running = False
                break

            if user_input.upper() == "OMEGA":
                print("\n[SYSTEM]: Triggering OMEGA PROTOCOL...")
                os.system(f"{sys.executable} tools/maintenance/stasis_protocol.py")
                is_running = False
                break
            
            # Fetch context
            context = fetch_client_context(sender_id)
            
            # Generate response
            print("\nThinking...", end="\r")
            response = generate_ai_response(sender_id, user_input, context)
            
            # Print response
            print(f"AI: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye.")
            is_running = False
            break
        except Exception as e:
            print(f"\n[Error]: {e}")
            is_running = False
            break

if __name__ == "__main__":
    chat()

