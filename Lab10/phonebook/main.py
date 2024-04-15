import csv, psycopg2
from config import host, user, password, database


# connecting to pgadmin
def connectDatabase():
    # error handling
    try:
        conn = psycopg2.connect(host=host,
                                database=database,
                                user=user,
                                password=password)
        return conn

    except Exception as e:
        print("Error connectin to the database:", e)
        return None


# creating table if it doesnt exist
def createTable(conn):
    try:
        # cursor executes sql commands
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


# inputing data from console
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

        # oppening csv file to upload data
        with open(r"C:\Users\Admin\PP2\Lab10\data.csv", 'r') as file:
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


# setting default values if it doesnt provided
def updateData(conn, chosenId, newName=None, newNumber=None):
    try:
        cur = conn.cursor()

        # checking for none
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

        # filters for query
        print("Choose an option:")
        print("1. Query all")
        print("2. Query only names")
        print("3. Query only numbers")

        choice = input("Enter your choice (1-3): ")
        cur = conn.cursor()

        # all data
        if choice == '1':
            cur.execute('SELECT * FROM phone_book;')
            records = cur.fetchall()
            print("Queried data:")
            with open(r"C:\Users\Admin\PP2\Lab10\querriedData.txt", "w") as file:
                for record in records:
                    print("ID:", record[0], "Name:", record[1], "Phone Number:", record[2])
                    file.write(f"{record[0]}, {record[1]}, {record[2]}\n")

        # only names in id: name format
        elif choice == '2':
            cur.execute('SELECT id, name FROM phone_book;')
            records = cur.fetchall()
            print("Queried data:")
            with open(r"C:\Users\Admin\PP2\Lab10\querriedData.txt", "w") as file:
                for record in records:
                    print("ID:", record[0], "Name:", record[1])
                    file.write(f"{record[0]}: {record[1]}\n")

        # only numbers and id
        elif choice == '3':
            cur.execute('SELECT id, number FROM phone_book;')
            records = cur.fetchall()
            print("Queried data:")
            with open(r"C:\Users\Admin\PP2\Lab10\querriedData.txt", "w") as file:
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
        # deleting by username
        cur.execute("DELETE FROM phone_book WHERE name = %s;", (username,))
        conn.commit()
        print(f"User {username} was deleted")
    except Exception as e:
        print("An error occurred while deleting data:", e)


def main():
    conn = connectDatabase()
    if conn is not None:
        createTable(conn)
        while True:

            # imitation for interface
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

                # adding possibility to remain current value
                newName = None if newName == "" else newName
                newNumber = None if newNumber == "" else newNumber
                updateData(conn, chosenId, newName, newNumber)

            elif choice == '4':
                queryData(conn)

            elif choice == '5':
                rowToDelete = input("Enter a user name you want to delete: ")
                deleteData(conn, rowToDelete)

            elif choice == '6':
                print("Exiting program.")
                break

            else:
                print("Invalid choice. Please choose from 1-6.")
        conn.close()
    else:
        print("Failed to connect to the database")

    # code will lauch after exit


if __name__ == "__main__":
    main()