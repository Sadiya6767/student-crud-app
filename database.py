import os
import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

# Ensure database is stored in the same folder as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")


@contextmanager
def get_db_connection():
    """
    Context manager for SQLite database connection.
    Automatically handles closing the connection and provides row access by column name.
    """
    conn = sqlite3.connect(DB_PATH)
    # Allows accessing columns by name: row["name"] or dict(row)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """
    Creates the students table automatically if it does not already exist.
    Called when the FastAPI application starts up.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                course TEXT,
                address TEXT,
                enrollment_date TEXT
            );
        """)
        conn.commit()


def create_student(student_data: Dict[str, Any]) -> int:
    """
    Inserts a new student record into SQLite using parameterized query.
    Returns the newly generated student ID.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (
                name,
                date_of_birth,
                email,
                phone,
                course,
                address,
                enrollment_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (
            student_data.get("name"),
            student_data.get("date_of_birth"),
            student_data.get("email"),
            student_data.get("phone"),
            student_data.get("course"),
            student_data.get("address"),
            student_data.get("enrollment_date")
        ))
        conn.commit()
        return cursor.lastrowid


def get_all_students() -> List[Dict[str, Any]]:
    """
    Fetches all student records from SQLite sorted by ID.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY id ASC;")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_student_by_id(student_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieves a single student by their unique ID.
    Returns a dictionary of student data or None if not found.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?;", (student_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


def update_student(student_id: int, student_data: Dict[str, Any]) -> bool:
    """
    Performs a full update (PUT) of a student's record using parameterized query.
    Returns True if a row was updated, False if student_id was not found.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE students
            SET name = ?,
                date_of_birth = ?,
                email = ?,
                phone = ?,
                course = ?,
                address = ?,
                enrollment_date = ?
            WHERE id = ?;
        """, (
            student_data.get("name"),
            student_data.get("date_of_birth"),
            student_data.get("email"),
            student_data.get("phone"),
            student_data.get("course"),
            student_data.get("address"),
            student_data.get("enrollment_date"),
            student_id
        ))
        conn.commit()
        return cursor.rowcount > 0


def patch_student(student_id: int, update_fields: Dict[str, Any]) -> bool:
    """
    Performs a partial update (PATCH) on only the fields provided.
    Uses parameterized query and a strict column whitelist to prevent SQL injection.
    """
    # Strict whitelist of allowed database columns
    allowed_columns = {
        "name",
        "date_of_birth",
        "email",
        "phone",
        "course",
        "address",
        "enrollment_date"
    }

    # Filter out any unexpected keys
    valid_updates = {col: val for col, val in update_fields.items() if col in allowed_columns}

    if not valid_updates:
        # Nothing valid to update
        return True

    # Construct parameterized SET clause: "col1 = ?, col2 = ?"
    set_clause = ", ".join([f"{column} = ?" for column in valid_updates.keys()])
    values = list(valid_updates.values())
    values.append(student_id)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        sql_query = f"UPDATE students SET {set_clause} WHERE id = ?;"
        cursor.execute(sql_query, values)
        conn.commit()
        return cursor.rowcount > 0


def delete_student(student_id: int) -> bool:
    """
    Deletes a student record by ID using a parameterized query.
    Returns True if deleted, False if student_id was not found.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?;", (student_id,))
        conn.commit()
        return cursor.rowcount > 0
