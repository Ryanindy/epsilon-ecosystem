"""
Goal Queue Manager: Manages the persistent queue of autonomous objectives.
"""
import sqlite3
import json
import os
import time
from typing import List, Dict, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "memory.db")

class GoalQueue:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS goal_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    goal TEXT,
                    priority INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'pending', -- pending, processing, completed, failed
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    result TEXT
                )
            ''')
            conn.commit()

    def add_goal(self, goal: str, source: str = "system", priority: int = 1) -> int:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO goal_queue (goal, source, priority) VALUES (?, ?, ?)",
                (goal, source, priority)
            )
            conn.commit()
            return cursor.lastrowid

    def get_next_goal(self) -> Optional[Dict]:
        """Fetches the highest priority pending goal."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM goal_queue WHERE status = 'pending' ORDER BY priority DESC, created_at ASC LIMIT 1"
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def update_status(self, goal_id: int, status: str, result: str = None):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if result:
                cursor.execute(
                    "UPDATE goal_queue SET status = ?, result = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (status, result, goal_id)
                )
            else:
                cursor.execute(
                    "UPDATE goal_queue SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (status, goal_id)
                )
            conn.commit()

    def list_pending(self) -> List[Dict]:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM goal_queue WHERE status = 'pending'")
            return [dict(row) for row in cursor.fetchall()]
