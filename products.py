import sqlite3
conn = sqlite3.connect('db.db')

c = conn.cursor()

with open('vegetables.txt') as f:
    lines = f.readlines()


# insert
for i in range(0, 120):
    c.execute("INSERT INTO products(name, unit, category, author_id, date_added, public) VALUES (?, 'pcs', 'fruit', 1, datetime(), 1)", (lines[i].rstrip().lower(),))

# Zapisz zmiany
conn.commit()

# Zamknięcie połączenia z bazą danych
conn.close()