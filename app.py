"""
app.py - GDPR-säker testdata hantering
Kurs: Testdata, testmiljöer och dataskyddsförordningen (GDPR)
"""

import sqlite3
import os

# Sökväg till databasen (sparas i /data när Docker körs)
DB_PATH = os.getenv("DB_PATH", "/data/test_users.db")


def get_connection():
    """Öppnar anslutning till SQLite-databasen."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Skapar tabellen 'users' och lägger till två testanvändare.
    Körs automatiskt vid start.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Skapa tabell om den inte finns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # Lägg till testanvändare om tabellen är tom
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        test_users = [
            ("Anna Andersson", "anna@test.se"),
            ("Bo Bergström",   "bo@test.se"),
        ]
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", test_users)
        print("✅ Två testanvändare skapade.")

    conn.commit()
    conn.close()


def display_users():
    """Visar alla användare i databasen."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("(Inga användare i databasen)")
    else:
        print("\n--- Användare i databasen ---")
        for row in rows:
            print(f"  ID: {row[0]} | Namn: {row[1]} | E-post: {row[2]}")
        print("-----------------------------\n")


# ── GDPR-ÅTGÄRD 1: Radering (Art. 17 – Rätten att bli bortglömd) ──────────
def clear_test_data():
    """
    Raderar ALL data ur tabellen users.
    Motsvarar GDPR Art. 17 - 'Right to be Forgotten'.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    print("🗑️  Alla testanvändare har raderats (GDPR Art. 17).")


def delete_user(user_id: int):
    """
    Raderar EN specifik användare baserat på ID.
    Hanterar en enskild 'Right to be Forgotten'-begäran.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    deleted = cursor.rowcount  # antal raderade rader
    conn.close()

    if deleted:
        print(f"🗑️  Användare med ID {user_id} raderades (GDPR Art. 17).")
    else:
        print(f"⚠️  Ingen användare med ID {user_id} hittades.")


# ── GDPR-ÅTGÄRD 2: Anonymisering (Art. 4(5)) ─────────────────────────────
def anonymize_data():
    """
    Ersätter namn och e-post med anonym/icke-identifierbar data.
    Motsvarar GDPR Art. 4(5) - Pseudonymisering/Anonymisering.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    user_ids = cursor.fetchall()

    for (uid,) in user_ids:
        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (f"Anonym Användare {uid}", f"anonym{uid}@okänd.se", uid),
        )

    conn.commit()
    conn.close()
    print("🔒 Alla användare har anonymiserats (GDPR Art. 4(5)).")


# ── Huvudprogram ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== GDPR Testdata System ===\n")

    # 1. Initiera databasen
    init_db()

    # 2. Visa original-data
    print("📋 Original testdata:")
    display_users()

    # 3. Demonstrera anonymisering
    anonymize_data()
    print("📋 Efter anonymisering:")
    display_users()

    # 4. Demonstrera radering
    clear_test_data()
    print("📋 Efter radering:")
    display_users()

    print("✅ Systemet fungerar korrekt!")