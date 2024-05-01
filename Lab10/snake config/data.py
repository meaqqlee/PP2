import psycopg2

conn = psycopg2.connect(
    dbname='snake_game', user='postgres', password='magzhan0201', host='localhost'
)
cursor = conn.cursor()

cursor.execute("SELECT * FROM users;")
scores = cursor.fetchall()

print("table consists user_scores:")
for score in scores:
    print(score)

cursor.close()
conn.close()
