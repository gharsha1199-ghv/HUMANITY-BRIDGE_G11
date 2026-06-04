import mysql.connector

db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Sharjina@74802',
    database='humanity_bridge'
)
cursor = db.cursor()

cursor.execute("SHOW PROCESSLIST")
processes = cursor.fetchall()

for p in processes:
    print(p)
    if p[4] == 'Sleep' and p[5] > 10:
        print(f"Killing process {p[0]}")
        try:
            cursor.execute(f"KILL {p[0]}")
        except Exception as e:
            print(f"Error killing {p[0]}: {e}")

cursor.close()
db.close()
