import logging
import sqlite3
import os
from datetime import datetime
import persona_prompt

# Database Configuration
DB_PATH = "memory.db"

def init_db():
    """
    Initializes the SQLite database and creates the interactions table if it doesn't exist.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                sender TEXT,
                message_in TEXT,
                message_out TEXT,
                flagged BOOLEAN DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

# Initialize database on module load
init_db()

def run_safety_check(message):
    """
    Very basic safety check. High-risk keywords trigger a higher score.
    """
    risk_keywords = ["exploit", "hack", "illegal", "threat"]
    score = 0
    for word in risk_keywords:
        if word in message.lower():
            score += 2
    return score

def generate_ai_response(sender_number, message, context):
    """
    Calls the persona_prompt module to get a real AI response.
    """
    return persona_prompt.generate_ai_response(sender_number, message, context)

def log_interaction(sender, message, response, flagged=False):
    """
    Logs the interaction to the SQLite database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO interactions (sender, message_in, message_out, flagged) VALUES (?, ?, ?, ?)",
            (sender, message, response, 1 if flagged else 0)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error("Failed to log interaction: %s", e)

def fetch_client_context(sender):
    """
    Fetches the last 5 interactions for a given sender to provide context.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT message_in, message_out FROM interactions WHERE sender = ? ORDER BY timestamp DESC LIMIT 5",
            (sender,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        # Format for persona_prompt
        history = []
        for row in reversed(rows): # Oldest first for chronological order
            history.append({"message_in": row[0], "message_out": row[1]})
        
        return {"recent_messages": history}
    except Exception as e:
        logger.error("Failed to fetch client context: %s", e)
        return {"recent_messages": []}

logger = logging.getLogger(__name__)

def handle_incoming_sms(sender_number: str, message_body: str) -> str:
    """
    Process an inbound SMS and return the reply text.
    """
    logger.info("Received SMS from %s: %s", sender_number, message_body)

    try:
        context = fetch_client_context(sender_number)
        risk_score = run_safety_check(message_body)
        
        if risk_score >= 5:
            reply = "Thanks for reaching out. We're unavailable at the moment."
            logger.warning("High risk score (%s) for message from %s", risk_score, sender_number)
            log_interaction(sender_number, message_body, reply, flagged=True)
        else:
            reply = generate_ai_response(sender_number, message_body, context)
            log_interaction(sender_number, message_body, reply)

        return reply
    except Exception:
        logger.exception("Failed to process incoming SMS from %s", sender_number)
        return "Sorry, we're having trouble processing your message."
