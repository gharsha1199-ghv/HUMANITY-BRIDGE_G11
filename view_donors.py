import mysql.connector

try:
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Sharjina@74802',
        database='humanity_bridge'
    )
    cursor = db.cursor()
    
    print("--- DONORS TABLE DATA ---")
    cursor.execute("SELECT id, name, phone, email, city, pincode FROM donors")
    rows = cursor.fetchall()
    
    if not rows:
        print("No donors found in the database.")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {row[3]} | City: {row[4]} | Pincode: {row[5]}")
        
    print("\n--- VOLUNTEERS TABLE DATA ---")
    cursor.execute("SELECT id, name, phone, email, city, pincode, vehicle_type FROM volunteers")
    v_rows = cursor.fetchall()
    
    if not v_rows:
        print("No volunteers found in the database.")
    for row in v_rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {row[3]} | City: {row[4]} | Pincode: {row[5]} | Vehicle: {row[6]}")
        
    cursor.close()
    db.close()
except Exception as e:
    print("Error connecting to database:", e)
