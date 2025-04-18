import psycopg2
import csv

# Функция для установления соединения с PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname="postgres", user="postgres", password="fank_emp2005", host="localhost", client_encoding="utf-8"
    )

# 1. Создание таблицы PhoneBook
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone_number VARCHAR(15) UNIQUE
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# 2. Вставка данных из CSV файла
def load_from_csv(csv_file):
    conn = connect_db()
    cursor = conn.cursor()
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            cursor.execute("""
                INSERT INTO PhoneBook (first_name, last_name, phone_number)
                VALUES (%s, %s, %s)
            """, (row[0], row[1], row[2]))
    conn.commit()
    cursor.close()
    conn.close()

# 3. Вставка данных через консоль
def insert_from_console():
    conn = connect_db()
    cursor = conn.cursor()
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_number = input("Enter phone number: ")
    cursor.execute("""
        INSERT INTO PhoneBook (first_name, last_name, phone_number)
        VALUES (%s, %s, %s)
    """, (first_name, last_name, phone_number))
    conn.commit()
    cursor.close()
    conn.close()

# 4. Обновление данных по номеру телефона
def update_data():
    conn = connect_db()
    cursor = conn.cursor()
    phone_number = input("Enter phone number to update: ")
    new_first_name = input("Enter new first name: ")
    new_phone_number = input("Enter new phone number: ")
    cursor.execute("""
        UPDATE PhoneBook
        SET first_name = %s, phone_number = %s
        WHERE phone_number = %s
    """, (new_first_name, new_phone_number, phone_number))
    conn.commit()
    cursor.close()
    conn.close()

# 5. Запрос данных по имени
def query_data_by_name():
    conn = connect_db()
    cursor = conn.cursor()
    search_name = input("Enter first name to search: ")
    cursor.execute("SELECT * FROM PhoneBook WHERE first_name = %s", (search_name,))
    records = cursor.fetchall()
    for record in records:
        print(record)
    cursor.close()
    conn.close()

# 6. Запрос данных по телефону
def query_data_by_phone():
    conn = connect_db()
    cursor = conn.cursor()
    search_phone = input("Enter phone number to search: ")
    cursor.execute("SELECT * FROM PhoneBook WHERE phone_number = %s", (search_phone,))
    records = cursor.fetchall()
    for record in records:
        print(record)
    cursor.close()
    conn.close()

# 7. Удаление данных по телефону
def delete_data_by_phone():
    conn = connect_db()
    cursor = conn.cursor()
    phone_number = input("Enter phone number to delete: ")
    cursor.execute("DELETE FROM PhoneBook WHERE phone_number = %s", (phone_number,))
    conn.commit()
    cursor.close()
    conn.close()

# 8. Удаление данных по имени
def delete_data_by_name():
    conn = connect_db()
    cursor = conn.cursor()
    first_name = input("Enter first name to delete: ")
    cursor.execute("DELETE FROM PhoneBook WHERE first_name = %s", (first_name,))
    conn.commit()
    cursor.close()
    conn.close()

# Главное меню для пользователя
def main():
    print("Welcome to the PhoneBook management system.")
    while True:
        print("\nSelect an action:")
        print("1. Create table")
        print("2. Load data from CSV file")
        print("3. Insert data from console")
        print("4. Update data")
        print("5. Query data by name")
        print("6. Query data by phone number")
        print("7. Delete data by phone number")
        print("8. Delete data by first name")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            csv_file = input("Enter the path to the CSV file: ")
            load_from_csv(csv_file)
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_data()
        elif choice == "5":
            query_data_by_name()
        elif choice == "6":
            query_data_by_phone()
        elif choice == "7":
            delete_data_by_phone()
        elif choice == "8":
            delete_data_by_name()
        elif choice == "9":
            print("Exiting the PhoneBook system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
