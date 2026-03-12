import os
import sqlite3

# Använd en separat testdatabas så vi inte förstör riktig data
os.environ["DB_PATH"] = "/tmp/test_users.db"

# Ta bort gammal testdatabas för att börja från början
if os.path.exists("/tmp/test_users.db"):
    os.remove("/tmp/test_users.db")

# Importera funktioner från app.py
from app import get_connection, init_db, anonymize_data, clear_test_data, generate_fake_users

print("=" * 40)
print("TESTER FÖR APP.PY")
print("=" * 40)

# TEST 1: GDPR-TEST – Anonymisering
print("\n🔒 GDPR-TEST: Anonymisera data")
print("-" * 30)

init_db()
anonymize_data()

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT name FROM users WHERE id=1")
resultat = cursor.fetchone()

if resultat and "Anonym" in resultat[0]:
    print("✅ PASS: Data anonymiserades korrekt för GDPR")
else:
    print("❌ FAIL: Data anonymiserades INTE korrekt")

conn.close()

# TEST 2: UNIT TEST – Databas skapas
print("\n🧪 UNIT TEST: Databas funktioner")
print("-" * 30)

# Börja om från början
if os.path.exists("/tmp/test_users.db"):
    os.remove("/tmp/test_users.db")

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
    print("✅ PASS: 2 användare lades till i tabellen")
else:
    print(f"❌ FAIL: Fel antal användare ({antal} istället för 2)")

conn.close()

# TEST 3: GDPR-TEST – Radering
print("\n🗑️  GDPR-TEST: Radera all data")
print("-" * 30)

clear_test_data()

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
antal = cursor.fetchone()[0]

if antal == 0:
    print("✅ PASS: All data raderades korrekt")
else:
    print(f"❌ FAIL: {antal} användare finns kvar")

conn.close()

# TEST 4: Generera fake-användare
print("\n🧪 GDPR-TEST: Generera fake-användare")
print("-" * 30)

generate_fake_users(100)

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
antal = cursor.fetchone()[0]

if antal == 100:
    print("✅ PASS: 100 fake-användare genererades korrekt")
else:
    print(f"❌ FAIL: Fel antal ({antal} istället för 100)")

conn.close()

print("\n" + "=" * 40)
print("TESTER KLARA")
print("=" * 40)