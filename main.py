import sqlite3
conn=sqlite3.connect("greenmate.db")
cursor=conn.cursor()
while(True):
    print("\n====== GREENMATE ======\n")
    print("1. Add Plant")
    print("2. View Plants")
    print("3. Update Watering Date")
    print("4. Delete plant")
    print("5. Search Plant")
    print("6. Exit")
    choice=int(input("Enter your choice :"))
    if(choice==1):
        plant=input("Enter plant name : ")
        watered=input("Enter last watered date :")
        sunlight=input("Enter sunlight requirement: ")
        cursor.execute("""
                       insert into plants (plant_name,last_watered,sunlight) values (?,?,?)""",(plant,watered,sunlight))
        conn.commit()
        print("Plant added Successfully")

    elif(choice==2):
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
                print("------------")    
    elif choice==3:

        plant_id=int(input("Enter Plant ID : "))
        cursor.execute("""
                       select * from plants where id=?""",(plant_id,))
        plant=cursor.fetchone()
        if(plant is not None):
            new_date=input("Enter new watered date : ")
            cursor.execute("""
                       update plants set last_watered=? where id=?
                       """,(new_date,plant_id))
            conn.commit()
            print("Watering date updated successfully!")
       
            
        else:    
            print("Plant ID NOT Found")
    elif choice==4:
        plant_id=int(input("Enter plant ID to be deleted : "))
        cursor.execute("""
                       delete from plants where id=?""",(plant_id,))
        if(cursor.rowcount==0):
            print("Plant ID not found!")
        else:
            print("Plant Deleted successfully!")
        conn.commit()        
    elif choice==5:
        plant=input("Enter plant name :")
        cursor.execute("""
                       select * from plants where plant_name= ?""",(plant,))
        row=cursor.fetchone()
        if(row is None):
            print(plant," does not exists !")
        else:
          
            print("-----Plant Details-----")
            print("ID : ",row[0])
            print("Name : ",row[1])
            print("Last_water_date : ",row[2])
            print("Level of Sunlight Required : ",row[3])   

   
    
    elif choice==6:
        print("Thank you for using GreenMate!")
        break
    else:
        print("Invalid choice!")        
conn.close()
