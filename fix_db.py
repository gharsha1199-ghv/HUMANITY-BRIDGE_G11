import mysql.connector

db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Sharjina@74802',
    database='humanity_bridge'
)
cursor = db.cursor()

tables_to_add_status = [
    'donors', 
    'volunteers', 
    'regulardonors', 
    'ngo_receivers', 
    'donor_donations', 
    'regular_donor_donations', 
    'ngo_requests', 
    'deliveries'
]

for table in tables_to_add_status:
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN status VARCHAR(50) DEFAULT 'Pending'")
        db.commit()
        print(f"Added status to {table}")
    except Exception as e:
        print(f"Error adding status to {table}: {e}")

cursor.close()
db.close()
