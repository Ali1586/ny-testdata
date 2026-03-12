"""
app.py - GDPR-säker testdata hantering
Kurs: Testdata, testmiljöer och dataskyddsförordningen (GDPR)
"""

import sqlite3
import os
import random
import string

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

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


def display_users(limit=10):
    """Visar användare i databasen. limit = hur många som visas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users LIMIT ?", (limit,))
    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    conn.close()

    if not rows:
        print("(Inga användare i databasen)")
    else:
        print(f"\n--- Visar {len(rows)} av totalt {total} användare ---")
        for row in rows:
            print(f"  ID: {row[0]} | Namn: {row[1]} | E-post: {row[2]}")
        print("--------------------------------------------------\n")


# ── GDPR-ÅTGÄRD 1: Radering (Art. 17 – Rätten att bli bortglömd) ──────────
def clear_test_data():
    """Raderar ALL data. GDPR Art. 17 - 'Right to be Forgotten'."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    print("🗑️  Alla testanvändare har raderats (GDPR Art. 17).")


def delete_user(user_id: int):
    """Raderar EN specifik användare. GDPR Art. 17."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted:
        print(f"🗑️  Användare med ID {user_id} raderades (GDPR Art. 17).")
    else:
        print(f"⚠️  Ingen användare med ID {user_id} hittades.")


# ── GDPR-ÅTGÄRD 2: Anonymisering (Art. 4(5)) ─────────────────────────────
def anonymize_data():
    """Ersätter namn och e-post med anonym data. GDPR Art. 4(5)."""
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


# ── GDPR-ÅTGÄRD 3: Generera fake-användare (Art. 5 – Dataminimering) ──────
def generate_fake_users(count: int = 1000):
    """
    Genererar realistisk men helt PÅHITTAD testdata i stor skala.
    Ingen riktig personinformation används.
    GDPR Art. 5 – Dataminimering.

    count = antal användare att generera (standard 1000, fungerar upp till 100 000+)
    """
    first_names = [
        "Anna", "Bo", "Carl", "Diana", "Erik", "Fatima", "Gustav", "Hanna",
        "Ivan", "Julia", "Karl", "Lisa", "Magnus", "Nina", "Oscar", "Petra",
        "Reza", "Sara", "Thomas", "Ulrika", "Viktor", "Wendy", "Yasmin",
        "Maria", "Johan", "Emma", "Lars", "Sofia", "Anders", "Zakaria"
    ]
    last_names = [
        "Andersson", "Bergström", "Carlsson", "Davidsson", "Eriksson",
        "Fransson", "Gustafsson", "Hansson", "Johansson", "Karlsson",
        "Lindgren", "Magnusson", "Nilsson", "Olsson", "Persson",
        "Svensson", "Thorsson", "Vikström", "Wallén", "Zetterberg"
    ]

    def random_string(length=6):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    # Bygg hela listan först – mycket snabbare än att insertera en i taget
    fake_users = []
    for _ in range(count):
        first = random.choice(first_names)
        last  = random.choice(last_names)
        email = f"{first.lower()}.{last.lower()}{random_string()}@faketest.se"
        fake_users.append((f"{first} {last}", email))

    # Spara alla på en gång med executemany
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", fake_users)
    conn.commit()
    conn.close()

    print(f"🧪 {count:,} fake-användare genererade (GDPR Art. 5 – Dataminimering).")


# ── Huvudprogram ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== GDPR Testdata System ===\n")

    # 1. Initiera databasen
    init_db()

    # 2. Visa original-data
    print("📋 Original testdata:")
    display_users()

    # 3. Generera 100 000 fake-användare
    print("⏳ Genererar 100 000 fake-användare...")
    generate_fake_users(100_000)

    print("📋 Exempel på genererade användare (visar 10 st):")
    display_users(limit=10)

    # 4. Anonymisera
    anonymize_data()
    print("📋 Efter anonymisering (visar 10 st):")
    display_users(limit=10)

    # 5. Radera allt
    clear_test_data()
    print("📋 Efter radering:")
    display_users()

    print("✅ Systemet fungerar korrekt!")