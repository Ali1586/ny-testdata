import os
import sqlite3

# Ta bort gammal databas för att börja från början
if os.path.exists("mynewapp.db"):
    os.remove("mynewapp.db")

# Importera funktioner från app.py
from app import connect, init_db, anonymize_data, clear_test_data, generate_fake_users

print("=" * 40)
print("TESTER FÖR APP.PY")
print("=" * 40)

# TEST 1: GDPR-TEST - Anonymisering
print("\n🔒 GDPR-TEST: Anonymisera data")
print("-" * 30)

init_db()
anonymize_data()

conn = connect()
cursor = conn.cursor()
cursor.execute("SELECT name FROM personer WHERE id=1")
resultat = cursor.fetchone()

if resultat and resultat[0] == "Anonymiserad Namn":
    print("✅ PASS: Data anonymiserades korrekt för GDPR")
else:
    print("❌ FAIL: Data anonymiserades INTE korrekt")

conn.close()

# TEST 2: UNIT TEST - Databas skapas
print("\n🧪 UNIT TEST: Databas funktioner")
print("-" * 30)

if os.path.exists("mynewapp.db"):
    os.remove("mynewapp.db")

init_db()

if os.path.exists("mynewapp.db"):
    print("✅ PASS: Databasfil skapades")
else:
    print("❌ FAIL: Databasfil skapades INTE")

conn = connect()
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personer'")
tabell = cursor.fetchone()

if tabell:
    print("✅ PASS: Tabellen 'personer' skapades")
else:
    print("❌ FAIL: Tabellen skapades INTE")

cursor.execute("SELECT COUNT(*) FROM personer")
antal = cursor.fetchone()[0]

if antal == 2:
    print("✅ PASS: 2 personer lades till i tabellen")
else:
    print(f"❌ FAIL: Fel antal personer ({antal} istället för 2)")

conn.close()

# TEST 3: Generera fake-användare
print("\n🧪 GDPR-TEST: Generera fake-användare (Art. 5)")
print("-" * 30)

generate_fake_users(100)

conn = connect()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM personer")
antal = cursor.fetchone()[0]

# 2 från init_db + 100 från generate = 102
if antal == 102:
    print("✅ PASS: 100 fake-användare genererades korrekt")
else:
    print(f"❌ FAIL: Fel antal ({antal} istället för 102)")

conn.close()

print("\n" + "=" * 40)
print("TESTER KLARA")
print("=" * 40)