from datetime import datetime
import sqlite3
def valid_date(date):
    try:
        datetime.strptime(date,"%d-%m-%Y")
        return True
    except:
        return False
def needs_watering(date,watering_frequency_days):
    last_watered=datetime.strptime(date,"%d-%m-%Y")
    today=datetime.now()
    days=(today-last_watered).days
    if(days>watering_frequency_days):
        return True
    return False 
def add_plant():
    plant=input("Enter plant name : ")
    while True:
        watered=input("Enter last watered date :")
        if(valid_date(watered)):
            break
        print("Invalid Date ! Use DD-MM-YYYY")
    sunlight=input("Enter sunlight requirement: ")
    plant_type=input("Enter type of the plant: ")
    watering_frequency=int(input("Enter the watering frequency : "))
    cursor.execute("""
                       insert into plants (plant_name,last_watered,sunlight,plant_type,watering_frequency_days) values (?,?,?,?,?)""",(plant,watered,sunlight,plant_type,watering_frequency))
    conn.commit()
    plant_id=cursor.lastrowid
       
    cursor.execute(""" 
                       insert
                        into watering_history(plant_id,watering_date) values (?,?)""",(plant_id,watered))
    conn.commit()
    print("Plant added Successfully")
def view_plants():
    cursor.execute("select * from plants")
    rows=cursor.fetchall()
    if len(rows)==0:
        print("No plants added yet!")
    else:
        print("------------")
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"Plant Name : {row[1]}")
            print(f"Last watered : {row[2]}")
            print(f"Sunlight : {row[3]}")
            print(f"Type of plant : {row[4]}")
            print(f"Watering frequency : {row[5]} days")
            if(needs_watering(row[2],row[5])):
                print("⚠ Needs Watering")
            print("------------")     
def update_watering():
        plant_id=int(input("Enter Plant ID : "))
        cursor.execute("""
                       select * from plants where id=?""",(plant_id,))
        
        plant=cursor.fetchone()
        if(plant is not None):
            while True:
                new_date=input("Enter new watered date : ")
                if(valid_date(new_date)):
                    break
                print("Invalid Format ! Use DD-MM-YYYY")
            cursor.execute("""
                       update plants set last_watered=? where id=?
                       """,(new_date,plant_id))
            conn.commit()
            cursor.execute("""
                           insert into watering_history(plant_id,watering_date) values(?,?)""",(plant_id,new_date))
            conn.commit()
            print("Watering date updated successfully!")
       
            
        else:    
            print("Plant ID NOT Found")
def delete_plant():
        plant_id=int(input("Enter plant ID to be deleted : "))
        cursor.execute("""
                       delete from watering_history where plant_id=?""",(plant_id,))
        cursor.execute("""
                       delete from plants where id=?""",(plant_id,))
        if(cursor.rowcount==0):
            print("Plant ID not found!")
        else:
            print("Plant Deleted successfully!")
        conn.commit()   

def search_plant():
        plant=input("Enter plant name :")
        cursor.execute("""
                       select * from plants where lower(plant_name)= lower(?)""",(plant,))
        row=cursor.fetchone()
        if(row is None):
            print(plant," does not exists !")
        else:
          
            print("-----Plant Details-----")
            print("ID : ",row[0])
            print("Name : ",row[1])
            print("Last_water_date : ",row[2])
            print("Level of Sunlight Required : ",row[3])
            print(f"Type of plant : {row[4]}")
            print(f"Watering frequency : {row[5]} days")  

def view_history():
    cursor.execute("select * from watering_history")
        
    rows=cursor.fetchall()
    if len(rows)==0:
        print("No plants added yet!")
    else:
        print("------------")
        for row in rows:
            cursor.execute("""
                               select * from plants where id=?""",(row[1],))
            row1=cursor.fetchone()
            print(f"History ID: {row[0]}")
            print(f"Plant Id : {row[1]}")
            print(f"Plant Name : {row1[1]}")
            print(f"Watering date : {row[2]}")
                
            print("------------")  

def show_statistics():
        cursor.execute("""
                                   select count(*) from plants """)
        plant_count=cursor.fetchone()
        cursor.execute("""
                       select count(*) from watering_history""")
        
        records=cursor.fetchone()
        count=0
        cursor.execute("""
                       select * from plants """)
        rows=cursor.fetchall()
        if(rows is not  None):
            for row in rows:
                if(needs_watering(row[2],row[5])):
                    count+=1
        print("----- PLANT STATISTICS ------")
        print("Total Plants - ",plant_count[0] if(plant_count) else 0)
        print("Total Watering Records - ",records[0] if(records) else 0)
        print("Plants Need Watering - ",count)
        print("-----------------------------")





conn=sqlite3.connect("greenmate.db")
cursor=conn.cursor()
while(True):
    print("\n====== GREENMATE ======\n")
    print("1. Add Plant")
    print("2. View Plants")
    print("3. Update Watering Date")
    print("4. Delete plant")
    print("5. Search Plant")
    print("6. View Watering History")
    print("7. Plant Statistics")
    print("8. Exit")
    choice=int(input("Enter your choice :"))
    if(choice==1):
        add_plant()

    elif(choice==2):
        view_plants() 
    elif choice==3:
        update_watering()
    elif choice==4:
        delete_plant()      
    elif choice==5:
        search_plant()   

    elif choice==6:
        view_history()


    elif choice==7:
        show_statistics()
    elif choice==8:
        print("Thank you for using GreenMate!")
        break
    else:
        print("Invalid choice!")        
conn.close()
