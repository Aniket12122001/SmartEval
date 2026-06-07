import sqlite3
import os

# ================= DATABASE PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "exam_system.db")


# ================= CONNECTION =================
def get_connection():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


conn = get_connection()
cursor = conn.cursor()


# ================= USERS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    roll_number TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")


# ================= EXAMS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_name TEXT,
    teacher_id TEXT,
    subject_name TEXT,
    exam_name TEXT
)
""")


# ================= QUESTIONS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER,
    subject TEXT,
    question TEXT,
    reference_answer TEXT,
    marks INTEGER,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
)
""")


# ================= RESULTS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    roll_number TEXT,
    exam_id INTEGER,
    exam_name TEXT,
    obtained_marks REAL,
    total_marks REAL,
    percentage REAL,
    grade TEXT,
    question_data TEXT,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
)
""")


# ================= UNIQUE RESULT INDEX =================
cursor.execute("""
CREATE UNIQUE INDEX IF NOT EXISTS idx_result_unique
ON results (roll_number, exam_id)
""")

conn.commit()


# =================================================
# USERS
# =================================================
def create_user(username, roll_number, password, role):

    username = username.strip()
    roll_number = roll_number.strip().upper()

    cursor.execute(
        "SELECT * FROM users WHERE roll_number=?",
        (roll_number,)
    )

    if cursor.fetchone():
        return False

    cursor.execute("""
        INSERT INTO users
        (username, roll_number, password, role)
        VALUES (?, ?, ?, ?)
    """, (username, roll_number, password, role))

    conn.commit()
    return True


def login(username, password, role):

    cursor.execute("""
        SELECT * FROM users
        WHERE roll_number=? AND password=? AND role=?
    """, (username.strip().upper(), password, role))

    return cursor.fetchone()


def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


def get_teachers():
    cursor.execute("SELECT * FROM users WHERE role='teacher'")
    return cursor.fetchall()


def get_students():
    cursor.execute("SELECT * FROM users WHERE role='student'")
    return cursor.fetchall()


# =================================================
# EXAMS
# =================================================
def add_exam(teacher_name, teacher_id, subject, exam_name):

    cursor.execute("""
        INSERT INTO exams
        (teacher_name, teacher_id, subject_name, exam_name)
        VALUES (?, ?, ?, ?)
    """, (teacher_name, teacher_id, subject, exam_name))

    conn.commit()


def get_exams(teacher_id=None):

    if teacher_id:
        cursor.execute("""
            SELECT id, teacher_name, teacher_id, subject_name, exam_name
            FROM exams
            WHERE teacher_id=?
        """, (teacher_id,))
    else:
        cursor.execute("""
            SELECT id, teacher_name, teacher_id, subject_name, exam_name
            FROM exams
        """)

    return cursor.fetchall()


def delete_exam(exam_id, teacher_id=None):

    if teacher_id:
        cursor.execute("""
            DELETE FROM exams
            WHERE id=? AND teacher_id=?
        """, (exam_id, teacher_id))
    else:
        cursor.execute("""
            DELETE FROM exams
            WHERE id=?
        """, (exam_id,))

    conn.commit()


# =================================================
# QUESTIONS
# =================================================
def add_question(exam_id, subject, question, ref, marks):

    cursor.execute("""
        INSERT INTO questions
        (exam_id, subject, question, reference_answer, marks)
        VALUES (?, ?, ?, ?, ?)
    """, (exam_id, subject, question, ref, marks))

    conn.commit()


def get_questions(exam_id):

    cursor.execute("""
        SELECT id, exam_id, subject,
               question, reference_answer, marks
        FROM questions
        WHERE exam_id=?
    """, (exam_id,))

    return cursor.fetchall()


def update_question(question_id, question, reference_answer, marks):

    cursor.execute("""
        UPDATE questions
        SET question=?,
            reference_answer=?,
            marks=?
        WHERE id=?
    """, (question, reference_answer, marks, question_id))

    conn.commit()


def delete_question(question_id):

    cursor.execute(
        "DELETE FROM questions WHERE id=?",
        (question_id,)
    )

    conn.commit()


# =================================================
# RESULTS
# =================================================
def save_result(data):

    cursor.execute("""
        INSERT INTO results (
            student_name,
            roll_number,
            exam_id,
            exam_name,
            obtained_marks,
            total_marks,
            percentage,
            grade,
            question_data
        )
        VALUES (?,?,?,?,?,?,?,?,?)
    """, data)

    conn.commit()


def get_results():
    cursor.execute("SELECT * FROM results")
    return cursor.fetchall()


def has_attempted_exam(roll_number, exam_id):

    cursor.execute("""
        SELECT 1 FROM results
        WHERE roll_number=? AND exam_id=?
        LIMIT 1
    """, (roll_number, exam_id))

    return cursor.fetchone() is not None


# =================================================
# USER MANAGEMENT
# =================================================
def delete_user(user_id):

    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()


def update_user(user_id, username, roll_number, password):

    username = username.strip()
    roll_number = roll_number.strip().upper()

    cursor.execute("""
        UPDATE users
        SET username=?,
            roll_number=?,
            password=?
        WHERE id=?
    """, (username, roll_number, password, user_id))

    conn.commit()