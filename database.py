import sqlite3
from datetime import datetime

DATABASE = "history.db"


def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================
# INITIALIZE DATABASE
# =====================================

def initialize_database():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        patient_name TEXT NOT NULL,

        age INTEGER NOT NULL,

        gender TEXT NOT NULL,

        model TEXT NOT NULL,

        prediction TEXT NOT NULL,

        confidence REAL NOT NULL,

        image_path TEXT,

        gradcam_path TEXT,

        pdf_path TEXT,

        created_at TEXT NOT NULL

    )
    """)

    conn.commit()
    conn.close()


# =====================================
# SAVE RECORD
# =====================================

def save_prediction(
        patient_name,
        age,
        gender,
        model,
        prediction,
        confidence,
        image_path,
        gradcam_path,
        pdf_path):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO history(

        patient_name,
        age,
        gender,
        model,
        prediction,
        confidence,
        image_path,
        gradcam_path,
        pdf_path,
        created_at

    )

    VALUES(?,?,?,?,?,?,?,?,?,?)

    """, (

        str(patient_name),
        int(age),
        str(gender),
        str(model),
        str(prediction),
        float(confidence),
        str(image_path),
        str(gradcam_path) if gradcam_path else "",
        str(pdf_path),
        datetime.now().strftime("%d-%m-%Y %H:%M")

    ))

    conn.commit()
    conn.close()


# =====================================
# GET ALL HISTORY
# =====================================

def get_history():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM history

    ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# =====================================
# SEARCH HISTORY
# =====================================

def search_history(keyword):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM history

    WHERE patient_name LIKE ?

    ORDER BY id DESC

    """, (f"%{keyword}%",))

    rows = cursor.fetchall()

    conn.close()

    return rows


# =====================================
# DASHBOARD STATS
# =====================================

def get_statistics():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM history")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM history WHERE prediction='Tuberculosis'"
    )
    tb = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM history WHERE prediction='Normal'"
    )
    normal = cursor.fetchone()[0]

    conn.close()

    return {

        "total": total,

        "tb": tb,

        "normal": normal

    }


# =====================================
# DELETE RECORD
# =====================================

def delete_record(record_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM history WHERE id=?",

        (record_id,)

    )

    conn.commit()

    conn.close()