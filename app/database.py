"""Small SQLite helpers for report metadata and learning notes."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from app.config import DATABASE_PATH


def connect(path: Path = DATABASE_PATH) -> sqlite3.Connection:
  """Open a SQLite connection and ensure the parent directory exists."""
  path.parent.mkdir(parents=True, exist_ok=True)
  return sqlite3.connect(path)


def init_db(path: Path = DATABASE_PATH) -> None:
  """Create local metadata tables if they do not already exist."""
  with connect(path) as db:
    db.execute(
      """
      CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_type TEXT NOT NULL,
        title TEXT NOT NULL,
        markdown_path TEXT NOT NULL,
        json_path TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
      )
      """
    )
    db.commit()


def save_report_metadata(
  *,
  report_type: str,
  title: str,
  markdown_path: str,
  json_path: str,
  path: Path = DATABASE_PATH,
) -> None:
  """Store report file locations for the dashboard."""
  init_db(path)
  with connect(path) as db:
    db.execute(
      """
      INSERT INTO reports (report_type, title, markdown_path, json_path)
      VALUES (?, ?, ?, ?)
      """,
      (report_type, title, markdown_path, json_path),
    )
    db.commit()


def recent_reports(limit: int = 5, path: Path = DATABASE_PATH) -> list[dict[str, str]]:
  """Return recent reports for UI display."""
  init_db(path)
  with connect(path) as db:
    rows = db.execute(
      """
      SELECT report_type, title, markdown_path, json_path, created_at
      FROM reports
      ORDER BY created_at DESC, id DESC
      LIMIT ?
      """,
      (limit,),
    ).fetchall()
  return [
    {
      "report_type": row[0],
      "title": row[1],
      "markdown_path": row[2],
      "json_path": row[3],
      "created_at": row[4],
    }
    for row in rows
  ]
