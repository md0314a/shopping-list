import sqlite3
conn = sqlite3.connect('db.db')

c = conn.cursor()

with open('processed foods.txt') as f:
    lines = f.readlines()


# insert
for line in lines:
    line = line.split(',')

    if line[1] == '\n':
        line[1] = 'pcs'

    c.execute("INSERT INTO products(name, unit, category, author_id, date_added, public) VALUES (?, ?, 'processed foods', 1, datetime(), 1)", (line[0].rstrip().lower(), line[1].strip()))

# Zapisz zmiany
conn.commit()

# Zamknięcie połączenia z bazą danych
conn.close()