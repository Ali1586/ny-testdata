import sqlite3
import os

# Databasnamn
db_namn = "mynewapp.db"

def connect():
    return sqlite3.connect(db_namn)

def init_db():
    conn = connect()
    cursor = conn.cursor()

    # Skapa tabell
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personer (
            id    INTEGER PRIMARY KEY,
            name  TEXT,
            email TEXT
        )
    ''')

    # Lägg till 2 testanvändare om tabellen är tom
    cursor.execute('SELECT COUNT(*) FROM personer')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO personer (id, name, email) VALUES (?, ?, ?)
        ''', [
            (1, 'Testperson1', 'test1@faketest.se'),
            (2, 'Testperson2', 'test2@faketest.se')
        ])
        print('Testdata skapad.')

    conn.commit()
    conn.close()

def display_users():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personer')
    for rad in cursor.fetchall():
        print(f"ID: {rad[0]}, Namn: {rad[1]}, E-post: {rad[2]}")
    conn.close()

# GDPR-åtgärd 1: Radering (Art. 17 - Rätten att bli bortglömd)
def clear_test_data():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM personer')
    conn.commit()
    conn.close()
    print('All data raderad (GDPR Art. 17).')

# GDPR-åtgärd 2: Anonymisering (Art. 4(5))
def anonymize_data():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE personer SET name = 'Anonymiserad Namn'")
    conn.commit()
    conn.close()
    print('All data anonymiserad (GDPR Art. 4(5)).')

# GDPR-åtgärd 3: Generera valfritt antal fake-användare (Art. 5 - Dataminimering)
# Exempel: generate_fake_users(1000000) = 1 miljon användare
def generate_fake_users(count=10):
    conn = connect()
    cursor = conn.cursor()

    # Genererar 'count' antal påhittade användare automatiskt
    fake_users = [
        (f'Testperson{i}', f'test{i}@faketest.se') for i in range(1, count + 1)
    ]
    cursor.executemany('INSERT INTO personer (name, email) VALUES (?, ?)', fake_users)
    conn.commit()
    conn.close()
    print(f'{count} fake-användare skapade (GDPR Art. 5).')

if __name__ == "__main__":
    print('=== GDPR Testdata System ===')

    print('\n[Steg 1: Skapa 2 testanvändare]')
    init_db()
    display_users()

    print('\n[Steg 2: Anonymisera]')
    anonymize_data()
    display_users()

    print('\n[Steg 3: Radera allt]')
    clear_test_data()
    display_users()

    print('\nKlart!')