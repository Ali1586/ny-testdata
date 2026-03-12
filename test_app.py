import os
import sqlite3

# Använd en separat testdatabas så vi inte förstör riktig data
os.environ["DB_PATH"] = "/tmp/test_users.db"

# Ta bort gammal testdatabas för att börja från början
if os.path.exists("/tmp/test_users.db"):
    os.remove("/tmp/test_users.db")

# Importera funktioner från app.py
from app import init_db, display_users, clear_test_data, anonymize_data, generate_fake_users, get_connection

print("=" * 40)
print("TESTER FÖR APP.PY")
print("=" * 40)

# ── TEST 1: Databas och tabell skapas ─────────────────────────────────────
print("\n🧪 TEST 1: Databas skapas korrekt")
print("-" * 30)

init_db()

if os.path.exists("/tmp/test_users.db"):
    print("✅ PASS: Databasfil skapades")
else:
    print("❌ FAIL: Databasfil skapades INTE")

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
tabell = cursor.fetchone()

if tabell:
    print("✅ PASS: Tabellen 'users' skapades")
else:
    print("❌ FAIL: Tabellen skapades INTE")

cursor.execute("SELECT COUNT(*) FROM users")
antal = cursor.fetchone()[0]

if antal == 2:
    print("✅ PASS: 2 testanvändare lades till")
else:
    print(f"❌ FAIL: Fel antal användare ({antal} istället för 2)")

conn.close()

# ── TEST 2: Anonymisering fungerar ────────────────────────────────────────
print("\n🔒 TEST 2: Anonymisering (GDPR Art. 4(5))")
print("-" * 30)

anonymize_data()

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT name, email FROM users WHERE id=1")
rad = cursor.fetchone()

if rad and "Anonym" in rad[0] and "okänd.se" in rad[1]:
    print("✅ PASS: Data anonymiserades korrekt")
else:
    print("❌ FAIL: Data anonymiserades INTE korrekt")

conn.close()

# ── TEST 3: Radering fungerar ─────────────────────────────────────────────
print("\n🗑️  TEST 3: Radering (GDPR Art. 17)")
print("-" * 30)

clear_test_data()

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
antal = cursor.fetchone()[0]

if antal == 0:
    print("✅ PASS: All data raderades korrekt")
else:
    print(f"❌ FAIL: {antal} användare finns kvar efter radering")

conn.close()

# ── TEST 4: Generera fake-användare ──────────────────────────────────────
print("\n🧪 TEST 4: Generera fake-användare (GDPR Art. 5)")
print("-" * 30)

generate_fake_users(500)

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
antal = cursor.fetchone()[0]

if antal == 500:
    print("✅ PASS: 500 fake-användare genererades korrekt")
else:
    print(f"❌ FAIL: Fel antal ({antal} istället för 500)")

# Kontrollera att e-post innehåller @faketest.se
cursor.execute("SELECT email FROM users LIMIT 1")
email = cursor.fetchone()[0]

if "@faketest.se" in email:
    print("✅ PASS: Fake e-postadresser ser korrekta ut")
else:
    print("❌ FAIL: E-postadresser ser fel ut")

conn.close()

print("\n" + "=" * 40)
print("TESTER KLARA")
print("=" * 40)