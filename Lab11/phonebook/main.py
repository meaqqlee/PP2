#imports
import csv, psycopg2

#database connection
def connect_database():
    try:
        conn = psycopg2.connect(host="localhost", database="phonebook11", user="postgres", password="magzhan0201")
        print("Database connected successfully")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def createTable(conn):
    try:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS phone_book (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                number VARCHAR(255) NOT NULL
            );
        ''')
        conn.commit()
        print("Table created successfully")
    except Exception as e:
        print("Error while creating the table:", e)
        conn.rollback()

def setupDatabaseFunctions(conn):
    cur = conn.cursor()
    try:
        # Function to search records by pattern
        cur.execute('''
        CREATE OR REPLACE FUNCTION search_records(pattern VARCHAR)
        RETURNS TABLE(id INT, name VARCHAR, number VARCHAR) AS $$
        BEGIN
            RETURN QUERY SELECT id, name, number FROM phone_book
            WHERE name LIKE '%' || pattern || '%' OR number LIKE '%' || pattern || '%';
        END;
        $$ LANGUAGE plpgsql;
        ''')

        # Procedure to insert or update a user
        cur.execute('''
        CREATE OR REPLACE PROCEDURE insert_or_update_user(user_name VARCHAR, phone_number VARCHAR)
        AS $$
        BEGIN
            IF EXISTS (SELECT 1 FROM phone_book WHERE name = user_name) THEN
                UPDATE phone_book SET number = phone_number WHERE name = user_name;
            ELSE
                INSERT INTO phone_book(name, number) VALUES (user_name, phone_number);
            END IF;
        END;
        $$ LANGUAGE plpgsql;
        ''')

        # Procedure for bulk inserting users
        cur.execute('''
        CREATE OR REPLACE PROCEDURE bulk_insert_users(users RECORD[])
        AS $$
        DECLARE
            user RECORD;
        BEGIN
            FOR user IN SELECT * FROM unnest(users)
            LOOP
                CALL insert_or_update_user(user.name, user.number);
            END LOOP;
        END;
        $$ LANGUAGE plpgsql;
        ''')

        # Function for pagination
        cur.execute('''
        CREATE OR REPLACE FUNCTION paginate_phonebook(limit INT, offset INT)
        RETURNS TABLE(id INT, name VARCHAR, number VARCHAR) AS $$
        BEGIN
            RETURN QUERY SELECT id, name, number FROM phone_book
            ORDER BY id LIMIT limit OFFSET offset;
        END;
        $$ LANGUAGE plpgsql;
        ''')

        # Procedure to delete data by name or phone
        cur.execute('''
        CREATE OR REPLACE PROCEDURE delete_record_by_name_or_phone(username VARCHAR, phone_number VARCHAR)
        AS $$
        BEGIN
            DELETE FROM phone_book WHERE name = username OR number = phone_number;
        END;
        $$ LANGUAGE plpgsql;
        ''')

        conn.commit()
        print("All procedures and functions created successfully")
    except Exception as e:
        print("Error while creating procedures and functions:", e)
        conn.rollback()
    finally:
        cur.close()

#inputing data from console
def inputData(conn, name, number):

    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO phone_book(name, number) VALUES(%s, %s);
        ''', (name, number))

        conn.commit()
        print("Data inputted successfully")
    
    except Exception as e:
        print("Error while inputing data:", e)
        conn.rollback()

def inputCSV(conn):

    try:
        cur = conn.cursor()

        #oppening csv file to upload data
        with open(r"C:\Users\Admin\PP2\Lab11\phonebook\data.csv", 'r') as file:
            table = csv.reader(file)
            for row in table:
                cur.execute('''
                    INSERT INTO phone_book(name, number) VALUES(%s, %s);
                ''', (row[0], row[1]))
        conn.commit()
        print("Data from data.csv inputted successfully")
    
    except Exception as e:
        print("Error while inputing data from csv:", e)
        conn.rollback()

#setting default values if it doesnt provided
def updateData(conn, chosenId, newName = None, newNumber = None):

    try:
        cur = conn.cursor()

        #checking for none
        if newName: 
            cur.execute("UPDATE phone_book SET name = %s WHERE id = %s;", (newName, chosenId))

        if newNumber: 
            cur.execute("UPDATE phone_book SET number = %s WHERE id = %s;", (newNumber, chosenId))
        

        conn.commit()
        print("Data updated successfully")
    
    except Exception as e:
        print("Error while updating data:", e)
        conn.rollback()

