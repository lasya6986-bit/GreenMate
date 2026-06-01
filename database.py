import sqlite3
conn = sqlite3.connect("greenmate.db")
cursor= conn.cursor()
cursor.execute("""
               create table if not exists plants(id integer primary key autoincrement,
               plant_name text not null,last_watered text,sunlight text)""")
conn.commit()

cursor.execute("""
               Create table if not exists watering_history(history_id INTEGER PRIMARY KEY AUTOINCREMENT,
               plant_id INTEGER, watering_date TEXT,FOREIGN KEY(plant_id) references plants(id))""")
conn.commit()

print("DataBase and table created successfully!")
conn.close()
