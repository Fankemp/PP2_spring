import psycopg2
import csv

def connect_db():
    """Устанавливает соединение с базой данных"""
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="fank_emp2005",
        host="localhost",
        client_encoding="utf-8"
    )

def validate_phone(phone):
    """Проверяет корректность номера телефона"""
    return phone.isdigit() and 10 <= len(phone) <= 15

def create_table():
    """Создает таблицу и хранимые процедуры"""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Создаем таблицу
    cursor.execute("""
    DROP TABLE IF EXISTS PhoneBook;
    CREATE TABLE PhoneBook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        phone_number VARCHAR(15) UNIQUE
    );
    """)
    
    # Удаляем существующие процедуры/функции если есть
    cursor.execute("""
    DROP FUNCTION IF EXISTS search_by_pattern;
    DROP PROCEDURE IF EXISTS upsert_user;
    DROP PROCEDURE IF EXISTS insert_many_users;
    DROP FUNCTION IF EXISTS get_paginated_records;
    DROP PROCEDURE IF EXISTS delete_by_username_or_phone;
    """)
    
    # Функция поиска по шаблону
    cursor.execute("""
    CREATE OR REPLACE FUNCTION search_by_pattern(pattern TEXT)
    RETURNS TABLE(
        result_id INT, 
        result_first_name VARCHAR(50),
        result_last_name VARCHAR(50),
        result_phone_number VARCHAR(15)
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT 
            pb.id AS result_id,
            pb.first_name AS result_first_name,
            pb.last_name AS result_last_name,
            pb.phone_number AS result_phone_number
        FROM PhoneBook pb
        WHERE pb.first_name ILIKE '%' || pattern || '%'
           OR pb.last_name ILIKE '%' || pattern || '%'
           OR pb.phone_number LIKE '%' || pattern || '%';
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # Процедура добавления/обновления (исправленная)
    cursor.execute("""
    CREATE OR REPLACE PROCEDURE upsert_user(
        f_name VARCHAR(50),
        l_name VARCHAR(50),
        phone VARCHAR(15)
    ) AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM PhoneBook WHERE phone_number = phone) THEN
            UPDATE PhoneBook 
            SET first_name = f_name, last_name = l_name 
            WHERE phone_number = phone;
        ELSE
            INSERT INTO PhoneBook (first_name, last_name, phone_number)
            VALUES (f_name, l_name, phone);
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # Процедура массового добавления
    cursor.execute("""
    CREATE OR REPLACE PROCEDURE insert_many_users(
        users_list TEXT[][], 
        OUT incorrect_data TEXT[]
    ) AS $$
    DECLARE
        user_record TEXT[];
    BEGIN
        incorrect_data := '{}';
        
        FOREACH user_record SLICE 1 IN ARRAY users_list LOOP
            IF user_record[3] ~ '^[0-9]{10,15}$' THEN
                CALL upsert_user(
                    user_record[1]::VARCHAR(50),
                    user_record[2]::VARCHAR(50),
                    user_record[3]::VARCHAR(15)
                );
            ELSE
                incorrect_data := array_append(incorrect_data, 
                    user_record[1] || '|' || user_record[2] || '|' || user_record[3]);
            END IF;
        END LOOP;
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # Функция пагинации
    cursor.execute("""
    CREATE OR REPLACE FUNCTION get_paginated_records(
        lim INT, offs INT
    ) RETURNS TABLE(
        id INT, 
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        phone_number VARCHAR(15)
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT * FROM PhoneBook
        ORDER BY id
        LIMIT lim OFFSET offs;
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # Процедура удаления
    cursor.execute("""
    CREATE OR REPLACE PROCEDURE delete_by_username_or_phone(search_term TEXT) AS $$
    BEGIN
        DELETE FROM PhoneBook
        WHERE first_name ILIKE '%' || search_term || '%'
           OR last_name ILIKE '%' || search_term || '%'
           OR phone_number LIKE '%' || search_term || '%';
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    conn.commit()
    print("Таблица и хранимые процедуры успешно созданы!")
    cursor.close()
    conn.close()

def search_by_pattern():
    """Поиск записей по шаблону"""
    conn = connect_db()
    cursor = conn.cursor()
    pattern = input("Введите строку для поиска: ")
    
    cursor.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
    results = cursor.fetchall()
    
    if not results:
        print("Записи не найдены")
    else:
        print("\nРезультаты поиска:")
        print("{:<5} {:<15} {:<15} {:<15}".format("ID", "Имя", "Фамилия", "Телефон"))
        print("-" * 50)
        for row in results:
            print("{:<5} {:<15} {:<15} {:<15}".format(*row))
    
    cursor.close()
    conn.close()


def upsert_user():
    """Добавление или обновление пользователя"""
    conn = connect_db()
    cursor = conn.cursor()
    
    print("\nДобавление/обновление пользователя")
    first_name = input("Имя: ").strip()
    last_name = input("Фамилия: ").strip()
    phone = input("Телефон: ").strip()
    
    if not validate_phone(phone):
        print("Ошибка: Некорректный номер телефона (должен содержать 10-15 цифр)")
        return
    
    # Исправленный вызов процедуры
    cursor.execute(
        "CALL upsert_user(%s::VARCHAR(50), %s::VARCHAR(50), %s::VARCHAR(15))",
        (first_name, last_name, phone)
    )
    
    conn.commit()
    print("Операция выполнена успешно!")
    cursor.close()
    conn.close()

def insert_many_users():
    """Массовое добавление пользователей"""
    conn = connect_db()
    cursor = conn.cursor()

    users = []
    print("\nВведите данные пользователей (формат: имя,фамилия,телефон). Для завершения введите 'done':")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() == 'done':
            break

        parts = user_input.split(',')
        if len(parts) != 3:
            print("Ошибка: Неверный формат. Используйте: имя,фамилия,телефон")
            continue

        users.append([parts[0].strip(), parts[1].strip(), parts[2].strip()])

    if not users:
        print("Не введено ни одного пользователя")
        return

    # Формируем массив для PostgreSQL
    users_str = "ARRAY["
    users_str += ",".join([f"ARRAY['{u[0]}','{u[1]}','{u[2]}']" for u in users])
    users_str += "]::TEXT[][]"

    # Вызываем процедуру и получаем некорректные данные
    cursor.execute(f"""
    DO $$
    DECLARE
        incorrect TEXT[];
    BEGIN
        CALL insert_many_users({users_str}, incorrect);
        RAISE NOTICE 'Некорректные данные: %', incorrect;
    END $$;
    """)
    conn.commit()

    print("\nОперация завершена. Проверьте логи PostgreSQL для информации о некорректных данных.")
    cursor.close()
    conn.close()

def get_paginated_records():
    """Получение записей с пагинацией"""
    conn = connect_db()
    cursor = conn.cursor()

    limit = input("Количество записей на странице: ")
    offset = input("Смещение: ")

    if not limit.isdigit() or not offset.isdigit():
        print("Ошибка: введите числа для limit и offset")
        return

    cursor.execute("SELECT * FROM get_paginated_records(%s, %s)", (int(limit), int(offset)))
    results = cursor.fetchall()

    if not results:
        print("Записи не найдены")
    else:
        print("\nРезультаты:")
        print("{:<5} {:<15} {:<15} {:<15}".format("ID", "Имя", "Фамилия", "Телефон"))
        print("-" * 50)
        for row in results:
            print("{:<5} {:<15} {:<15} {:<15}".format(*row))

    cursor.close()
    conn.close()

def delete_by_username_or_phone():
    """Удаление записей по имени или телефону"""
    conn = connect_db()
    cursor = conn.cursor()

    search_term = input("Введите имя, фамилию или часть номера телефона для удаления: ")

    cursor.execute("CALL delete_by_username_or_phone(%s)", (search_term,))
    conn.commit()

    print(f"Удалено записей: {cursor.rowcount}")
    cursor.close()
    conn.close()

def main():
    """Главное меню"""
    print("Система управления телефонной книгой")

    while True:
        print("\nМеню:")
        print("1. Инициализировать базу данных")
        print("2. Поиск по шаблону")
        print("3. Добавить/обновить пользователя")
        print("4. Массовое добавление пользователей")
        print("5. Просмотр с пагинацией")
        print("6. Удаление по имени/телефону")
        print("7. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            search_by_pattern()
        elif choice == "3":
            upsert_user()
        elif choice == "4":
            insert_many_users()
        elif choice == "5":
            get_paginated_records()
        elif choice == "6":
            delete_by_username_or_phone()
        elif choice == "7":
            print("Выход из системы")
            break
        else:
            print("Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    main()
