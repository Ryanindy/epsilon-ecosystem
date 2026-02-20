"""
SMS Handler: Manages incoming messages and conversation context.
Version: 2.0 (Thread-safe with connection pooling)
"""
import logging
import sqlite3
import os
import threading
from datetime import datetime
from contextlib import contextmanager

# --- PROJECT ROOT ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

import persona_prompt

# --- LOGGING ---
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("SMSHandler")

# --- DATABASE CONFIGURATION ---
DB_PATH = os.path.join(PROJECT_ROOT, "memory.db")

# --- THREAD-SAFE CONNECTION POOL ---
class SQLiteConnectionPool:
    """Thread-safe SQLite connection manager."""

    def __init__(self, db_path: str, max_connections: int = 5):
        self.db_path = db_path
        self._local = threading.local()
        self._lock = threading.Lock()
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        try:
            conn = sqlite3.connect(self.db_path)
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
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_sender ON interactions(sender)
            ''')
            conn.commit()
            conn.close()
            logger.info(f"Database initialized: {self.db_path}")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    @contextmanager
    def get_connection(self):
        """Get a thread-local database connection."""
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            self._local.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=30.0
            )
            self._local.connection.row_factory = sqlite3.Row

        try:
            yield self._local.connection
        except Exception as e:
            self._local.connection.rollback()
            raise

    def close_all(self):
        """Close thread-local connection if exists."""
        if hasattr(self._local, 'connection') and self._local.connection:
            self._local.connection.close()
            self._local.connection = None

# Initialize connection pool
db_pool = SQLiteConnectionPool(DB_PATH)

# --- SAFETY CHECK ---
RISK_KEYWORDS = ["exploit", "hack", "illegal", "threat", "attack", "malware", "ransomware"]

def run_safety_check(message: str) -> int:
    """
    Basic safety check. High-risk keywords trigger a higher score.
    """
    score = 0
    message_lower = message.lower()
    for word in RISK_KEYWORDS:
        if word in message_lower:
            score += 2
    return score

# --- CORE FUNCTIONS ---

def generate_ai_response(sender_number: str, message: str, context: dict) -> str:
    """
    Calls the persona_prompt module to get a real AI response.
    """
    try:
        return persona_prompt.generate_ai_response(sender_number, message, context)
    except Exception as e:
        logger.error(f"AI response generation failed: {e}")
        return "I'm having trouble processing your request right now."

def log_interaction(sender: str, message: str, response: str, flagged: bool = False):
    """
    Logs the interaction to the SQLite database.
    """
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO interactions (sender, message_in, message_out, flagged) VALUES (?, ?, ?, ?)",
                (sender, message, response, 1 if flagged else 0)
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Failed to log interaction: {e}")

def fetch_client_context(sender: str) -> dict:
    """
    Fetches the last 5 interactions for a given sender to provide context.
    """
    try:
        with db_pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT message_in, message_out FROM interactions WHERE sender = ? ORDER BY timestamp DESC LIMIT 5",
                (sender,)
            )
            rows = cursor.fetchall()

            # Format for persona_prompt (oldest first for chronological order)
            history = []
            for row in reversed(rows):
                history.append({"message_in": row["message_in"], "message_out": row["message_out"]})

            return {"recent_messages": history}
    except Exception as e:
        logger.error(f"Failed to fetch client context: {e}")
        return {"recent_messages": []}

def handle_incoming_sms(sender_number: str, message_body: str) -> str:
    """
    Process an inbound SMS and return the reply text.
    """
    logger.info(f"Received message from {sender_number}: {message_body[:50]}...")

    try:
        context = fetch_client_context(sender_number)
        risk_score = run_safety_check(message_body)

        if risk_score >= 5:
            reply = "Thanks for reaching out. We're unavailable at the moment."
            logger.warning(f"High risk score ({risk_score}) for message from {sender_number}")
            log_interaction(sender_number, message_body, reply, flagged=True)
        else:
            reply = generate_ai_response(sender_number, message_body, context)
            log_interaction(sender_number, message_body, reply)

        return reply
    except Exception as e:
        logger.exception(f"Failed to process incoming message from {sender_number}")
        return "Sorry, we're having trouble processing your message."
