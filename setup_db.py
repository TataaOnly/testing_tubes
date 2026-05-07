import mysql.connector

def setup_database():
    print("Setting up the database...")
    
    # First, connect to MySQL without specifying a database to create the 'simrs' database
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()
        
        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS simrs")
        print("Database 'simrs' created or already exists.")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL Server: {err}")
        print("Please ensure your MySQL server (like XAMPP or native MySQL) is running.")
        return

    # Now connect to the 'simrs' database and execute the SQL script
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="simrs"
        )
        cursor = conn.cursor()
        
        # Read the simrs.sql file
        with open('simrs.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        # Execute the script statement by statement
        print("Importing simrs.sql...")
        
        # MySQL Connector allows executing multi-statement strings if multi=True
        results = cursor.execute(sql_script, multi=True)
        for result in results:
            pass # Iterate through results to ensure execution
            
        conn.commit()
        print("Database setup complete! You can now run the app using `python app.py`")
        
    except FileNotFoundError:
        print("Error: simrs.sql file not found.")
    except mysql.connector.Error as err:
        print(f"Error executing SQL: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    setup_database()