def queryData(conn):
    try:
        
        #filters for query
        print("Choose an option:")
        print("1. Query all")
        print("2. Query only names")
        print("3. Query only numbers")
        
        choice = input("Enter your choice (1-3): ")
        cur = conn.cursor()

        #all data
        if choice == '1':
            cur.execute('SELECT * FROM phone_book;')
            records = cur.fetchall()
            print("Queried data:")
            with open(r"C:\Users\Admin\PP2\Lab11\phonebook\querriedData.txt", "w") as file:
                for record in records:
                    print("ID:", record[0], "Name:", record[1], "Phone Number:", record[2])
                    file.write(f"{record[0]}, {record[1]}, {record[2]}\n")
        
        #only names in id: name format
        elif choice == '2':
            cur.execute('SELECT id, name FROM phone_book;')
            records = cur.fetchall()
            print("Queried data:")
            with open(r"C:\Users\Admin\PP2\Lab11\phonebook\querriedData.txt", "w") as file:
                for record in records:
                    print("ID:", record[0], "Name:", record[1])
                    file.write(f"{record[0]}: {record[1]}\n")
        
        #only numbers and id
        elif choice == '3':
            cur.execute('SELECT id, number FROM phone_book;')
            records = cur.fetchall()
            print("Queried data:")
            with open(r"C:\Users\Admin\PP2\Lab11\phonebook\querriedData.txt", "w") as file:
                for record in records:
                    print("ID:", record[0], "Number:", record[1])
                    file.write(f"{record[0]}: {record[1]}\n")
        else:
                print("Invalid choice. Please choose from 1-3.")
    
    
    except Exception as e:
        print("An error occurred while querying data:", e)

def deleteData(conn, username):
    try:
        cur = conn.cursor()
        #deleting by username
        cur.execute("DELETE FROM phone_book WHERE name = %s;", (username, ))
        conn.commit()
        print(f"User {username} was deleted")
    except Exception as e:
        print("An error occurred while deleting data:", e)

def main():
    conn = connect_database()
    if conn:
        createTable(conn)
        setupDatabaseFunctions(conn)  # Setting up database functions and procedures
        while True:
            print("Choose an option:")
            print("1. Enter new contact")
            print("2. Upload the data from csv")
            print("3. Update a row")
            print("4. Query the table")
            print("5. Delete a row")
            print("6. Exit")
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                person_name = input("Enter person's name: ")
                phone_number = input("Enter phone number: ")
                inputData(conn, person_name, phone_number)

            elif choice == '2':
                inputCSV(conn)

            elif choice == '3':
                chosenId = int(input("Enter an ID of the user: "))
                newName = input("Enter a new name, or press enter to save current value: ")
                newNumber = input("Enter a new number, or press enter to save current value: ")
                newName = None if newName == "" else newName
                newNumber = None if newNumber == "" else newNumber
                updateData(conn, chosenId, newName, newNumber)

            elif choice == '4':
                queryData(conn)

            elif choice == '5':
                rowToDelete = input("Enter a user name you want to delete: ")
                deleteData(conn, rowToDelete)

            elif choice == '6':
                pattern = input("Enter search pattern (name, surname, or phone number part): ")
                searchByPattern(conn, pattern)  # You'll need to implement this function to call the search_records function

            elif choice == '7':
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please choose from 1-6.")
        conn.close()
    else:
        print("Failed to connect to the database")

if __name__ == "__main__":
    main()


def searchByPattern(conn, pattern):
    cur = conn.cursor()
    try:
        cur.callproc('search_records', [pattern])
        records = cur.fetchall()
        print("Search Results:")
        for rec in records:
            print(f"ID: {rec[0]}, Name: {rec[1]}, Number: {rec[2]}")
    except Exception as e:
        print("Error during search:", e)
    finally:
        cur.close()


def insertOrUpdateUser(conn, user_name, phone_number):
    cur = conn.cursor()
    try:
        cur.callproc('insert_or_update_user', [user_name, phone_number])
        conn.commit()
        print(f"User {user_name} has been inserted or updated successfully.")
    except Exception as e:
        print(f"Error while inserting or updating user: {e}")
        conn.rollback()
    finally:
        cur.close()

def bulkInsertUsers(conn, user_list):
    cur = conn.cursor()
    try:
        # Convert user_list into a list of PostgreSQL RECORD types
        # Example user_list: [(name1, number1), (name2, number2), ...]
        cur.execute("SELECT * FROM bulk_insert_users(%s)", (user_list,))
        conn.commit()
        print("Bulk insert operation completed successfully.")
    except Exception as e:
        print(f"Error during bulk insert: {e}")
        conn.rollback()
    finally:
        cur.close()


def paginatePhonebook(conn, limit, offset):
    cur = conn.cursor()
    try:
        cur.callproc('paginate_phonebook', [limit, offset])
        records = cur.fetchall()
        print("Paginated Results:")
        for record in records:
            print(f"ID: {record[0]}, Name: {record[1]}, Number: {record[2]}")
    except Exception as e:
        print(f"Error during pagination: {e}")
    finally:
        cur.close()

def deleteRecordByNameOrPhone(conn, username, phone_number):
    cur = conn.cursor()
    try:
        cur.callproc('delete_record_by_name_or_phone', [username, phone_number])
        conn.commit()
        print(f"Record with name {username} or phone {phone_number} has been deleted.")
    except Exception as e:
        print(f"Error while deleting data: {e}")
        conn.rollback()
    finally:
        cur.close()

