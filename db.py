import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = 'reports.db'


def init_db() -> None:
    """Initialize the SQLite database and reports table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            summary TEXT,
            sources TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_report(query: str, summary: str, sources: str) -> int:
    """Save a new report and return its ID."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO reports (query, summary, sources, created_at) VALUES (?, ?, ?, ?)',
        (query, summary, sources, datetime.utcnow().isoformat())
    )
    conn.commit()
    report_id = c.lastrowid
    conn.close()
    return report_id


def get_all_reports() -> List[Dict]:
    """Return a list of all reports (id, query, created_at)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, query, created_at FROM reports ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return [{'id': r[0], 'query': r[1], 'created_at': r[2]} for r in rows]


def get_report_by_id(report_id: int) -> Optional[Dict]:
    """Return a single report by ID."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'SELECT id, query, summary, sources, created_at FROM reports WHERE id = ?',
        (report_id,)
    )
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {
        'id': row[0],
        'query': row[1],
        'summary': row[2],
        'sources': row[3],
        'created_at': row[4]
    }


# Initialize DB automatically when importing
init_db()
